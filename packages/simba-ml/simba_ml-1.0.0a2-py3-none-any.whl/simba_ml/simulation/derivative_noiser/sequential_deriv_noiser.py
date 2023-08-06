"""Provides the `SequentialDerivNoiser`."""

import typing

from simba_ml.simulation.derivative_noiser import derivative_noiser


class SequentialDerivNoiser(derivative_noiser.DerivNoiser):
    """The `SequentialNoiser` applies multiple given `DerivNoiser` sequentially.

    Attributes:
        noisers: A list of `DerivNoiser` to be applied.
    """

    def __init__(self, noisers: list[derivative_noiser.DerivNoiser]):
        """Inits `SequentialNoiser` with the provided arguments.

        Args:
            noisers: A list of `DerivNoiser` to be applied.
        """
        self.noisers = noisers

    def noisify(
        self,
        deriv: typing.Callable[
            [float, list[float], dict[str, float]], tuple[float, ...]
        ],
        max_t: float,
    ) -> typing.Callable[[float, list[float], dict[str, float]], tuple[float, ...]]:
        """Applies noise to the provided derivative function.

        Args:
            deriv: Derivative function.
            max_t: Adds noise up to this timestep.

        Returns:
            Noised derivative function.
        """
        for noiser in self.noisers:
            deriv = noiser.noisify(deriv, max_t)
        return deriv
