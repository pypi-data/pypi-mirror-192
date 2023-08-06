"""Provides the `NoDerivNoiser`."""

import typing

from simba_ml.simulation.derivative_noiser import derivative_noiser


class NoDerivNoiser(derivative_noiser.DerivNoiser):
    """The NoDerivNoiser is a dummy `DerivNoiser`, that applies no noise."""

    def noisify(
        self,
        deriv: typing.Callable[
            [float, list[float], dict[str, float]], tuple[float, ...]
        ],
        _max_t: float,
    ) -> typing.Callable[[float, list[float], dict[str, float]], tuple[float, ...]]:
        """Returns the input signal.

        Args:
            deriv: Derivative function.

        Returns:
            Not noised derivative function.
        """
        return deriv
