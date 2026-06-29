"""Axis utilities: ticks, labels, grid rendering."""

import numpy as np
from matplotlib import ticker
from matplotlib.patches import FancyArrowPatch

MAX_TICKS = 1000


def tick_count(lo, hi, step):
    """Calculate number of ticks at given step."""
    if step <= 0 or not np.isfinite(step):
        return MAX_TICKS + 1
    return int(np.floor((hi - lo) / step)) + 1


def make_ticks(lo, hi, step, *, exclude_endpoints=False):
    """Generate tick positions in range."""
    start = np.ceil(lo / step) * step
    ticks = np.round(np.arange(start, hi + step * 1e-9, step), 10)
    return [
        t
        for t in ticks
        if lo <= t <= hi
        and not np.isclose(t, 0.0)
        and not (exclude_endpoints and (np.isclose(t, lo) or np.isclose(t, hi)))
    ]


def normalize_step(lo, hi, step, label):
    """Adjust step if too many ticks would be created."""
    warnings = []
    if tick_count(lo, hi, step) > MAX_TICKS:
        step = max((hi - lo) / (MAX_TICKS - 1), 1e-6)
        warnings.append(
            f"{label} was automatically increased to {step:.4g} to avoid too many ticks."
        )
    return step, warnings


def _axis_arrow_style(lo: float, hi: float) -> str | None:
    """Determine arrow style based on axis bounds."""
    lower_arrow = lo < 0
    upper_arrow = hi > 0
    if lower_arrow and upper_arrow:
        return "<|-|>"
    if upper_arrow:
        return "-|>"
    if lower_arrow:
        return "<|-"
    return None


def _add_axis_arrow(ax, start, end, arrowstyle: str) -> None:
    """Add arrow to axis."""
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle=arrowstyle,
            color="black",
            linewidth=0.8,
            mutation_scale=8,
            shrinkA=0,
            shrinkB=0,
            clip_on=False,
        )
    )


def _draw_axis_arrowheads(ax, x_bounds, y_bounds) -> None:
    """Draw axis arrow endpoints."""
    x0, x1 = x_bounds
    y0, y1 = y_bounds
    x_style = _axis_arrow_style(x0, x1)
    y_style = _axis_arrow_style(y0, y1)
    if y0 <= 0 <= y1 and x_style:
        _add_axis_arrow(ax, (x0, 0), (x1, 0), x_style)
    if x0 <= 0 <= x1 and y_style:
        _add_axis_arrow(ax, (0, y0), (0, y1), y_style)


def _draw_axis_labels(ax, x_label, y_label, x_bounds, y_bounds) -> None:
    """Draw axis labels."""
    x0, x1 = x_bounds
    y0, y1 = y_bounds
    style = {"fontsize": 9, "fontstyle": "italic", "clip_on": False}
    if x_label and x1 > 0 and y0 <= 0 <= y1:
        ax.annotate(
            x_label,
            xy=(x1, 0),
            xytext=(-2, -7),
            textcoords="offset points",
            ha="center",
            va="top",
            **style,
        )
    if y_label and y1 > 0 and x0 <= 0 <= x1:
        ax.annotate(
            y_label,
            xy=(0, y1),
            xytext=(-7, -1),
            textcoords="offset points",
            ha="right",
            va="center",
            **style,
        )


def _configure_ticks(
    ax, x_bounds, y_bounds, steps, *, show_labels, show_minor_grid, axis_arrows
) -> None:
    """Configure tick marks and grid."""
    x0, x1 = x_bounds
    y0, y1 = y_bounds
    plot_x_step, plot_y_step, x_minor, y_minor = steps
    ax.xaxis.set_major_locator(ticker.MultipleLocator(plot_x_step))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(plot_y_step))
    if show_minor_grid:
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(x_minor))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(y_minor))
    else:
        ax.xaxis.set_minor_locator(ticker.NullLocator())
        ax.yaxis.set_minor_locator(ticker.NullLocator())
    if show_labels or axis_arrows:
        ax.set_xticks(make_ticks(x0, x1, plot_x_step, exclude_endpoints=axis_arrows))
        ax.set_yticks(make_ticks(y0, y1, plot_y_step, exclude_endpoints=axis_arrows))
    if show_minor_grid and axis_arrows:
        ax.set_xticks(make_ticks(x0, x1, x_minor, exclude_endpoints=True), minor=True)
        ax.set_yticks(make_ticks(y0, y1, y_minor, exclude_endpoints=True), minor=True)
    if not show_labels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])


def configure_axes(ax, settings, steps) -> None:
    """Configure axis appearance, ticks, grid, arrows, labels."""
    x0, x1 = settings["x0"], settings["x1"]
    y0, y1 = settings["y0"], settings["y1"]
    width, height = settings["width"], settings["height"]
    axis_arrows = settings.get("axis_arrows", False)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)
    ax.set_aspect("equal" if width == height else "auto")
    ax.set(xlabel="", ylabel="")
    ax.spines[["right", "top"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_position("zero")
    if axis_arrows:
        ax.spines[["left", "bottom"]].set_visible(False)
    plot_x_step, plot_y_step = steps
    x_minor = settings["x_minor"] if settings.get("x_minor", 0) > 0 else plot_x_step / 2
    y_minor = settings["y_minor"] if settings.get("y_minor", 0) > 0 else plot_y_step / 2
    _configure_ticks(
        ax,
        (x0, x1),
        (y0, y1),
        (plot_x_step, plot_y_step, x_minor, y_minor),
        show_labels=settings["show_labels"],
        show_minor_grid=settings.get("show_minor_grid", False),
        axis_arrows=axis_arrows,
    )
    if settings["show_grid"]:
        ax.grid(True, which="major", linestyle=":", alpha=0.5)
    if settings["show_minor_grid"]:
        ax.grid(True, which="minor", linestyle=":", alpha=0.25)
    if axis_arrows:
        _draw_axis_arrowheads(ax, (x0, x1), (y0, y1))
        _draw_axis_labels(
            ax,
            settings.get("x_label", ""),
            settings.get("y_label", ""),
            (x0, x1),
            (y0, y1),
        )
    ax.tick_params(axis="both", labelsize=9)
