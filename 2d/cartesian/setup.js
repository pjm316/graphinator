import { makeCartesianRow } from "./forms.js";
import { makePointRow } from "../ui.js";
import { bindRerender } from "../../shared-ui.js";
import { renderCartesian } from "./render.js";

export function setup(pyodide, fns) {
  const rerender = () => renderCartesian(pyodide, fns.cartesian);
  const cartCont = document.getElementById("cart-eqs");
  const cartPts = document.getElementById("cart-pts");

  makeCartesianRow(cartCont, rerender, { expr: "x^2" });

  document.getElementById("cart-add")?.addEventListener("click", () => {
    makeCartesianRow(cartCont, rerender);
    rerender();
  });
  if (cartPts) {
    document.getElementById("cart-pts-add")?.addEventListener("click", () => {
      makePointRow(cartPts, rerender, ["x", "y"]);
      rerender();
    });
    cartPts.addEventListener("change", rerender);
  }

  cartCont.addEventListener("change", rerender);
  bindRerender(
    [
      "cart-xmin",
      "cart-xmax",
      "cart-xstep",
      "cart-ymin",
      "cart-ymax",
      "cart-ystep",
      "cart-grid",
      "cart-minor-grid",
      "cart-tick-labels",
      "cart-lw",
      "cart-xlabel",
      "cart-ylabel",
      "cart-width",
      "cart-height",
    ],
    rerender,
  );

  document.getElementById("cart-arrows")?.addEventListener("change", (e) => {
    const labelsEl = document.getElementById("cart-arrow-labels");
    if (labelsEl) labelsEl.hidden = !e.target.checked;
    rerender();
  });
}
