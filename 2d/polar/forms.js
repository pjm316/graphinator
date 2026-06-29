import {
  el,
  eqLine,
  lbl,
  nextColor,
  removeBtn,
  styleSelect,
} from "../../shared-ui.js";

export function makePolarRow(container, rerender, opts = {}) {
  const row = el("div", { class: "eq-row" });
  const expr = el("input", {
    class: "expr",
    type: "text",
    placeholder: "e.g. 2*sin(3*theta)",
    "aria-label": "Expression",
  });
  expr.value = opts.expr ?? "";
  const color = el("input", {
    class: "color",
    type: "color",
    value: opts.color ?? nextColor(container),
    "aria-label": "Color",
  });
  const tmin = el("input", {
    class: "tmin",
    type: "number",
    value: opts.theta_min ?? 0,
    step: "15",
    "aria-label": "theta min (deg)",
  });
  const tmax = el("input", {
    class: "tmax",
    type: "number",
    value: opts.theta_max ?? 360,
    step: "15",
    "aria-label": "theta max (deg)",
  });
  row.append(
    eqLine(lbl("r = f(θ)", expr), removeBtn(container, row, expr, rerender)),
    eqLine(
      lbl("Color", color, "color-grp"),
      lbl("Style", styleSelect(opts.style ?? "solid")),
      lbl("θ min (deg)", tmin),
      lbl("θ max (deg)", tmax),
    ),
  );
  container.appendChild(row);
}

export function getPolarEqs(container) {
  return [...container.querySelectorAll(".eq-row")].map((r) => ({
    expr: r.querySelector(".expr").value,
    color: r.querySelector(".color").value,
    style: r.querySelector(".style").value,
    theta_min: Number.parseFloat(r.querySelector(".tmin").value),
    theta_max: Number.parseFloat(r.querySelector(".tmax").value),
  }));
}
