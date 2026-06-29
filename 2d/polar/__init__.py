"""Polar graphing: r = f(theta) on native polar axes."""

from io import BytesIO
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sympy import SympifyError

from shared import THETA, LS_MAP, PIXELS_PER_INCH, real_values, plot_point


def plot_polar_equation(ax, eq, line_width):
    expr_text = str(eq.get("expr", "")).strip()
    if not expr_text:
        return None
    try:
        theta_min_deg = float(eq.get("theta_min", 0.0))
        theta_max_deg = float(eq.get("theta_max", 360.0))
        if not (np.isfinite(theta_min_deg) and np.isfinite(theta_max_deg)):
            return f"Invalid theta range for `{expr_text}`."
        theta_vals = np.linspace(
            np.radians(theta_min_deg), np.radians(theta_max_deg), 4000
        )
        with np.errstate(divide="ignore", invalid="ignore"):
            r_vals = real_values(expr_text, THETA, theta_vals)
        # Reflect negative r through the origin: r<0 plots at (|r|, theta+pi).
        theta_plot = theta_vals.copy()
        r_plot = r_vals.copy()
        neg = r_plot < 0
        r_plot[neg] = -r_plot[neg]
        theta_plot[neg] += np.pi
        ax.plot(
            theta_plot,
            r_plot,
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
        return f"Could not plot `{expr_text}`. Check the expression."
    return None


def plot_polar_point(ax, pt, line_width):
    try:
        r = float(pt["r"])
        theta_rad = math.radians(float(pt["theta"]))
    except (TypeError, ValueError):
        return
    plot_point(ax, {**pt, "x": theta_rad, "y": r}, line_width)


def render_polar_plot(settings):
    line_width = settings["line_width"]
    width_in = settings["width"] / PIXELS_PER_INCH
    height_in = settings["height"] / PIXELS_PER_INCH
    fig, ax = plt.subplots(
        figsize=(width_in, height_in),
        dpi=PIXELS_PER_INCH,
        subplot_kw={"projection": "polar"},
        layout="constrained",
    )
    warnings = []
    for eq in settings.get("equations", []):
        w = plot_polar_equation(ax, eq, line_width)
        if w:
            warnings.append(w)
    for pt in settings.get("points", []):
        plot_polar_point(ax, pt, line_width)
    r_max = settings.get("r_max", 0.0)
    if r_max > 0:
        ax.set_rmax(r_max)
    theta_step = settings.get("theta_step", 30.0)
    if theta_step > 0:
        ax.set_thetagrids(np.arange(0, 360, theta_step))
    ax.grid(True)
    ax.tick_params(labelsize=9)
    # Draw radial labels at 45 degrees with high z-order so they appear above grid circles.
    r_ticks = [t for t in ax.get_yticks() if t > 0]
    ax.set_yticklabels([])
    theta_label = np.radians(45)
    for r in r_ticks:
        ax.text(
            theta_label, r, f"{r:.4g}", fontsize=9, ha="left", va="center", zorder=100
        )
    return fig, warnings


def render_polar(settings):
    """Pyodide entry point: settings dict -> {svg, warnings} or {error}."""
    try:
        fig, warnings = render_polar_plot(settings)
        buf = BytesIO()
        fig.savefig(buf, format="svg")
        plt.close(fig)
        return {"svg": buf.getvalue().decode(), "warnings": warnings}
    except Exception as exc:
        return {"error": str(exc)}
