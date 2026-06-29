"""Number line drawing: equations, rays, segments, skip counting arcs."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path

from shared import PIXELS_PER_INCH
from number_line_parse import parse_nl

SKIP_COLOR = "blue"
MAX_SKIP_ARCS = 200
ARC_BASE_OFFSET = 0.09
ARC_HEIGHT = 0.58
LABEL_GAP = 0.08
SKIP_COUNT_ROW_SPACING = 1.35
STANDARD_ROW_SPACING = 1.0
BASE_ARROW_SIZE = 11
RAY_ARROW_SIZE = 16


def add_clean_arrow(ax, x, y, direction, *, color, size=15):
    """Add a clean arrow at (x, y) pointing left or right."""
    sign = 1 if direction == "right" else -1
    arrowstyle = f"Simple,head_width={size * 0.6},head_length={size * 0.9},tail_width=0"
    ax.add_patch(
        FancyArrowPatch(
            posA=(x - sign * 0.01, y),
            posB=(x, y),
            arrowstyle=arrowstyle,
            color=color,
            linewidth=0,
            mutation_scale=1,
            zorder=11,
        )
    )


def _tip_offset(ax, fig, size):
    """Convert screen size to data coordinates."""
    points_per_inch = 72.0
    width_pts = ax.get_position().width * fig.get_size_inches()[0] * points_per_inch
    x_limits = ax.get_xlim()
    data_per_point = (x_limits[1] - x_limits[0]) / width_pts if width_pts > 0 else 0
    return size * 0.9 * data_per_point


def _draw_number_line_ray(ax, eq, parsed, outer_x0, outer_x1, settings, y, tip_ray):
    """Draw a ray (open or closed at endpoint)."""
    val, inclusive = parsed["bound"]
    going_right = parsed["direction"] == "right"
    end = outer_x1 if going_right else outer_x0
    line_end = end - tip_ray if going_right else end + tip_ray
    thick = settings["line_width"] * 2.2
    ax.plot([val, line_end], [y, y], color=eq["color"], lw=thick, ls="solid", zorder=8)
    add_clean_arrow(
        ax, end, y, parsed["direction"], color=eq["color"], size=RAY_ARROW_SIZE
    )
    ax.plot(
        val,
        y,
        "o",
        color=eq["color"] if inclusive else "white",
        markersize=7,
        markeredgecolor=eq["color"],
        markeredgewidth=1.5,
        zorder=9,
    )


def _draw_number_line_segment(ax, eq, left_value, right_value, y, settings):
    """Draw a segment with open/closed endpoints."""
    thick = 2.2 * settings["line_width"]
    ax.plot(
        [left_value[0], right_value[0]],
        [y, y],
        color=eq["color"],
        lw=thick,
        ls="solid",
        zorder=8,
    )
    for point_value, inclusive in [left_value, right_value]:
        ax.plot(
            point_value,
            y,
            "o",
            color=eq["color"] if inclusive else "white",
            markersize=7,
            markeredgecolor=eq["color"],
            markeredgewidth=1.5,
            zorder=9,
        )


def _draw_number_line_tick(ax, tick, y, show_labels):
    """Draw a single tick mark."""
    ax.plot([tick, tick], [y - 0.06, y + 0.06], color="#333", lw=1.0, zorder=6)
    if show_labels:
        ax.text(tick, y - 0.18, f"{tick:g}", ha="center", va="top", fontsize=9)


def _draw_number_line_ticks(ax, settings, y):
    """Draw all tick marks for this row."""
    x0, x1, x_step = settings["x0"], settings["x1"], settings["x_step"]
    show_labels = settings["show_labels"]
    for tick in np.round(
        np.arange(np.ceil(x0 / x_step) * x_step, x1 + 1e-9, x_step), 10
    ):
        if x0 <= tick <= x1:
            _draw_number_line_tick(ax, tick, y, show_labels)


def _skip_count_segments(settings):
    """Generate (left, right) pairs for skip counting arcs."""
    x0, x1 = settings["x0"], settings["x1"]
    step = settings.get("skip_step", 2.0)
    start = settings.get("skip_start", 0.0)
    if step <= 0:
        return
    current = start
    while current + step < x0:
        current += step
    for _ in range(MAX_SKIP_ARCS):
        next_value = current + step
        if next_value > x1 + 1e-9:
            break
        if next_value > x0 and current < x1:
            yield current, next_value
        current = next_value


def _skip_count_arc_path(left, right, y):
    """Construct Path for skip counting arc."""
    base_y = y + ARC_BASE_OFFSET
    peak_y = y + ARC_HEIGHT
    span = right - left
    return Path(
        [
            (left, base_y),
            (left + span * 0.18, peak_y),
            (left + span * 0.82, peak_y),
            (right, base_y),
        ],
        [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4],
    )


def _skip_count_label_y(y):
    """Y-position for skip counting label."""
    return y + ARC_HEIGHT + LABEL_GAP


def draw_skip_counting(ax, settings, y):
    """Draw skip counting arcs and labels."""
    if not settings.get("show_skip_counting", False):
        return
    for left, right in _skip_count_segments(settings):
        arc = FancyArrowPatch(
            path=_skip_count_arc_path(left, right, y),
            arrowstyle="-|>",
            mutation_scale=11,
            lw=1.35,
            color=SKIP_COLOR,
            alpha=0.95,
            zorder=8,
        )
        ax.add_patch(arc)
        ax.text(
            (left + right) / 2,
            _skip_count_label_y(y),
            f"{right:g}",
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="semibold",
            color=SKIP_COLOR,
            zorder=9,
        )


def _number_line_row_spacing(settings):
    """Spacing between rows based on whether skip counting is shown."""
    return (
        SKIP_COUNT_ROW_SPACING
        if settings.get("show_skip_counting", False)
        else STANDARD_ROW_SPACING
    )


def _number_line_y_limits(equations, settings, row_spacing):
    """Y-axis limits for plot."""
    if not settings.get("show_skip_counting", False):
        return -0.8, len(equations) + 0.2
    top_row_y = max(len(equations) - 1, 0) * row_spacing
    return -0.8, top_row_y + 1.2


def plot_number_line_equation(
    ax, eq, index, outer_x0, outer_x1, settings, *, tip, tip_ray, row_spacing
):
    """Render one equation on the number line."""
    equations = settings.get("equations", [])
    y = (len(equations) - 1 - index) * row_spacing
    ax.plot([outer_x0 + tip, outer_x1 - tip], [y, y], color="#333", lw=1.0, zorder=5)
    add_clean_arrow(ax, outer_x0, y, "left", color="#333", size=BASE_ARROW_SIZE)
    add_clean_arrow(ax, outer_x1, y, "right", color="#333", size=BASE_ARROW_SIZE)
    _draw_number_line_ticks(ax, settings, y)
    draw_skip_counting(ax, settings, y)
    expr_text = str(eq.get("expr", "")).strip()
    if not expr_text:
        return None
    parsed = parse_nl(expr_text)
    if not parsed:
        return f"Could not plot `{expr_text}`. Check the expression."

    def draw_parsed(part):
        if part["type"] == "ray":
            _draw_number_line_ray(
                ax, eq, part, outer_x0, outer_x1, settings, y, tip_ray
            )
        elif part["type"] == "segment":
            _draw_number_line_segment(ax, eq, part["left"], part["right"], y, settings)

    if parsed["type"] == "union":
        for part in parsed["parts"]:
            draw_parsed(part)
    else:
        draw_parsed(parsed)
    return None


def render_number_line_plot(settings):
    """Generate matplotlib figure for number line plot."""
    equations = settings.get("equations", [])
    if settings.get("show_skip_counting", False) and not equations:
        equations = [{"expr": "", "color": SKIP_COLOR}]
    plot_settings = {**settings, "equations": equations}
    row_spacing = _number_line_row_spacing(settings)
    width_in = settings["width"] / PIXELS_PER_INCH
    height_in = max(settings["height"] / PIXELS_PER_INCH, len(equations) * row_spacing)
    fig, ax = plt.subplots(figsize=(width_in, height_in), dpi=PIXELS_PER_INCH)
    x_pad = 0.12 * (settings["x1"] - settings["x0"])
    ax.set_xlim(settings["x0"] - x_pad * 1.5, settings["x1"] + x_pad * 1.5)
    ax.set_ylim(*_number_line_y_limits(equations, plot_settings, row_spacing))
    ax.axis("off")
    x0, x1 = settings["x0"], settings["x1"]
    tip = _tip_offset(ax, fig, size=BASE_ARROW_SIZE)
    tip_ray = _tip_offset(ax, fig, size=RAY_ARROW_SIZE)
    outer_x0, outer_x1 = x0 - x_pad, x1 + x_pad
    warnings = []
    for idx, eq in enumerate(equations):
        w = plot_number_line_equation(
            ax,
            eq,
            idx,
            outer_x0,
            outer_x1,
            plot_settings,
            tip=tip,
            tip_ray=tip_ray,
            row_spacing=row_spacing,
        )
        if w:
            warnings.append(w)
    return fig, warnings
