import { renderToPanel } from "../../pyodide.js";
import { size } from "../../shared-ui.js";
import {
  getXYPoints,
  xyWindowSettings,
  cartesianLikeStyleSettings,
} from "../ui.js";
import { getParametricEqs } from "./forms.js";

export function renderParametric(pyodide, fn) {
  renderToPanel(pyodide, fn, "param", {
    equations: getParametricEqs(document.getElementById("param-eqs")),
    points: getXYPoints(document.getElementById("param-pts")),
    ...xyWindowSettings("param"),
    ...size("param"),
    ...cartesianLikeStyleSettings("param"),
  });
}
