import {
  el,
  eqLine,
  lbl,
  nextColor,
  removeBtn,
  styleSelect,
} from "../../shared-ui.js";

export function makeCartesianRow(container, rerender, opts = {}) {
  const row = el("div", { class: "eq-row" });
  const expr = el("input", {
    class: "expr",
    type: "text",
    placeholder: "e.g. x^2",
    "aria-label": "Expression",
  });
  expr.value = opts.expr ?? "";
  const color = el("input", {
    class: "color",
    type: "color",
    value: opts.color ?? nextColor(container),
    "aria-label": "Color",
  });
  const ineq = el("select", { class: "ineq", "aria-label": "Inequality" });
  for (const [v, t] of [
    ["none", "none"],
    ["y >", "y >"],
    ["y <", "y <"],
  ]) {
    const o = el("option", { value: v, text: t });
    if (v === (opts.ineq ?? "none")) o.selected = true;
    ineq.appendChild(o);
  }
  const xmin = el("input", {
    class: "xmin",
    type: "number",
    placeholder: "auto",
    "aria-label": "x min",
  });
  if (opts.x_min !== undefined) xmin.value = opts.x_min;
  const xmax = el("input", {
    class: "xmax",
    type: "number",
    placeholder: "auto",
    "aria-label": "x max",
  });
  if (opts.x_max !== undefined) xmax.value = opts.x_max;
  row.append(
    eqLine(lbl("y = f(x)", expr), removeBtn(container, row, expr, rerender)),
    eqLine(
      lbl("Color", color, "color-grp"),
      lbl("Style", styleSelect(opts.style ?? "solid", ["solid", "dashed"])),
      lbl("Inequality", ineq),
    ),
    eqLine(lbl("x min", xmin), lbl("x max", xmax)),
  );
  container.appendChild(row);
}

export function getCartesianEqs(container) {
  return [...container.querySelectorAll(".eq-row")].map((r) => {
    const eq = {
      expr: r.querySelector(".expr").value,
      color: r.querySelector(".color").value,
      style: r.querySelector(".style").value,
      ineq: r.querySelector(".ineq").value,
    };
    const xminVal = r.querySelector(".xmin")?.value;
    const xmaxVal = r.querySelector(".xmax")?.value;
    if (xminVal !== "" && xminVal !== undefined)
      eq.x_min = Number.parseFloat(xminVal);
    if (xmaxVal !== "" && xmaxVal !== undefined)
      eq.x_max = Number.parseFloat(xmaxVal);
    return eq;
  });
}
