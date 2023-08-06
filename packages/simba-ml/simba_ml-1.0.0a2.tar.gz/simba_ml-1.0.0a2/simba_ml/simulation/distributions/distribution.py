"""Defines an abstract definition of `Distribution`."""

import abc

import numpy as np
from numpy import typing as npt


class Distribution(abc.ABC):
    """A Distribution presents a set of values a property can have.

    Note:
        If no explicit way for sampling with the hypercube,
        the following code-snippet can probably be used:
        ```
        exactness = 1000
        vals = self.get_random_values((n * exactness, ))
        vals = np.sort(vals)
        return [
            np.random.choice(vals[i:i+exactness
            ]) for i in range(0, len(vals), exactness)]
        ```
    """

    def get_random_value(self) -> np.float64:
        """Samples a random value due to the type of Distribution.

        Returns:
            float: A randomly selected value of the set of possible values.
        """
        return self.get_random_values(shape=(1,))[0]

    @abc.abstractmethod
    def get_random_values(self, shape: tuple[int, ...]) -> npt.NDArray[np.float64]:
        """Samples an array with the given distribution.

        Args:
            shape: The shape of the output array.
        """

    @abc.abstractmethod
    def get_samples_from_hypercube(self, n: int) -> list[float]:
        """Samples n values from a hypercube.

        Args:
            n: the number of samples.
        """
