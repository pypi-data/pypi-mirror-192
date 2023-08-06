"""Web color tools."""

from ._color.core import (
    Color, is_hex_str, is_hsl_function_str, is_keyword_str,
    is_rgb_function_str, keyword_strs)
from ._compositing import alpha_composite
from ._contrast import contrast_ratio, relative_luminance
from ._version import __version__  # noqa: F401


__all__ = [
    "alpha_composite", "Color", "contrast_ratio", "is_hex_str",
    "is_hsl_function_str", "is_keyword_str", "is_rgb_function_str",
    "keyword_strs", "relative_luminance"]
