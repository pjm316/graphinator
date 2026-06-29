import { bindRerender } from "../../shared-ui.js";
import { makeNLRow } from "./forms.js";
import { render } from "./render.js";

export function setup(pyodide, fns) {
  const rerender = () => render(pyodide, fns.numberLine);
  const nlCont = document.getElementById("nl-eqs");
  const ineqSection = document.getElementById("nl-ineq-section");
  const scSection = document.getElementById("nl-sc-section");
  const lwSection = document.getElementById("nl-lw-section");

  makeNLRow(nlCont, rerender, { expr: "x > 2" });

  for (const radio of document.querySelectorAll('input[name="nl-mode"]')) {
    radio.addEventListener("change", () => {
      const isSC = radio.value === "skip-counting";
      ineqSection.hidden = isSC;
      scSection.hidden = !isSC;
      lwSection.hidden = isSC;
      if (isSC) {
        document.getElementById("nl-xmin").value = 0;
        document.getElementById("nl-xmax").value = 10;
        document.getElementById("nl-xstep").value = 2;
      } else {
        document.getElementById("nl-xmin").value = -10;
        document.getElementById("nl-xmax").value = 10;
        document.getElementById("nl-xstep").value = 1;
      }
      rerender();
    });
  }

  nlCont.addEventListener("change", rerender);
  bindRerender(
    [
      "nl-xmin",
      "nl-xmax",
      "nl-xstep",
      "nl-lw",
      "nl-width",
      "nl-height",
      "nl-sc-start",
      "nl-sc-step",
    ],
    rerender,
  );
}
