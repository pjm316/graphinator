"""Parametric graphing: x(t), y(t) curve pairs."""

from io import BytesIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sympy import SympifyError

from shared import (
    T,
    LS_MAP,
    PIXELS_PER_INCH,
    real_values,
    normalize_step,
    configure_axes,
    plot_point,
)

DEFAULT_T_MAX = 2 * np.pi


def plot_parametric_equation(ax, eq, line_width):
    x_expr = str(eq.get("x_expr", "cos(t)")).strip()
    y_expr = str(eq.get("y_expr", "sin(t)")).strip()
    if not x_expr or not y_expr:
        return None
    try:
        t_min = float(eq.get("t_min", 0.0))
        t_max = float(eq.get("t_max", DEFAULT_T_MAX))
        t_vals = np.linspace(t_min, t_max, 3000)
        with np.errstate(divide="ignore", invalid="ignore"):
            x_vals = real_values(x_expr, T, t_vals)
            y_vals = real_values(y_expr, T, t_vals)
        ax.plot(
            x_vals,
            y_vals,
            color=eq["color"],
            linewidth=line_width,
            linestyle=LS_MAP[eq["style"]],
        )
    except (
        TypeError,
        ValueError,
        SyntaxError,
        ZeroDivisionError,
        OverflowError,
        SympifyError,
    ):
        return f"Could not plot `x={x_expr}`, `y={y_expr}`. Check the expressions."
    return None


def render_parametric_plot(settings):
    x0, x1 = settings["x0"], settings["x1"]
    y0, y1 = settings["y0"], settings["y1"]
    plot_x_step, x_warnings = normalize_step(x0, x1, settings["x_step"], "xStep")
    plot_y_step, y_warnings = normalize_step(y0, y1, settings["y_step"], "yStep")
    width_in = settings["width"] / PIXELS_PER_INCH
    height_in = settings["height"] / PIXELS_PER_INCH
    fig, ax = plt.subplots(
        figsize=(width_in, height_in), dpi=PIXELS_PER_INCH, layout="constrained"
    )
    warnings = x_warnings + y_warnings
    for eq in settings.get("equations", []):
        w = plot_parametric_equation(ax, eq, settings["line_width"])
        if w:
            warnings.append(w)
    for pt in settings.get("points", []):
        plot_point(ax, pt, settings["line_width"])
    configure_axes(ax, settings, (plot_x_step, plot_y_step))
    return fig, warnings


def render_parametric(settings):
    """Pyodide entry point: settings dict -> {svg, warnings} or {error}."""
    try:
        fig, warnings = render_parametric_plot(settings)
        buf = BytesIO()
        fig.savefig(buf, format="svg")
        plt.close(fig)
        return {"svg": buf.getvalue().decode(), "warnings": warnings}
    except Exception as exc:
        return {"error": str(exc)}
