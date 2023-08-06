# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

from math import log
from typing import Callable, Dict, List, Optional, Tuple, Union

import jax.numpy as jnp
import numpy as np
import pandas as pd
from jax.interpreters.xla import DeviceArray
from jax.lax import scan

from pyhgf.binary import loop_binary_inputs
from pyhgf.continuous import gaussian_surprise, loop_continuous_inputs
from pyhgf.plots import plot_correlations, plot_trajectories
from pyhgf.response import total_binary_surprise, total_gaussian_surprise
from pyhgf.structure import structure_as_dict
from pyhgf.typing import ParametersType


class HGF(object):
    r"""The two-level and three-level Hierarchical Gaussian Filters (HGF).

    This class use pre-made nodes structures that corresponds to the most widely used
    HGF. The inputs can be continuous or binary.

    Attributes
    ----------
    hgf_results : dict
        After oberving the data using the `input_data` method, the output of the model
        are stored in the `hgf_results` dictionary.
    model_type : str
        The model implemented (can be `"continuous"`, `"binary"` or `"custom"`).
    n_levels : int
        The number of hierarchies in the model, including the input vector. Cannot be
        less than 2.
    node_structure : tuple
        A tuple of tuples representing the nodes hierarchy.
    node_trajectories : tuples
        The node structure updated at each new observation.
    results :
        Time, values inputs and overall surprise of the model.
    structure_dict : dict
        The node structure as a dictionary,
        retrieved using :py:fun:`pyhgf.structure.structure_as_dict`
    verbose : bool
        Verbosity level.

    """

    def __init__(
        self,
        n_levels: Optional[int] = 2,
        model_type: str = "continuous",
        initial_mu: Dict[str, Optional[float]] = {"1": 0.0, "2": 0.0},
        initial_pi: Dict[str, Optional[float]] = {"1": 1.0, "2": 1.0},
        omega_input: float = log(1e-4),
        omega: Dict[str, Optional[float]] = {"1": -3.0, "2": -3.0},
        kappas: Dict[str, Optional[float]] = {"1": 1.0},
        eta0: float = 0.0,
        eta1: float = 1.0,
        pihat: float = jnp.inf,
        rho: Dict[str, Optional[float]] = {"1": 0.0, "2": 0.0},
        verbose: bool = True,
    ):
        r"""Parameterization of the HGF model.

        Parameters
        ----------
        n_levels : int | None
            The number of hierarchies in the perceptual model (can be `2` or `3`). If
            `None`, the nodes hierarchy is not created and might be provided afterward
            using `add_nodes()`. Defaults to `2` for a 2-level HGF.
        model_type : str
            The model type to use (can be `"continuous"`, `"binary"` or `"custom"`).
        initial_mu : dict
            Dictionary containing the initial values for the :math:`\\mu` parameter at
            different levels of the hierarchy. Defaults set to `{"1": 0.0, "2": 0.0}`
            for a 2-level model for continuous inputs.
        initial_pi : dict
            Dictionary containing the initial values for the :math:`\\pi` parameter at
            different levels of the hierarchy. Pis values encode the precision of the
            values at each level (Var = 1/pi) Defaults set to `{"1": 1.0, "2": 1.0}` for
            a 2-level model.
        omega : dict
            Dictionary containing the initial values for the :math:`\\omega` parameter
            at different levels of the hierarchy. :math:`\\omega` represents the tonic
            part of the variance (the part that is not affected by the parent node).
            Defaults set to `{"1": -10.0, "2": -10.0}` for a 2-level model for
            continuous inputs. This parameter is only required for Gaussian Random Walk
            nodes.
        omega_input : float
            Default value sets to `log(1e-4)`. Represents the noise associated with
            the input.
        rho : dict
            Dictionary containing the initial values for the :math:`\\rho` parameter at
            different levels of the hierarchy. Rho represents the drift of the random
            walk. This parameter is only required for Gaussian Random Walk nodes.
            Defaults set all entries to `0` according to the number of required levels.
        kappas : dict
            Dictionary containing the initial values for the :math:`\\kappa` parameter
            at different levels of the hierarchy. Kappa represents the phasic part of
            the variance (the part that is affected by the parents nodes) and will
            defines the strenght of the connection between the node and the parent
            node. Often fixed to `1`. Defaults set to `{"1": 1.0}` for a 2-level model.
            This parameter is only required for Gaussian Random Walk nodes.
        eta0 : float
            The first categorical value of the binary node. Defaults to `0.0`. Only
            relevant if `model_type="binary"`.
        eta1 : float
            The second categorical value of the binary node. Defaults to `0.0`. Only
            relevant if `model_type="binary"`.
        pihat : float
            The precision of the binary input node. Default to `jnp.inf`. Only relevant
            if `model_type="binary"`.
        verbose : bool
            Verbosity of the methods for model creation and fitting. Defaults to `True`.

        Raises
        ------
        ValueError
            If `model_type` is not `"continuous"`, `"binary"` or `"custom"`.

        """
        self.model_type = model_type
        self.verbose = verbose
        self.n_levels = n_levels
        self.structure_dict = None

        if model_type not in ["continuous", "binary", "custom"]:
            raise ValueError(
                "Invalid model type. Should be continuous, binary or custom,"
            )

        if self.model_type == "custom":
            if self.verbose:
                print(
                    (
                        "Initializing a Hierarchical Gaussian Filter"
                        " using a custom node structure"
                    )
                )
        else:
            if self.verbose:
                print(
                    (
                        f"Creating a {self.model_type} Hierarchical Gaussian Filter "
                        f"with {self.n_levels} levels."
                    )
                )

            if self.n_levels == 2:

                # Second level
                x2_parameters = {
                    "mu": initial_mu["2"],
                    "muhat": jnp.nan,
                    "pi": initial_pi["2"],
                    "pihat": jnp.nan,
                    "kappas": None,
                    "nu": jnp.nan,
                    "psis": None,
                    "omega": omega["2"],
                    "rho": rho["2"],
                }
                x2 = ((x2_parameters, None, None),)

            elif self.n_levels == 3:

                # Third level
                x3_parameters = {
                    "mu": initial_mu["3"],
                    "muhat": jnp.nan,
                    "pi": initial_pi["3"],
                    "pihat": jnp.nan,
                    "kappas": None,
                    "nu": jnp.nan,
                    "psis": None,
                    "omega": omega["3"],
                    "rho": rho["3"],
                }
                x3 = ((x3_parameters, None, None),)

                # Second level
                x2_parameters = {
                    "mu": initial_mu["2"],
                    "muhat": jnp.nan,
                    "pi": initial_pi["2"],
                    "pihat": jnp.nan,
                    "kappas": (kappas["2"],),  # type: ignore
                    "nu": jnp.nan,
                    "psis": None,
                    "omega": omega["2"],
                    "rho": rho["2"],
                }
                x2 = ((x2_parameters, None, x3),)

            x1_parameters = {
                "mu": initial_mu["1"],
                "muhat": jnp.nan,
                "pi": initial_pi["1"],
                "pihat": jnp.nan,
                "kappas": (kappas["1"],),
                "nu": jnp.nan,
                "psis": None,
                "omega": omega["1"],
                "rho": rho["1"],
            }

            if model_type == "continuous":

                # First level (continuous node)
                x1 = ((x1_parameters, None, x2),)

                # Input node
                input_node_parameters: ParametersType = {
                    "kappas": None,
                    "omega": omega_input,
                }

                self.node_structure = input_node_parameters, x1, None

            elif model_type == "binary":

                # First level (binary node)
                x1 = ((x1_parameters, x2, None),)

                input_node_parameters: ParametersType = {
                    "pihat": pihat,
                    "eta0": eta0,
                    "eta1": eta1,
                }
                self.node_structure = input_node_parameters, x1, None

    def add_nodes(self, nodes: Tuple):
        """Add a custom node structure.

        Parameters
        ----------
        nodes : tuple
            The input node embeding the node hierarchy that will be updated during
            model fit.

        """
        self.node_structure = nodes  # type: ignore
        return self

    def input_data(
        self,
        input_data: Union[List, np.ndarray, DeviceArray],
        time: Optional[np.ndarray] = None,
    ):
        """Add new observations.

        Parameters
        ----------
        input_data : np.ndarray
            The new observations.
        time : np.ndarray | None
            Time vector (optional). If `None`, the time vector will defaults to
            `np.arange(0, len(input_data))`.

        """
        input_data = jnp.asarray(input_data)

        if self.verbose:
            print((f"Add {input_data.shape[0]} new {self.model_type} observations."))
        if time is None:
            # create a time vector (starting at 1 as time 0 already exists by default)
            time = jnp.arange(0.0, len(input_data))
        else:
            assert len(input_data) == len(time)

        # Initialise the first values
        res_init = (
            self.node_structure,
            {
                "time": time[0],
                "value": input_data[0],
                "surprise": jnp.array(0.0),
            },
        )

        # create the input array (data, time)
        data = jnp.array([input_data, time], dtype=float).T

        # this is where the model loop over the input time series
        # at each input the node structure is traversed and beliefs are updated
        # using precision-weighted prediction errors
        if self.model_type == "continuous":
            _, scan_updates = scan(loop_continuous_inputs, res_init, data[1:, :])
        elif self.model_type == "binary":
            _, scan_updates = scan(loop_binary_inputs, res_init, data[1:, :])
        else:
            raise ValueError("This method only works with binary or continuous models")

        # the node structure at each value update
        self.node_trajectories = scan_updates[0]

        self.results = scan_updates[1]  # time, values and surprise

        return self

    def plot_trajectories(self, **kwargs):
        """Plot the parameters trajectories."""
        return plot_trajectories(hgf=self, **kwargs)

    def plot_correlations(self):
        """Plot the heatmap of cross-trajectories correlation."""
        return plot_correlations(hgf=self)

    def surprise(
        self,
        response_function: Optional[Callable] = None,
        response_function_parameters: Tuple = (),
    ):
        """Surprise (negative log probability) under new observations.

        The surprise depends on the input data, the model parameters, the response
        function and its additional parameters(optional).

        Parameters
        ----------
        response_function : callable (optional)
            The response function to use to compute the model surprise. If `None`
            (default), return the sum of gaussian surprise if `model_type=="continuous"`
            or the sum of the binary surprise if `model_type=="binary"`.
        response_function_parameters : tuple (optional)
            Additional parameters to the response function (optional) .

        Returns
        -------
        surprise : float
            The model surprise given the input data and the response function.

        """
        if response_function is None:
            response_function = (
                total_gaussian_surprise
                if self.model_type == "continuous"
                else total_binary_surprise
            )

        return response_function(
            hgf=self,
            response_function_parameters=response_function_parameters,
        )

    def structure_as_dict(self) -> Dict:
        """Export the node structure to a dictionary of nodes.

        Returns
        -------
        structure_dict : dict
            The node structure as a dictionary, each node is a key in the dictionary,
            from 1 (lower node) to **n**.

        """
        if self.structure_dict is None:
            structure_dict = {}
            self.structure_dict = structure_as_dict(
                node_structure=self.node_trajectories,
                node_id=0,
                structure_dict=structure_dict,
            )
        return self.structure_dict

    def to_pandas(self) -> pd.DataFrame:
        """Export the nodes trajectories and surprise as a Pandas data frame.

        Returns
        -------
        structure_df : pd.DataFrame
            Pandas data frame with the time series of the sufficient statistics and
            surprise of each node in the structure.

        """
        node_dict = self.structure_as_dict()
        structure_df = pd.DataFrame(
            {
                "time": self.results["time"],
                "observation": self.results["value"],
                "surprise": self.results["surprise"],
            }
        )
        # loop over nodes and store sufficient statistics with surprise
        for key in list(node_dict.keys())[1:]:
            structure_df[f"{key}_mu"] = node_dict[key]["mu"]
            structure_df[f"{key}_pi"] = node_dict[key]["pi"]
            structure_df[f"{key}_muhat"] = node_dict[key]["muhat"]
            structure_df[f"{key}_pihat"] = node_dict[key]["pihat"]
            surprise = gaussian_surprise(
                x=node_dict[key]["mu"][1:],
                muhat=node_dict[key]["muhat"][:-1],
                pihat=node_dict[key]["pihat"][:-1],
            )
            structure_df[f"{key}_surprise"] = np.insert(surprise, 0, np.nan)

        return structure_df
