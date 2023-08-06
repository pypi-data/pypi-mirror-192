from __future__ import annotations

from typing import cast

from ._color.core import Color


def contrast_ratio(color1: Color, color2: Color) -> float:
    """Calculate the contrast ratio of two colors.

    Parameters
    ----------
    color1 : wclr.Color
        Color.
    color2 : wclr.Color
        Another color.

    Returns
    -------
    float
        Contrast ratio. In the range [1, 21] for colors in the sRGB gamut.

    Raises
    ------
    ValueError
        If a color is not fully opaque.

    Notes
    -----
    The definition can be found in Sec. 6 of Ref. [1]_.

    The order of arguments does not affect the returned value.

    References
    ----------
    .. [1] A. Kirkpatrick, J. O. Connor, A. Campbell, and M. Cooper, `Web
       Content Accessibility Guidelines (WCAG) 2.1
       <https://www.w3.org/TR/WCAG21/>`_, W3C Recommendation, 2018.
    """
    rl1 = relative_luminance(color1)
    rl2 = relative_luminance(color2)
    if rl1 < rl2:
        rl1, rl2 = rl2, rl1

    return (rl1+0.05) / (rl2+0.05)


def relative_luminance(color: Color) -> float:
    """Calculate the relative luminance of a color.

    Parameters
    ----------
    color : wclr.Color
        Color of which relative luminance is calculated.

    Returns
    -------
    float
        Relative luminance. Zero for sRGB black and one for sRGB white.

    Raises
    ------
    ValueError
        If a color is not fully opaque.

    Notes
    -----
    The definition can be found in Sec. 6 of Ref. [1]_.

    References
    ----------
    .. [1] A. Kirkpatrick, J. O. Connor, A. Campbell, and M. Cooper, `Web
       Content Accessibility Guidelines (WCAG) 2.1
       <https://www.w3.org/TR/WCAG21/>`_, W3C Recommendation, 2018.
    """
    rgba = color.to_srgb_tuple()
    rgb, alpha = rgba[:3], rgba[3]

    if alpha != 1:
        raise ValueError("alpha component must be 1")

    # to linear-light sRGB
    rgb = tuple(
        c / 12.92 if c <= 0.03928 else cast(float, ((c+0.055)/1.055) ** 2.4)
        for c in rgb)

    return 0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2]
