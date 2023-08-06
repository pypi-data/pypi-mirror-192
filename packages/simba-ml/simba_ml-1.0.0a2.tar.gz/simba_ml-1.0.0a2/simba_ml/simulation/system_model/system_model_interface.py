"""Provides the interface for a `PredictionTask`."""


import typing

import pandas as pd

from simba_ml.simulation import species


@typing.runtime_checkable
class SystemModelInterface(typing.Protocol):
    """Defines the interface for a `PredictionTask`."""

    @property
    def deriv(
        self,
    ) -> typing.Callable[[float, list[float], dict[str, float]], tuple[float, ...]]:
        """Returns the deriv."""

    @property
    def specieses(self) -> dict[str, species.Species]:
        """Returns the specieses."""

    @property
    def name(self) -> str:
        """Returns the name."""

    @property
    def kinetic_parameters(self) -> typing.Dict[str, typing.Any]:
        """Returns the kinetic_parameters."""

    def apply_noisifier(self, signal: pd.DataFrame) -> pd.DataFrame:
        """Applies the objects noisifier to a signal.

        Args:
            signal: (pd.DataFrame) The signal.
        """

    def apply_sparsifier(self, signal: pd.DataFrame) -> pd.DataFrame:
        """Applies the objects sparsifier to a signal.

        Args:
            signal: (pd.DataFrame) The signal.
        """

    def get_clean_signal(
        self,
        start_values: dict[str, typing.Any],
        sample_id: int,
        deriv_noised: bool = True,
    ) -> pd.DataFrame:
        """Creates a clean signal.

        Args:
            start_values: Start values for the simulation.
            sample_id: The id of the sample.
            deriv_noised: Whether the derivative is noised.
        """

    def sample_start_values_from_hypercube(self, n: int) -> dict[str, typing.Any]:
        """Creates a config dict.

        Args:
            n: Number of samples.
        """
