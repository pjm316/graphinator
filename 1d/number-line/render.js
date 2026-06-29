import { renderToPanel } from "../../pyodide.js";
import { num, size } from "../../shared-ui.js";
import { getNLEqs } from "./forms.js";

export function render(pyodide, fn) {
  const isSkipCounting =
    document.querySelector('input[name="nl-mode"]:checked')?.value ===
    "skip-counting";
  renderToPanel(pyodide, fn, "nl", {
    equations: isSkipCounting
      ? []
      : getNLEqs(document.getElementById("nl-eqs")),
    x0: num("nl-xmin"),
    x1: num("nl-xmax"),
    x_step: num("nl-xstep"),
    show_labels: true,
    line_width: num("nl-lw"),
    show_skip_counting: isSkipCounting,
    skip_start: isSkipCounting ? num("nl-sc-start") : 0,
    skip_step: isSkipCounting ? num("nl-sc-step") : 2,
    ...size("nl"),
  });
}
