"""Defines a Distribution which only has one value."""

import typing

import numpy as np
from numpy import typing as npt

from simba_ml import error_handler
from simba_ml.simulation.distributions import distribution


class Constant(distribution.Distribution):
    """An object which represents a constant value.

    Attributes:
        value: The scalar used as constant value.

    Raises:
        TypeError: If value is not a float or int.
    """

    def __init__(self, value: typing.Union[float, int]) -> None:
        """Inits the Constant with the provided value.

        Args:
            value: The scalar used as constant value.
        """
        self.value = value
        error_handler.confirm_param_is_float_or_int(self.value, "value")

    def get_random_values(self, shape: tuple[int, ...]) -> npt.NDArray[np.float64]:
        """Returns an array of the constant value in the given shape.

        Args:
            shape: The shape of the output array.

        Returns:
            np.ndarray[float]
        """
        return np.full(shape, self.value)

    def get_samples_from_hypercube(self, n: int) -> list[float]:
        """Samples n values from a hypercube.

        Args:
            n: the number of samples.

        Returns:
            Samples of the distributions, sampled from a hypercube.
        """
        return list(np.full(n, self.value))
