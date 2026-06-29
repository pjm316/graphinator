import { makeParametricRow } from "./forms.js";
import { makePointRow } from "../ui.js";
import { bindRerender } from "../../shared-ui.js";
import { renderParametric } from "./render.js";

export function setup(pyodide, fns) {
  const rerender = () => renderParametric(pyodide, fns.parametric);
  const paramCont = document.getElementById("param-eqs");
  const paramPts = document.getElementById("param-pts");

  makeParametricRow(paramCont, rerender);

  document.getElementById("param-add")?.addEventListener("click", () => {
    makeParametricRow(paramCont, rerender);
    rerender();
  });
  if (paramPts) {
    document.getElementById("param-pts-add")?.addEventListener("click", () => {
      makePointRow(paramPts, rerender, ["x", "y"]);
      rerender();
    });
    paramPts.addEventListener("change", rerender);
  }

  paramCont.addEventListener("change", rerender);
  bindRerender(
    [
      "param-xmin",
      "param-xmax",
      "param-xstep",
      "param-ymin",
      "param-ymax",
      "param-ystep",
      "param-grid",
      "param-minor-grid",
      "param-tick-labels",
      "param-lw",
      "param-xlabel",
      "param-ylabel",
      "param-width",
      "param-height",
    ],
    rerender,
  );

  document.getElementById("param-arrows")?.addEventListener("change", (e) => {
    const labelsEl = document.getElementById("param-arrow-labels");
    if (labelsEl) labelsEl.hidden = !e.target.checked;
    rerender();
  });
}
