from __future__ import annotations

import fractions
from typing import Literal

from ._color.core import Color
from ._typing import ThreeTupleColor


def alpha_composite(
    element_color: Color,
    canvas_color: Color,
    interpolation: Literal["linearRGB", "sRGB"] = "sRGB"
) -> Color:
    """Perform the alpha compositing.

    Parameters
    ----------
    element_color : wclr.Color
        Color of an element stacked on a canvas.
    canvas_color : wclr.Color
        Color of a canvas.
    interpolation : {'linearRGB', 'sRGB'}, optional
        Color space where the compositing is performed. ``'linearRGB'`` is the
        linear-light sRGB color space and ``'sRGB'`` is the gamma-encoded sRGB
        color space.

    Returns
    -------
    wclr.Color
        Resulting color.

    Notes
    -----
    The specification can be found in Sec. 5 of Ref. [1]_. The formula can be
    found in Sec. 14.2 of Ref. [2]_.

    sRGB components of the resulting color are undefined for the case where
    both element color and canvas color are fully transparent, which are zero
    divided by zero. This function returns the canvas color for this case.

    Components of the returned color may not be exact due to the conversion
    from the floating-point number.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    .. [2] J. Ferraiolo, J. Fujisawa, and D. Jackson, `Scalable Vector Graphics
       (SVG) 1.1 Specification <https://www.w3.org/TR/SVG11/>`_, W3C
       Recommendation, 2003.
    """
    if interpolation not in {"sRGB", "linearRGB"}:
        raise ValueError("`interpolation` must be 'sRGB' or 'linearRGB'")

    element_rgba = element_color.to_srgb_tuple()
    element_rgb, element_alpha = element_rgba[:3], element_rgba[3]

    canvas_rgba = canvas_color.to_srgb_tuple()
    canvas_rgb, canvas_alpha = canvas_rgba[:3], canvas_rgba[3]

    if not element_alpha and not canvas_alpha:
        return Color(*canvas_rgba)

    if interpolation == "linearRGB":
        element_rgb = _srgb_to_linearrgb(element_rgb)
        canvas_rgb = _srgb_to_linearrgb(canvas_rgb)

    # to premuliplied values
    element_rgb = tuple(c * element_alpha for c in element_rgb)
    canvas_rgb = tuple(c * canvas_alpha for c in canvas_rgb)

    result_rgb = tuple(
        (1-element_alpha)*canvas_c + element_c
        for element_c, canvas_c in zip(element_rgb, canvas_rgb))
    result_alpha = 1 - (1-element_alpha)*(1-canvas_alpha)

    # to straight values
    result_rgb = tuple(c / result_alpha for c in result_rgb)

    if interpolation == "linearRGB":
        result_rgb = _linearrgb_to_srgb(result_rgb)  # type: ignore[arg-type]

    return Color(*result_rgb, alpha=result_alpha)  # type: ignore[misc]


def _srgb_to_linearrgb(rgb: ThreeTupleColor) -> ThreeTupleColor:
    """Convert gamma-encoded sRGB components into the linear-light space.

    Parameters
    ----------
    rgb : tuple of fractions.Fraction
        Gamma-encoded sRGB components. In the range [0, 1] for an in-gamut
        color.

    Returns
    -------
    tuple of fractions.Fraction
        Linear-light sRGB components. In the range [0, 1] for an in-gamut
        color.

    Notes
    -----
    The formula can be found in Sec. 11.7.1 of Ref. [1]_.

    The returned rational numbers may not be exact due to the conversion from
    the floating-point number.

    References
    ----------
    .. [1] J. Ferraiolo, J. Fujisawa, and D. Jackson, `Scalable Vector Graphics
       (SVG) 1.1 Specification <https://www.w3.org/TR/SVG11/>`_, W3C
       Recommendation, 2003.
    """
    return tuple(  # type: ignore[return-value]
        c / fractions.Fraction("12.92") if c <= fractions.Fraction("0.04045")
        else fractions.Fraction(
            ((c+fractions.Fraction("0.055"))/fractions.Fraction("1.055"))
            ** 2.4)
        for c in rgb)


def _linearrgb_to_srgb(rgb: ThreeTupleColor) -> ThreeTupleColor:
    """Convert linear-light sRGB components into the gamma-encoded space.

    Parameters
    ----------
    rgb : tuple of fractions.Fraction
        Linear-light sRGB components. In the range [0, 1] for an in-gamut
        color.

    Returns
    -------
    tuple of fractions.Fraction
        Gamma-encoded sRGB components. In the range [0, 1] for an in-gamut
        color.

    Notes
    -----
    The returned rational numbers may not be exact due to the conversion from
    the floating-point number.
    """
    return tuple(  # type: ignore[return-value]
        fractions.Fraction("12.92") * c
        if fractions.Fraction("12.92") * c <= fractions.Fraction("0.04045")
        else (fractions.Fraction("1.055")*fractions.Fraction(c**(1/2.4))
              - fractions.Fraction("0.055"))
        for c in rgb)
