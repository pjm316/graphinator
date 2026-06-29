import {
  el,
  eqLine,
  lbl,
  nextColor,
  removeBtn,
  styleSelect,
} from "../../shared-ui.js";

export function makeParametricRow(container, rerender, opts = {}) {
  const row = el("div", { class: "eq-row" });
  const xexpr = el("input", {
    class: "xexpr",
    type: "text",
    placeholder: "e.g. cos(t)",
    "aria-label": "x(t)",
  });
  xexpr.value = opts.x_expr ?? "cos(t)";
  const yexpr = el("input", {
    class: "yexpr",
    type: "text",
    placeholder: "e.g. sin(t)",
    "aria-label": "y(t)",
  });
  yexpr.value = opts.y_expr ?? "sin(t)";
  const color = el("input", {
    class: "color",
    type: "color",
    value: opts.color ?? nextColor(container),
    "aria-label": "Color",
  });
  const tmin = el("input", {
    class: "tmin",
    type: "number",
    value: opts.t_min ?? 0,
    step: "0.5",
    "aria-label": "t min",
  });
  const tmax = el("input", {
    class: "tmax",
    type: "number",
    value: opts.t_max ?? 6.28,
    step: "0.5",
    "aria-label": "t max",
  });
  row.append(
    eqLine(
      lbl("x(t)", xexpr),
      lbl("y(t)", yexpr),
      removeBtn(container, row, xexpr, rerender),
    ),
    eqLine(
      lbl("Color", color, "color-grp"),
      lbl("Style", styleSelect(opts.style ?? "solid")),
      lbl("t min", tmin),
      lbl("t max", tmax),
    ),
  );
  container.appendChild(row);
}

export function getParametricEqs(container) {
  return [...container.querySelectorAll(".eq-row")].map((r) => ({
    x_expr: r.querySelector(".xexpr").value,
    y_expr: r.querySelector(".yexpr").value,
    color: r.querySelector(".color").value,
    style: r.querySelector(".style").value,
    t_min: Number.parseFloat(r.querySelector(".tmin").value),
    t_max: Number.parseFloat(r.querySelector(".tmax").value),
  }));
}
