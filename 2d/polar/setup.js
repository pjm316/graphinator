import { makePolarRow } from "./forms.js";
import { makePointRow } from "../ui.js";
import { bindRerender } from "../../shared-ui.js";
import { renderPolar } from "./render.js";

export function setup(pyodide, fns) {
  const rerender = () => renderPolar(pyodide, fns.polar);
  const polCont = document.getElementById("pol-eqs");
  const polPts = document.getElementById("pol-pts");

  makePolarRow(polCont, rerender, { expr: "2*sin(3*theta)" });

  document.getElementById("pol-add")?.addEventListener("click", () => {
    makePolarRow(polCont, rerender);
    rerender();
  });
  if (polPts) {
    document.getElementById("pol-pts-add")?.addEventListener("click", () => {
      makePointRow(polPts, rerender, ["r", "theta"], {
        displayLabels: ["r", "θ"],
      });
      rerender();
    });
    polPts.addEventListener("change", rerender);
  }

  polCont.addEventListener("change", rerender);
  bindRerender(
    ["pol-rmax", "pol-lw", "pol-width", "pol-height"],
    rerender,
  );
}
