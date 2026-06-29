"""Cartesian graphing: y = f(x) equations with inequality shading."""

from io import BytesIO

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sympy import SympifyError

from shared import (
    X,
    LS_MAP,
    PIXELS_PER_INCH,
    real_values,
    refine_domain_boundaries,
    normalize_step,
    configure_axes,
    plot_point,
)


def plot_cartesian_equation(ax, eq, x_vals, y_bounds, line_width):
    y0, y1 = y_bounds
    expr_text = str(eq.get("expr", "")).strip()
    if not expr_text:
        return None
    try:
        x_min = float(eq.get("x_min", x_vals[0]))
        x_max = float(eq.get("x_max", x_vals[-1]))
        if x_min > x_max:
            x_min, x_max = x_max, x_min
        x_vals = x_vals[(x_vals >= x_min) & (x_vals <= x_max)]
        if x_vals.size == 0:
            return None
        with np.errstate(divide="ignore", invalid="ignore"):
            y_vals = real_values(expr_text, X, x_vals)
        x_vals, y_vals, anchor_mask = refine_domain_boundaries(
            expr_text, X, x_vals, y_vals, y_bounds=y_bounds
        )
        fill_vals = y_vals.copy()
        threshold = (y1 - y0) * 0.5
        for ji in np.nonzero(np.abs(np.diff(y_vals)) > threshold)[0]:
            if not anchor_mask[ji] and not anchor_mask[ji + 1]:
                y_vals[ji + 1] = np.nan
                fill_vals[ji + 1] = np.nan
        ax.plot(
            x_vals,
            y_vals,
            color=eq["color"],
            linewidth=line_width,
            linestyle=LS_MAP[eq["style"]],
        )
        ineq = eq.get("ineq", "none")
        if ineq == "y >":
            lower = np.clip(fill_vals, y0, y1)
            upper = np.full_like(fill_vals, y1)
            mask = ~np.isnan(fill_vals) & (fill_vals < y1)
            ax.fill_between(
                x_vals, lower, upper, where=mask, alpha=0.15, color=eq["color"]
            )
        elif ineq == "y <":
            lower = np.full_like(fill_vals, y0)
            upper = np.clip(fill_vals, y0, y1)
            mask = ~np.isnan(fill_vals) & (fill_vals > y0)
            ax.fill_between(
                x_vals, lower, upper, where=mask, alpha=0.15, color=eq["color"]
            )
    except (
        TypeError,
        ValueError,
        SyntaxError,
        ZeroDivisionError,
        OverflowError,
        SympifyError,
    ):
        return f"Could not plot `{expr_text}`. Check the expression."
    return None


def _sample_x_values(x0, x1):
    uniform = np.linspace(x0, x1, 4000)
    extra = []
    if x1 > 1e-12:
        extra.append(np.logspace(-12, np.log10(max(x1, 1e-12)), 800))
    if x0 < -1e-12:
        extra.append(-np.logspace(-12, np.log10(max(-x0, 1e-12)), 800))
    return np.unique(np.concatenate([uniform] + extra)) if extra else uniform


def render_cartesian_plot(settings):
    x0, x1 = settings["x0"], settings["x1"]
    y0, y1 = settings["y0"], settings["y1"]
    plot_x_step, x_warnings = normalize_step(x0, x1, settings["x_step"], "xStep")
    plot_y_step, y_warnings = normalize_step(y0, y1, settings["y_step"], "yStep")
    x_vals = _sample_x_values(x0, x1)
    width_in = settings["width"] / PIXELS_PER_INCH
    height_in = settings["height"] / PIXELS_PER_INCH
    fig, ax = plt.subplots(
        figsize=(width_in, height_in), dpi=PIXELS_PER_INCH, layout="constrained"
    )
    warnings = x_warnings + y_warnings
    for eq in settings.get("equations", []):
        w = plot_cartesian_equation(ax, eq, x_vals, (y0, y1), settings["line_width"])
        if w:
            warnings.append(w)
    for pt in settings.get("points", []):
        plot_point(ax, pt, settings["line_width"])
    configure_axes(ax, settings, (plot_x_step, plot_y_step))
    return fig, warnings


def render_cartesian(settings):
    """Pyodide entry point: settings dict -> {svg, warnings} or {error}."""
    try:
        fig, warnings = render_cartesian_plot(settings)
        buf = BytesIO()
        fig.savefig(buf, format="svg")
        plt.close(fig)
        return {"svg": buf.getvalue().decode(), "warnings": warnings}
    except Exception as exc:
        return {"error": str(exc)}
