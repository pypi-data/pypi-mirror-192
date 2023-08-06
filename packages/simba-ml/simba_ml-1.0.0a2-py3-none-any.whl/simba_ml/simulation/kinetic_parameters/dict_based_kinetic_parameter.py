"""Defines a kinetic parameter, that is constant over time."""
import pandas as pd

from simba_ml.simulation.kinetic_parameters import kinetic_parameter


class ZeroNotSetError(Exception):
    """Raised if no value for the timestamp 0 is provided."""


class DictBasedKineticParameter(kinetic_parameter.KineticParameter):
    """A kinetic parameter which value depends on the timestamp and given by a dict.

    Missing value will be interpolated by using the last known value.

    Attributes:
        values: A dictionary mapping the timestamp to the value
            of the kinetic parameter.
    """

    def __init__(self, values: dict[float, float]):
        """Initializes a dict based kinetic parameter.

        Args:
            values: A dict mapping the timestamp to the value of the kinetic parameter.

        Raises:
            ZeroNotSetError: If no value for the timestamp 0 is provided.
        """
        if 0 not in values:
            raise ZeroNotSetError()
        self.values = pd.Series(values)

    def prepare_samples(self, n: int, max_t: int) -> None:
        """Prepares a sample of the kinetic parameter.

        This method is called before a new simulation starts.

        Args:
            n: The number of samples to prepare.
            max_t: The maximum timestamp of the simulation.
        """

    def get_at_timestamp(self, run: int, t: float) -> float:
        """Returns the kinetic parameters at the given timestamp.

        Args:
            t: The timestamp, at which the kinetic parameters are needed.
            run: The run (time series) of the current simulation.

        Returns:
            The kinetic parameters at the given timestamp.
        """
        return self.values[self.values.index <= t].iloc[-1]
