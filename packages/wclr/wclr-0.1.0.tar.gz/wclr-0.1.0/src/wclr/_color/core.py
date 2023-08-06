from __future__ import annotations

import fractions

from .string import (
    HSL_FUNCTION_PATTERN, HSLA_FUNCTION_PATTERN, INTEGER_RGB_FUNCTION_PATTERN,
    INTEGER_RGBA_FUNCTION_PATTERN, KEYWORD_RGBS,
    PERCENTAGE_RGB_FUNCTION_PATTERN, PERCENTAGE_RGBA_FUNCTION_PATTERN,
    SIX_DIGIT_HEX_PATTERN, THREE_DIGIT_HEX_PATTERN)
from .utils import hsl_to_srgb, srgb_to_hsl, to_number_str
from .._math import clamp, round_half_up
from .._typing import FourTupleColor, FractionLike, Iterator


class Color:
    """Color object.

    Parameters
    ----------
    r : fraction-like
        Red component of sRGB color space. In the range [0, 1] for an in-gamut
        color.
    g : fraction-like
        Green component of sRGB color space. In the range [0, 1] for an in-
        gamut color.
    b : fraction-like
        Blue component of sRGB color space. In the range [0, 1] for an in-gamut
        color.
    alpha : fraction-like, optional
        Alpha component. Must be in the range [0, 1].
    """

    def __init__(
        self,
        r: FractionLike,
        g: FractionLike,
        b: FractionLike,
        alpha: FractionLike = 1
    ) -> None:
        r = fractions.Fraction(r)
        g = fractions.Fraction(g)
        b = fractions.Fraction(b)
        alpha = fractions.Fraction(alpha)

        if not 0 <= alpha <= 1:
            raise ValueError("`alpha` must be in the range [0, 1]")

        self._srgb = (r, g, b)
        self._alpha = alpha

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented

        return self._srgb == other._srgb and self._alpha == other._alpha

    def __hash__(self) -> int:
        return hash(self._srgb + (self._alpha,))

    def __repr__(self) -> str:
        return "<{}: ({}, {}, {}) in sRGB, alpha={}>".format(
            self.__class__.__name__, *self._srgb, self._alpha)

    @classmethod
    def from_str(cls, value: str) -> Color:
        """Construct an instance from a CSS color.

        Parameters
        ----------
        value : str
            Value of the CSS color property.

        Returns
        -------
        wclr.Color
            Color instance.

        Notes
        -----
        Values specified in Ref. [1]_ are valid except for the 'inherit'
        keyword, 'currentColor' keyword, and CSS2 system colors.

        References
        ----------
        .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
           <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
        """
        if match := THREE_DIGIT_HEX_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(int(match[1] * 2, base=16), 255),
                fractions.Fraction(int(match[2] * 2, base=16), 255),
                fractions.Fraction(int(match[3] * 2, base=16), 255))
        elif match := SIX_DIGIT_HEX_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(int(match[1], base=16), 255),
                fractions.Fraction(int(match[2], base=16), 255),
                fractions.Fraction(int(match[3], base=16), 255))
        elif match := INTEGER_RGB_FUNCTION_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(match[1]) / 255,
                fractions.Fraction(match[2]) / 255,
                fractions.Fraction(match[3]) / 255)
        elif match := PERCENTAGE_RGB_FUNCTION_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(match[1][:-1]) / 100,
                fractions.Fraction(match[2][:-1]) / 100,
                fractions.Fraction(match[3][:-1]) / 100)
        elif match := INTEGER_RGBA_FUNCTION_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(match[1]) / 255,
                fractions.Fraction(match[2]) / 255,
                fractions.Fraction(match[3]) / 255,
                alpha=clamp(match[4], 0, 1))
        elif match := PERCENTAGE_RGBA_FUNCTION_PATTERN.fullmatch(value):
            return cls(
                fractions.Fraction(match[1][:-1]) / 100,
                fractions.Fraction(match[2][:-1]) / 100,
                fractions.Fraction(match[3][:-1]) / 100,
                alpha=clamp(match[4], 0, 1))
        elif match := HSL_FUNCTION_PATTERN.fullmatch(value):
            hue = fractions.Fraction(match[1]) / 360
            saturation = clamp(match[2][:-1], 0, 100) / 100
            lightness = clamp(match[3][:-1], 0, 100) / 100
            rgb = hsl_to_srgb(hue, saturation, lightness)
            return cls(*rgb)
        elif match := HSLA_FUNCTION_PATTERN.fullmatch(value):
            hue = fractions.Fraction(match[1]) / 360
            saturation = clamp(match[2][:-1], 0, 100) / 100
            lightness = clamp(match[3][:-1], 0, 100) / 100
            alpha = clamp(match[4], 0, 1)
            rgb = hsl_to_srgb(hue, saturation, lightness)
            return cls(*rgb, alpha=alpha)

        if value == "transparent":
            return cls(0, 0, 0, alpha=0)

        key = value.lower()
        if key in KEYWORD_RGBS:
            return cls(*KEYWORD_RGBS[key])

        raise ValueError(f"invalid notation: {value}")

    @classmethod
    def from_hsl(
        cls,
        hue: FractionLike,
        saturation: FractionLike,
        lightness: FractionLike,
        alpha: FractionLike = 1
    ) -> Color:
        """Construct an instance from components of the HSL color space.

        Parameters
        ----------
        hue : fraction-like
            Hue. The period is one.
        saturation : fraction-like
            Saturation. Must be in the range [0, 1].
        lightness : fraction-like
            lightness. Must be in the range [0, 1].
        alpha : fraction-like, optional
            Alpha component. Must be in the range [0, 1].

        Returns
        -------
        wclr.Color
            Color instance.
        """
        hue = fractions.Fraction(hue)
        saturation = fractions.Fraction(saturation)
        lightness = fractions.Fraction(lightness)
        alpha = fractions.Fraction(alpha)

        if not 0 <= saturation <= 1:
            raise ValueError("`saturation` must be in the range [0, 1]")
        if not 0 <= lightness <= 1:
            raise ValueError("`lightness` must be in the range [0, 1]")
        if not 0 <= alpha <= 1:
            raise ValueError("`alpha` must be in the range [0, 1]")

        rgb = hsl_to_srgb(hue, saturation, lightness)

        return cls(*rgb, alpha=alpha)

    def to_hex_str(self, force_six_digit: bool = False) -> str:
        """Convert an instance into a CSS hex color.

        Parameters
        ----------
        force_six_digit : bool, optional
            If ``True``, the six-digit hexadecimal notation is always used.
            Otherwise, the three-digit hexadecimal notation is used if
            available.

        Returns
        -------
        str
            Hex color.

        Raises
        ------
        ValueError
            If a color is not in the sRGB gamut. If an alpha component is not
            one.

        Notes
        -----
        The notation can be found in Sec. 4.2.1 of Ref. [1]_.

        Components are rounded to integers.

        References
        ----------
        .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
           <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
        """
        if not all(0 <= c <= 1 for c in self._srgb):
            raise ValueError("sRGB components must be in the range [0, 1]")
        if self._alpha != 1:
            raise ValueError("alpha component must be 1")

        rgb = tuple(int(round_half_up(255 * c)) for c in self._srgb)
        if not force_six_digit and all(c % 17 == 0 for c in rgb):
            fields = tuple(f"{c//17:x}" for c in rgb)
        else:
            fields = tuple(f"{c:02x}" for c in rgb)

        return "#{}{}{}".format(*fields)

    def to_rgb_function_str(
        self,
        percentage: bool = True,
        force_rgba: bool = False,
        n_digits: int = 6
    ) -> str:
        """Convert an instance into a CSS RGB function color.

        Parameters
        ----------
        percentage : bool, optional
            If ``True``, red, green, and blue components are formatted in
            percentages. Otherwise, they are formatted in integers.
        force_rgba : bool, optional
            If ``True``, the RGBA function notation is always used. Otherwise,
            the notation is used only for a not-fully-opaque color.
        n_digits : int, optional
            Decimal places to which repeating decimals are rounded.

        Returns
        -------
        str
            RGB function color.

        Notes
        -----
        The notation can be found in Sec. 4.2.1 and 4.2.2 of Ref. [1]_.

        If the `percentage` argument is ``False``, components are rounded to
        integers.

        References
        ----------
        .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
           <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
        """
        if percentage:
            fields = [
                to_number_str(100 * c, n_digits=n_digits) + "%"
                for c in self._srgb]
        else:
            fields = [str(round_half_up(255 * c)) for c in self._srgb]

        if not force_rgba and self._alpha == 1:
            prefix = "rgb"
        else:
            prefix = "rgba"
            fields.append(to_number_str(self._alpha, n_digits=n_digits))

        return "{}({})".format(prefix, ",".join(fields))

    def to_hsl_function_str(
        self,
        force_hsla: bool = False,
        n_digits: int = 6
    ) -> str:
        """Convert an instance into a CSS HSL function color.

        Parameters
        ----------
        force_hsla : bool, optional
            If ``True``, the HSLA function notation is always used. Otherwise,
            the notation is used only for a not-fully-opaque color.
        n_digits : int, optional
            Decimal places to which repeating decimals are rounded.

        Returns
        -------
        str
            HSL function color.

        Notes
        -----
        The notation can be found in Sec. 4.2.4 and 4.2.5 of Ref. [1]_.

        References
        ----------
        .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
           <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
        """
        hue, saturation, lightness = srgb_to_hsl(*self._srgb)
        fields = [
            to_number_str(360 * hue, n_digits=n_digits),
            to_number_str(100 * saturation, n_digits=n_digits) + "%",
            to_number_str(100 * lightness, n_digits=n_digits) + "%"]

        if not force_hsla and self._alpha == 1:
            prefix = "hsl"
        else:
            prefix = "hsla"
            fields.append(to_number_str(self._alpha, n_digits=n_digits))

        return "{}({})".format(prefix, ",".join(fields))

    def to_srgb_tuple(self) -> FourTupleColor:
        """Convert an instance into components of the sRGB color space.

        Returns
        -------
        tuple of fractions.Fraction
            Red, green, blue, and alpha components. Red, green, and blue
            components are in the range [0, 1] for an in-gamut color. An alpha
            component is in the range [0, 1].
        """
        return self._srgb + (self._alpha,)

    def to_hsl_tuple(self) -> FourTupleColor:
        """Convert an instance into components of the HSL color space.

        Returns
        -------
        tuple of fractions.Fraction
            Hue, saturation, lightness, and alpha components. A hue is in the
            range [0, 1). Saturation and lightness are in the range [0, 1] for
            an in-gamut color. An alpha component is in the range [0, 1].

        Notes
        -----
        If a saturation is zero, a hue is zero. If a lightness is zero or one,
        a saturation is zero.
        """
        hsl = srgb_to_hsl(*self._srgb)

        return hsl + (self._alpha,)


def keyword_strs() -> Iterator[str]:
    """Get CSS keyword colors.

    Yields
    ------
    str
        CSS keyword color in lower case.
    """
    yield from KEYWORD_RGBS


def is_hex_str(
    obj: object,
    allow_three_digit: bool = True,
    allow_six_digit: bool = True
) -> bool:
    """Check if an object is a CSS hex color.

    Parameters
    ----------
    obj
        Object to be checked.
    allow_three_digit : bool, optional
        If ``True``, the three-digit notation is valid.
    allow_six_digit : bool, optional
        If ``True``, the six-digit notation is valid.

    Returns
    -------
    bool
        ``True`` if an object is a ``str`` instance of a CSS hex color.

    Notes
    -----
    The notation can be found in Sec. 4.2.1 of Ref. [1]_.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    """
    if not isinstance(obj, str):
        return False

    return bool(
        (allow_three_digit and THREE_DIGIT_HEX_PATTERN.fullmatch(obj))
        or (allow_six_digit and SIX_DIGIT_HEX_PATTERN.fullmatch(obj)))


def is_rgb_function_str(
    obj: object,
    allow_rgb: bool = True,
    allow_rgba: bool = True,
    allow_integer: bool = True,
    allow_percentage: bool = True
) -> bool:
    """Check if an object is a CSS RGB function color.

    Parameters
    ----------
    obj
        Object to be checked.
    allow_rgb : bool, optional
        If ``True``, the RGB function notation is valid.
    allow_rgba : bool, optional
        If ``True``, the RGBA function notation is valid.
    allow_integer : bool, optional
        If ``True``, the integer notation is valid for red, green, and blue
        components.
    allow_percentage : bool, optional
        If ``True``, the percentage notation is valid for red, green, and blue
        components.

    Returns
    -------
    bool
        ``True`` if an object is a ``str`` instance of a CSS RGB function
        color.

    Notes
    -----
    The notation can be found in Sec. 4.2.1 and 4.2.2 of Ref. [1]_.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    """
    if not isinstance(obj, str):
        return False

    return bool(
        (allow_rgb
         and allow_integer
         and INTEGER_RGB_FUNCTION_PATTERN.fullmatch(obj))
        or (allow_rgb
            and allow_percentage
            and PERCENTAGE_RGB_FUNCTION_PATTERN.fullmatch(obj))
        or (allow_rgba
            and allow_integer
            and INTEGER_RGBA_FUNCTION_PATTERN.fullmatch(obj))
        or (allow_rgba
            and allow_percentage
            and PERCENTAGE_RGBA_FUNCTION_PATTERN.fullmatch(obj)))


def is_hsl_function_str(
    obj: object,
    allow_hsl: bool = True,
    allow_hsla: bool = True
) -> bool:
    """Check if an object is a CSS HSL function color.

    Parameters
    ----------
    obj
        Object to be checked.
    allow_hsl : bool, optional
        If ``True``, the HSL function notation is valid.
    allow_hsla : bool, optional
        If ``True``, the HSLA function notation is valid.

    Returns
    -------
    bool
        ``True`` if an object is a ``str`` instance of a CSS HSL function
        color.

    Notes
    -----
    The notation can be found in Sec. 4.2.4 and 4.2.5 of Ref. [1]_.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    """
    if not isinstance(obj, str):
        return False

    return bool(
        (allow_hsl and HSL_FUNCTION_PATTERN.fullmatch(obj))
        or (allow_hsla and HSLA_FUNCTION_PATTERN.fullmatch(obj)))


def is_keyword_str(obj: object) -> bool:
    """Check if an object is a CSS keyword color.

    Parameters
    ----------
    obj
        Object to be checked.

    Returns
    -------
    bool
        ``True`` if an object is a ``str`` instance of a CSS keyword color.

    Notes
    -----
    The keywords can be found in Sec. 4.3 of Ref. [1]_.

    References
    ----------
    .. [1] T. Çelik, C. Lilley, and D. Baron, `CSS Color Module Level 3
       <https://www.w3.org/TR/css-color-3/>`_, W3C Recommendation, 2011.
    """
    if not isinstance(obj, str):
        return False

    return obj.lower() in KEYWORD_RGBS
