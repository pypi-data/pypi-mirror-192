"""Defines a kinetic parameter, that is constant over time."""
import typing

from simba_ml.simulation.kinetic_parameters import kinetic_parameter
from simba_ml.simulation.distributions import distribution as distribution_module


class ConstantKineticParameter(kinetic_parameter.KineticParameter):
    """A constant kinetic parameter.

    Attributes:
        samples: The kinetic parameters for each run (time series)
            of the current simulation.
        distribution: The distribution for possible values of the kinetic parameter.
    """

    samples: typing.Optional[list[float]] = None

    def __init__(self, distribution: distribution_module.Distribution):
        """Initializes a constant kinetic parameter.

        Args:
            distribution: The distribution for possible values of the kinetic parameter.
        """
        self.distribution = distribution

    def prepare_samples(self, n: int, max_t: int) -> None:
        """Prepares a sample of the kinetic parameter.

        This method is called before a new simulation starts.

        Args:
            n: The number of samples to prepare.
            max_t: The maximum timestamp of the simulation.
        """
        self.samples = self.distribution.get_samples_from_hypercube(n)

    def get_at_timestamp(self, run: int, t: float) -> float:
        """Returns the kinetic parameters at the given timestamp.

        Args:
            t: The timestamp, at which the kinetic parameters are needed.
            run: The run (time series) of the current simulation.

        Returns:
            The kinetic parameters at the given timestamp.

        Raises:
            RuntimeError: If the the samples have not been prepared.
                Preparation is done by calling the method `prepare_samples`.
        """
        if self.samples is None:
            raise RuntimeError("The samples have not been prepared.")
        if run >= len(self.samples):
            raise RuntimeError("The run index is too large.")
        return self.samples[run]
