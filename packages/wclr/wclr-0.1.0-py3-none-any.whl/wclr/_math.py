from __future__ import annotations

import fractions
import math

from ._typing import FractionLike


def clamp(
    value: FractionLike,
    lower_bound: FractionLike,
    upper_bound: FractionLike
) -> fractions.Fraction:
    """Restrict a value to a specified range.

    Parameters
    ----------
    value : fraction-like
        Value to be restricted.
    lower_bound : fraction-like
        Lower bound.
    upper_bound : fraction-like
        Upper bound.

    Returns
    -------
    fractions.Fraction
        Value in the range.
    """
    value = fractions.Fraction(value)
    lower_bound = fractions.Fraction(lower_bound)
    upper_bound = fractions.Fraction(upper_bound)

    if upper_bound < lower_bound:
        raise ValueError("`upper_bound` must be >= `lower_bound`")

    return min(max(lower_bound, value), upper_bound)


def round_half_up(
    value: FractionLike,
    n_digits: int = 0
) -> fractions.Fraction:
    """Round a number with the round-half-up rule.

    Parameters
    ----------
    value : fraction-like
        Number to be rounded.
    n_digits : int, optional
        Decimal places to which a number is rounded.

    Returns
    -------
    fractions.Fraction
        Rounded number.
    """
    value = fractions.Fraction(value)

    scale = fractions.Fraction(10) ** n_digits

    return math.floor(scale*value+fractions.Fraction(1, 2)) / scale
