import contextlib

import hypothesis
import pytest

from wclr._color.core import Color
from wclr._contrast import contrast_ratio, relative_luminance


@pytest.mark.parametrize(
    ["color", "desired"],
    [(Color(0, 0, 0), 0), (Color(1, 1, 1), 1)])
def test_relative_luminance_extreme(color, desired):
    actual = relative_luminance(color)

    assert actual == pytest.approx(desired)


@hypothesis.given(pytest.helpers.wclr.colors())
def test_relative_luminance_alpha(color):
    _, _, _, alpha = color.to_srgb_tuple()
    context = (
        contextlib.nullcontext() if alpha == 1 else pytest.raises(ValueError))

    with context:
        relative_luminance(color)


@hypothesis.given(
    pytest.helpers.wclr.colors(min_alpha=1, max_alpha=1),
    pytest.helpers.wclr.colors(min_alpha=1, max_alpha=1))
def test_contrast_ratio_order(color1, color2):
    actual = contrast_ratio(color1, color2)
    desired = contrast_ratio(color2, color1)

    assert actual == desired


@hypothesis.given(
    pytest.helpers.wclr.colors(min_alpha=1, max_alpha=1),
    pytest.helpers.wclr.colors(min_alpha=1, max_alpha=1))
def test_contrast_ratio_range(color1, color2):
    actual = contrast_ratio(color1, color2)

    assert 1 <= actual <= 21


@hypothesis.given(
    pytest.helpers.wclr.colors(),
    pytest.helpers.wclr.colors())
def test_contrast_ratio_alpha(color1, color2):
    _, _, _, alpha1 = color1.to_srgb_tuple()
    _, _, _, alpha2 = color2.to_srgb_tuple()
    context = (
        contextlib.nullcontext() if alpha1 == alpha2 == 1
        else pytest.raises(ValueError))

    with context:
        contrast_ratio(color1, color2)
