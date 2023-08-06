from __future__ import annotations

import fractions
from typing import cast

from .._math import clamp, round_half_up
from .._typing import FractionLike, ThreeTupleColor


def hsl_to_srgb(
    hue: FractionLike,
    saturation: FractionLike,
    lightness: FractionLike
) -> ThreeTupleColor:
    """Convert a color from the HSL color space to the sRGB color space.

    Parameters
    ----------
    hue : fraction-like
        Hue. The period is one.
    saturation : fraction-like
        Saturation. Must be in the range [0, 1].
    lightness : fraction-like
        Lightness. Must be in the range [0, 1].

    Returns
    -------
    tuple of fractions.Fraction
        Red, green, and blue components. In the range [0, 1].

    Notes
    -----
    The formula can be found in Sec. 4.2.4 of Ref. [1]_.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    """
    hue = fractions.Fraction(hue)
    saturation = fractions.Fraction(saturation)
    lightness = fractions.Fraction(lightness)

    hue %= 1
    a = saturation * min(lightness, 1-lightness)

    rgb = []
    for n in [0, 8, 4]:
        k = (n+12*hue) % 12
        rgb.append(lightness - a*clamp(min(k-3, 9-k), -1, 1))
    rgb = cast(
        "tuple[fractions.Fraction, fractions.Fraction, fractions.Fraction]",
        tuple(rgb))

    return rgb


def srgb_to_hsl(
    r: FractionLike,
    g: FractionLike,
    b: FractionLike
) -> ThreeTupleColor:
    """Convert a color from the sRGB color space to the HSL color space.

    Parameters
    ----------
    r : fraction-like
        Red component. In the range [0, 1] for an in-gamut color.
    g : fraction-like
        Green component. In the range [0, 1] for an in-gamut color.
    b : fraction-like
        Blue component. In the range [0, 1] for an in-gamut color.

    Returns
    -------
    tuple of fractions.Fraction
        Hue, saturation, and lightness. A hue is in the range [0, 1).
        Saturation and lightness are in the range [0, 1] for an in-gamut color.

    Notes
    -----
    The formula can be found in Ref. [1]_. If a saturation is zero, a hue is
    zero. If a lightness is zero or one, a saturation is zero.

    References
    ----------
    .. [1] `HSL and HSV <https://en.wikipedia.org/wiki/HSL_and_HSV>`_,
       Wikipedia, accessed September 21, 2022.
    """
    r = fractions.Fraction(r)
    g = fractions.Fraction(g)
    b = fractions.Fraction(b)

    rgb_min = min(r, g, b)
    rgb_max = max(r, g, b)

    c = rgb_max - rgb_min
    if c:
        rgb = (r, g, b)
        argmax = sorted(enumerate(rgb), key=lambda item: item[1])[-1][0]
        hue = ((rgb[argmax-2]-rgb[argmax-1])/c+2*argmax) / 6
        hue %= 1
    else:
        hue = fractions.Fraction(0)

    lightness = (rgb_min+rgb_max) / 2
    saturation = (
        fractions.Fraction(0) if lightness == 0 or lightness == 1
        else (rgb_max-lightness) / min(lightness, 1-lightness))

    return (hue, saturation, lightness)


def to_number_str(value: FractionLike, n_digits: int = 6) -> str:
    """Convert a number into a CSS number.

    Parameters
    ----------
    value : fraction-like
        Number to be converted.
    n_digits : int, optional
        Decimal places to which a repeating decimal is rounded.

    Returns
    -------
    str
        CSS number.
    """
    value = fractions.Fraction(value)

    # factorize a denominator into divisors of 10 and others
    factor = value.denominator
    exponents = {2: 0, 5: 0}
    for prime in exponents:
        while not factor % prime:
            factor //= prime
            exponents[prime] += 1

    if factor == 1:
        # `value` is a terminating decimal
        n_digits = max(exponents.values())
    else:
        # `value` is a repeating decimal
        value = round_half_up(value, n_digits=n_digits)

    if n_digits <= 0:
        return str(value)

    s = f"{int(value*10**n_digits):0{n_digits+1}d}"
    s = f"{s[:-n_digits]}.{s[-n_digits:]}"

    return s
