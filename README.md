# Graphinator

Graphinator is a static multi-page graphing app that runs Python in the browser with Pyodide and renders SVG graphs with Matplotlib.

It currently includes four independent pages:

- **Cartesian**: `y = f(x)` equations with inequality shading and `(x, y)` points
- **Polar**: `r = f(theta)` graphs with `(r, theta)` points
- **Parametric**: `x(t), y(t)` curve pairs with `(x, y)` points
- **Number Line**: inequalities, rays, segments, and optional skip counting

Each page has its own controls, examples, and SVG export. There is no shared state between pages.

## How It Works

- The HTML/JS frontend lives in `index.html`, `app.css`, `shared-ui.js`, and the page-specific files under `1d/` and `2d/`.
- `pyodide.js` loads Pyodide in the browser, fetches the Python source files, and calls the page renderer.
- The Python renderers build Matplotlib figures and return SVG back to the page.

## Architecture Notes

- The graph pages are intentionally kept as separate apps with separate setup and render flows.
- Shared code should stay at the utility layer: Pyodide bootstrapping, DOM helpers, SVG display/export, and small math/render helpers.
- Avoid adding a generic page framework unless the same change repeatedly lands across multiple apps.

## Run Locally

Because the frontend fetches local files, run the project through a local static server instead of opening `index.html` directly from disk.

### Option 1: Python

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.

### Option 2: Any static server

Any local static file server is fine as long as it serves the repo root.

## Python Dependencies

The browser runtime loads `sympy` and `matplotlib` through Pyodide, but the project also keeps Python dependencies listed locally for development:

```bash
pip install -r requirements.txt
```

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Formatting

```bash
npm install
pip install -r requirements-dev.txt
npm run format
npm run format:check
```
