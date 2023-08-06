# Author: Nicolas Legrand <nicolas.legrand@cas.au.dk>

from typing import TYPE_CHECKING

import jax.numpy as jnp

if TYPE_CHECKING:
    from pyhgf.model import HGF


def total_gaussian_surprise(hgf: "HGF", response_function_parameters):
    """Sum of the gaussian surprise along the time series (continuous HGF).

    .. note::
      The Gaussian surprise is the default method to compute surprise when
      `model_type=="continuous"`, therefore this method will only return the sum of
      valid time points, and `jnp.inf` if the model could not fit.

    Parameters
    ----------
    hgf : :py:class`pyhgf.model.HGF`
        Instance of the HGF model.
    response_function_parameters : None
        No additional parameters are required.

    Returns
    -------
    surprise : DeviceArray
        The model surprise given the input data.

    """
    # Fill surprises with zeros if invalid input
    this_surprise = jnp.where(
        jnp.any(jnp.isnan(hgf.results["value"][1:]), axis=0),
        0.0,
        hgf.results["surprise"],
    )

    # Return an infinite surprise if the model cannot fit
    this_surprise = jnp.where(jnp.isnan(this_surprise), jnp.inf, this_surprise)

    # Sum the surprise for this model
    surprise = jnp.sum(this_surprise)

    return surprise


def total_binary_surprise(hgf: "HGF", response_function_parameters):
    """Sum of the binary surprise along the time series (binary HGF).

    .. note::
      The binary surprise is the default method to compute surprise when
      `model_type=="binary"`, therefore this method will only return the sum of
      valid time points, and `jnp.inf` if the model could not fit.

    Parameters
    ----------
    hgf : :py:class`pyhgf.model.HGF`
        Instance of the HGF model.
    response_function_parameters : None
        No additional parameters are required.

    Returns
    -------
    surprise : DeviceArray
        The model surprise given the input data.

    """
    # Fill surprises with zeros if invalid input
    this_surprise = jnp.where(
        jnp.any(jnp.isnan(hgf.results["value"][1:]), axis=0),
        0.0,
        hgf.results["surprise"],
    )

    # Return an infinite surprise if the model cannot fit
    this_surprise = jnp.where(jnp.isnan(this_surprise), jnp.inf, this_surprise)

    # Sum the surprise for this model
    surprise = jnp.sum(this_surprise)

    return surprise
