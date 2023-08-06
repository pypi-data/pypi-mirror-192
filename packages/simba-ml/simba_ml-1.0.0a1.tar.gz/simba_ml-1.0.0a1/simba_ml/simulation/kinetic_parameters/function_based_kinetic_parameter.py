"""Defines a kinetic parameter, that is constant over time."""
import typing

from simba_ml.simulation.kinetic_parameters import kinetic_parameter


class FunctionBasedKineticParameter(kinetic_parameter.KineticParameter):
    """A kinetic parameter which values are based on a function.

    Attributes:
        function: A function mapping the timestamp to the value
            of the kinetic parameter.
    """

    def __init__(self, function: typing.Callable[[float], float]):
        """Initializes a function based kinetic parameter.

        Args:
            function: A function mapping the timestamp to the value
                of the kinetic parameter.
        """
        self.function = function

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
        return self.function(t)
