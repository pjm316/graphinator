"""Shared constants, parser config, and re-exports from math_utils and axis_utils."""

import re

from matplotlib import rcParams
from sympy import Abs, E, log
from sympy import pi as sym_pi
from sympy import symbols
from sympy.parsing.sympy_parser import convert_xor as xor_transform
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
)

rcParams["svg.fonttype"] = "none"

# --- Symbols & parser config ---

X = symbols("x")
T = symbols("t")
THETA = symbols("theta")

LOCAL_DICT = {
    "x": X,
    "t": T,
    "theta": THETA,
    "e": E,
    "pi": sym_pi,
    "ln": log,
    "log": lambda value, base=10: log(value, base),
    "Abs": Abs,
    "abs": Abs,
}

TRANSFORMS = standard_transformations + (
    implicit_multiplication_application,
    xor_transform,
)

# --- Display constants ---

COLORS = ["#0000FF", "#FF0000", "#008000", "#FFA500", "#800080", "#008080"]
LS_MAP = {"solid": "-", "dashed": "--"}

PIXELS_PER_INCH = 120.0


def normalize_absolute_value_notation(expr: str) -> str:
    """Convert |x| syntax into Abs(x) for SymPy parsing."""
    expr = expr.replace("−", "-")
    return re.sub(r"\|([^|]*)\|", r"Abs(\1)", expr)


def plot_point(ax, pt, line_width):
    try:
        px, py = float(pt["x"]), float(pt["y"])
        size = float(pt.get("size", 8.0))
        filled = pt.get("filled", True)
        ax.plot(
            px,
            py,
            marker="o",
            color=pt["color"],
            markersize=size * 0.75,
            linewidth=0,
            markerfacecolor=pt["color"] if filled else "white",
            markeredgecolor=pt["color"],
            markeredgewidth=max(1.2, line_width),
            zorder=10,
        )
        label = pt.get("label", "").strip()
        if label:
            ax.annotate(
                label,
                (px, py),
                textcoords="offset points",
                xytext=(float(pt.get("label_dx", 6)), float(pt.get("label_dy", 6))),
                fontsize=9,
                color=pt["color"],
                zorder=11,
            )
    except (TypeError, ValueError):
        pass


from math_utils import real_values, refine_domain_boundaries

from axis_utils import (
    normalize_step,
    configure_axes,
    _axis_arrow_style,
)
