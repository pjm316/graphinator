import { renderToPanel } from "../../pyodide.js";
import { size } from "../../shared-ui.js";
import {
  getXYPoints,
  xyWindowSettings,
  cartesianLikeStyleSettings,
} from "../ui.js";
import { getCartesianEqs } from "./forms.js";

export function renderCartesian(pyodide, fn) {
  renderToPanel(pyodide, fn, "cart", {
    equations: getCartesianEqs(document.getElementById("cart-eqs")),
    points: getXYPoints(document.getElementById("cart-pts")),
    ...xyWindowSettings("cart"),
    ...size("cart"),
    ...cartesianLikeStyleSettings("cart"),
  });
}
