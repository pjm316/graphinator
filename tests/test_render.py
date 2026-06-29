import matplotlib.pyplot as plt
import numpy as np

from cartesian import plot_cartesian_equation, plot_point
from number_line import parse_nl
from number_line_draw import (
    _number_line_row_spacing,
    _number_line_y_limits,
    _draw_number_line_ray,
    _draw_number_line_segment,
    SKIP_COLOR,
    _skip_count_arc_path,
    _skip_count_label_y,
    _skip_count_segments,
)
from shared import _axis_arrow_style, real_values, refine_domain_boundaries, X


def test_plot_cartesian_equation_fills_above_and_below():
    x_values = np.linspace(-1.0, 1.0, 5)
    for ineq in ["y >", "y <"]:
        _, ax = plt.subplots()
        eq = {"expr": "x", "color": "black", "style": "solid", "ineq": ineq}
        warning = plot_cartesian_equation(ax, eq, x_values, (-2.0, 2.0), line_width=1.0)
        assert warning is None
        assert len(ax.collections) == 1


def test_plot_cartesian_equation_accepts_reversed_interval():
    _, ax = plt.subplots()
    eq = {
        "expr": "x",
        "color": "black",
        "style": "solid",
        "ineq": "none",
        "x_min": 0.5,
        "x_max": -0.5,
    }
    warning = plot_cartesian_equation(
        ax, eq, np.linspace(-1.0, 1.0, 9), (-1.0, 1.0), line_width=1.0
    )
    assert warning is None
    assert min(ax.lines[0].get_xdata()) >= -0.5
    assert max(ax.lines[0].get_xdata()) <= 0.5


def test_refine_domain_boundaries_handles_shifted_log_boundary_inside_window():
    x_vals = np.linspace(-100.0, 100.0, 4000)
    y_vals = real_values("log(x-10)+90", X, x_vals)

    refined_x, refined_y, anchor_mask = refine_domain_boundaries(
        "log(x-10)+90",
        X,
        x_vals,
        y_vals,
        y_bounds=(-100.0, 100.0),
    )

    anchor_indices = np.flatnonzero(anchor_mask)
    assert len(anchor_indices) == 1
    anchor_index = anchor_indices[0]
    assert refined_x[anchor_index] > 10.0
    assert refined_x[anchor_index] - 10.0 < 1e-12
    assert refined_y[anchor_index] < -100.0


def test_skip_counting_increases_stacked_number_line_row_spacing():
    assert _skip_count_label_y(0.0) < _number_line_row_spacing(
        {"show_skip_counting": True}
    )


def test_normal_number_line_keeps_original_vertical_framing():
    assert _number_line_y_limits(
        [{}], {"show_skip_counting": False}, row_spacing=1.0
    ) == (-0.8, 1.2)


def test_single_skip_count_number_line_keeps_original_vertical_framing():
    assert _number_line_y_limits(
        [{}], {"show_skip_counting": True}, row_spacing=1.35
    ) == (-0.8, 1.2)


def test_skip_count_segments_include_arc_straddling_left_boundary():
    settings = {"x0": 1.0, "x1": 7.0, "skip_start": 0.0, "skip_step": 2.0}
    assert list(_skip_count_segments(settings)) == [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0)]


def test_skip_count_labels_are_above_controlled_arc_peak():
    path = _skip_count_arc_path(0.0, 100.0, y=0.0)
    assert _skip_count_label_y(0.0) > max(vertex[1] for vertex in path.vertices)


def test_graph_real_values_supports_absolute_value_notation():
    values = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    result = real_values("|x|", X, values)
    assert np.allclose(result, np.array([2.0, 1.0, 0.0, 1.0, 2.0]))


def test_graph_real_values_uses_real_cube_root_for_negative_inputs():
    values = np.array([-8.0, -1.0, 0.0, 1.0, 8.0])
    result = real_values("x^(1/3)", X, values)
    assert np.allclose(result, np.array([-2.0, -1.0, 0.0, 1.0, 2.0]))


def test_graph_real_values_uses_real_odd_root_for_fractional_powers():
    values = np.array([-8.0, -1.0, 0.0, 1.0, 8.0])
    result = real_values("x^(2/3)", X, values)
    assert np.allclose(result, np.array([4.0, 1.0, 0.0, 1.0, 4.0]))


def test_axis_arrow_style_omits_origin_boundary_arrowheads():
    assert _axis_arrow_style(-1.0, 1.0) == "<|-|>"
    assert _axis_arrow_style(0.0, 1.0) == "-|>"
    assert _axis_arrow_style(-1.0, 0.0) == "<|-"
    assert _axis_arrow_style(0.0, 0.0) is None


def test_plot_point_renders_circle_but_respects_fill_state():
    _, ax = plt.subplots()
    point = {
        "x": 0,
        "y": 0,
        "color": "black",
        "marker": "square",
        "size": 8,
        "filled": False,
    }
    plot_point(ax, point, line_width=1.0)
    assert ax.lines[0].get_marker() == "o"
    assert ax.lines[0].get_markerfacecolor() == "white"


def test_plot_point_can_still_render_optional_label():
    _, ax = plt.subplots()
    point = {
        "x": 1,
        "y": 2,
        "color": "black",
        "size": 8,
        "label": "A",
        "label_dx": 4,
        "label_dy": 5,
    }
    plot_point(ax, point, line_width=1.0)
    assert ax.lines[0].get_marker() == "o"
    assert ax.texts[0].get_text() == "A"


def test_number_line_ray_and_segment_helpers_draw_markers():
    _, ax = plt.subplots()
    settings = {"line_width": 1.0}
    _draw_number_line_ray(
        ax,
        {"color": "black"},
        {"bound": (1.0, True), "direction": "right"},
        -5.0,
        5.0,
        settings,
        y=0,
        tip_ray=0.1,
    )
    _draw_number_line_segment(
        ax,
        {"color": "black"},
        (-2.0, False),
        (2.0, True),
        y=1,
        settings=settings,
    )
    assert len(ax.lines) >= 5


def test_parse_number_line_reversed_compound_inequality():
    assert parse_nl("5 >= x > 1") == {
        "type": "segment",
        "left": (1.0, False),
        "right": (5.0, True),
    }
