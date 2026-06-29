"""Number line graphing: inequalities, rays, segments, skip counting."""

from io import BytesIO
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from shared import PIXELS_PER_INCH

from number_line_parse import parse_nl
from number_line_draw import render_number_line_plot


def render_number_line(settings):
    """Pyodide entry point: settings dict -> {svg, warnings} or {error}."""
    try:
        fig, warnings = render_number_line_plot(settings)
        buf = BytesIO()
        fig.savefig(buf, format="svg")
        plt.close(fig)
        return {"svg": buf.getvalue().decode(), "warnings": warnings}
    except Exception as exc:
        return {"error": str(exc)}
