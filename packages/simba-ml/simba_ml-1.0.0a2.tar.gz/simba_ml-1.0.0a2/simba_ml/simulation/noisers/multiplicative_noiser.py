"""Defines the `MultiplicativeNoiser`."""


import pandas as pd

from simba_ml.simulation.noisers import noiser
from simba_ml.simulation import distributions


class MultiplicativeNoiser(noiser.Noiser):
    """Multiplies each element individually with a randomly generated number.

    The number is generated using a selected `Distribution`.

    Attributes:
        distribution: A distribution to generate random noise.
    """

    def __init__(self, distribution: distributions.Distribution) -> None:
        """Inits MultiplicativeNoiser with the provided params.

        Args:
            distribution: A distribution to generate random noise.
        """
        self.distribution = distribution

    def noisify(self, signal: pd.DataFrame) -> pd.DataFrame:
        """Applies noise to the provided signal.

        Args:
            signal: The input data.

        Returns:
            pd.DataFrame
        """
        noise = self.distribution.get_random_values(signal.shape)
        return signal.mul(noise)
