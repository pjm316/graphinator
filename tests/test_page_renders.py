"""Targeted render tests for page-level plotting behavior."""

import math

import matplotlib.pyplot as plt
import numpy as np
import pytest

from cartesian import render_cartesian_plot
from polar import render_polar_plot, plot_polar_equation
from parametric import render_parametric_plot
from number_line import render_number_line_plot


def _cart_settings(**overrides):
    base = {
        "equations": [],
        "points": [],
        "x0": -5.0,
        "x1": 5.0,
        "y0": -5.0,
        "y1": 5.0,
        "x_step": 1.0,
        "y_step": 1.0,
        "x_minor": 0.5,
        "y_minor": 0.5,
        "width": 288.0,
        "height": 288.0,
        "line_width": 1.5,
        "show_grid": False,
        "show_minor_grid": False,
        "show_labels": False,
        "axis_arrows": False,
        "x_label": "",
        "y_label": "",
    }
    return {**base, **overrides}


def _pol_settings(**overrides):
    base = {
        "equations": [],
        "points": [],
        "r_max": 0.0,
        "theta_step": 30.0,
        "line_width": 1.5,
        "width": 288.0,
        "height": 288.0,
    }
    return {**base, **overrides}


def _nl_settings(**overrides):
    base = {
        "equations": [],
        "x0": -5.0,
        "x1": 5.0,
        "x_step": 1.0,
        "skip_start": 0.0,
        "skip_step": 2.0,
        "line_width": 1.5,
        "show_labels": True,
        "show_skip_counting": False,
        "width": 288.0,
        "height": 144.0,
    }
    return {**base, **overrides}


def test_cartesian_render_plots_expression():
    settings = _cart_settings(
        equations=[
            {
                "expr": "x^2",
                "color": "blue",
                "style": "solid",
                "ineq": "none",
                "x_min": -5.0,
                "x_max": 5.0,
            }
        ]
    )
    fig, warnings = render_cartesian_plot(settings)
    assert warnings == []
    plt.close(fig)


def test_cartesian_render_warns_for_invalid_expression():
    settings = _cart_settings(
        equations=[
            {
                "expr": "pizza(x)",
                "color": "blue",
                "style": "solid",
                "ineq": "none",
                "x_min": -5.0,
                "x_max": 5.0,
            }
        ]
    )
    _, warnings = render_cartesian_plot(settings)
    assert len(warnings) == 1 and "pizza" in warnings[0]


def test_cartesian_render_plots_inequality_fill():
    settings = _cart_settings(
        equations=[
            {
                "expr": "x",
                "color": "blue",
                "style": "solid",
                "ineq": "y >",
                "x_min": -5.0,
                "x_max": 5.0,
            }
        ]
    )
    fig, warnings = render_cartesian_plot(settings)
    assert warnings == []
    assert len(fig.axes[0].collections) >= 1
    plt.close(fig)


def test_parametric_render_plots_circle():
    settings = _cart_settings(
        equations=[
            {
                "x_expr": "cos(t)",
                "y_expr": "sin(t)",
                "t_min": 0.0,
                "t_max": 6.28,
                "color": "blue",
                "style": "solid",
            }
        ]
    )
    fig, warnings = render_parametric_plot(settings)
    assert warnings == []
    plt.close(fig)


def test_parametric_render_warns_for_invalid_expression():
    settings = _cart_settings(
        equations=[
            {
                "x_expr": "pizza(t)",
                "y_expr": "sin(t)",
                "t_min": 0.0,
                "t_max": 6.28,
                "color": "blue",
                "style": "solid",
            }
        ]
    )
    _, warnings = render_parametric_plot(settings)
    assert len(warnings) == 1


def test_polar_render_plots_rose():
    settings = _pol_settings(
        equations=[
            {
                "expr": "2*sin(3*theta)",
                "theta_min": 0.0,
                "theta_max": 360.0,
                "color": "blue",
                "style": "solid",
            }
        ]
    )
    fig, warnings = render_polar_plot(settings)
    assert warnings == []
    plt.close(fig)


def test_polar_render_warns_for_invalid_expression():
    settings = _pol_settings(
        equations=[
            {
                "expr": "pizza(theta)",
                "theta_min": 0.0,
                "theta_max": 360.0,
                "color": "blue",
                "style": "solid",
            }
        ]
    )
    _, warnings = render_polar_plot(settings)
    assert len(warnings) == 1


def test_polar_render_respects_r_max():
    settings = _pol_settings(
        r_max=2.0,
        equations=[
            {
                "expr": "1",
                "theta_min": 0.0,
                "theta_max": 360.0,
                "color": "blue",
                "style": "solid",
            }
        ],
    )
    fig, _ = render_polar_plot(settings)
    assert pytest.approx(fig.axes[0].get_rmax(), abs=0.01) == 2.0
    plt.close(fig)


def test_polar_negative_r_reflects_through_origin():
    plotted = []

    class FakeAx:
        def plot(self, theta, r, **kwargs):
            plotted.append((theta.copy(), r.copy()))

    eq = {
        "expr": "cos(4*theta)",
        "theta_min": 0.0,
        "theta_max": 360.0,
        "color": "blue",
        "style": "solid",
    }
    assert plot_polar_equation(FakeAx(), eq, line_width=1.5) is None
    theta_vals, r_vals = plotted[0]
    assert np.all(r_vals >= 0)
    assert np.any(theta_vals > 2 * math.pi)


def test_number_line_render_plots_ray():
    settings = _nl_settings(equations=[{"expr": "x > 0", "color": "blue"}])
    fig, warnings = render_number_line_plot(settings)
    assert warnings == []
    plt.close(fig)


def test_number_line_render_warns_for_invalid_inequality():
    settings = _nl_settings(equations=[{"expr": "pizza", "color": "blue"}])
    _, warnings = render_number_line_plot(settings)
    assert len(warnings) == 1 and "pizza" in warnings[0]


def test_skip_counting_render_draws_with_empty_equations():
    fig, warnings = render_number_line_plot(
        _nl_settings(show_skip_counting=True, equations=[])
    )
    assert warnings == []
    assert len(fig.axes[0].patches) > 0
    plt.close(fig)
