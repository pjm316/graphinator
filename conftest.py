import sys
from pathlib import Path

import matplotlib
import pytest
from matplotlib import pyplot as plt

matplotlib.use("Agg")

sys.path.insert(0, str(Path(__file__).parent / "2d"))
sys.path.insert(0, str(Path(__file__).parent / "1d" / "number-line"))


@pytest.fixture(autouse=True)
def close_matplotlib_figures():
    """Keep render-heavy tests from leaking Matplotlib figures."""
    yield
    plt.close("all")
