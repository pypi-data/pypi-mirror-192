import hypothesis.strategies
import pytest

from wclr._compositing import alpha_composite


@hypothesis.given(
    pytest.helpers.wclr.colors(min_alpha=1, max_alpha=1),
    pytest.helpers.wclr.colors(),
    hypothesis.strategies.sampled_from(["sRGB", "linearRGB"]))
def test_alpha_composite_fully_opaque(
        element_color, canvas_color, interpolation):
    color = alpha_composite(
        element_color, canvas_color, interpolation=interpolation)
    actual = color.to_srgb_tuple()
    desired = element_color.to_srgb_tuple()

    assert actual == pytest.approx(desired)


@hypothesis.given(
    pytest.helpers.wclr.colors(min_alpha=0, max_alpha=0),
    pytest.helpers.wclr.colors(),
    hypothesis.strategies.sampled_from(["sRGB", "linearRGB"]))
def test_alpha_composite_fully_transparent(
        element_color, canvas_color, interpolation):
    color = alpha_composite(
        element_color, canvas_color, interpolation=interpolation)
    actual = color.to_srgb_tuple()
    desired = canvas_color.to_srgb_tuple()

    assert actual == pytest.approx(desired)
