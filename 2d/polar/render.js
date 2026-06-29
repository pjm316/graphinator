import { renderToPanel } from "../../pyodide.js";
import { num, size } from "../../shared-ui.js";
import { getRTPoints } from "../ui.js";
import { getPolarEqs } from "./forms.js";

export function renderPolar(pyodide, fn) {
  renderToPanel(pyodide, fn, "pol", {
    equations: getPolarEqs(document.getElementById("pol-eqs")),
    points: getRTPoints(document.getElementById("pol-pts")),
    r_max: num("pol-rmax"),
    theta_step: 30,
    line_width: num("pol-lw"),
    ...size("pol"),
  });
}
