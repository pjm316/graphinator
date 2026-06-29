import { el, eqLine, lbl, nextColor, removeBtn } from "../../shared-ui.js";

export function makeNLRow(container, rerender, opts = {}) {
  const row = el("div", { class: "eq-row" });
  const expr = el("input", {
    class: "expr",
    type: "text",
    placeholder: "e.g. x > 2",
    "aria-label": "Inequality",
  });
  expr.value = opts.expr ?? "";
  const color = el("input", {
    class: "color",
    type: "color",
    value: opts.color ?? nextColor(container),
  });
  row.append(
    eqLine(
      lbl("Inequality", expr),
      lbl("Color", color, "color-grp"),
      removeBtn(container, row, expr, rerender),
    ),
  );
  container.appendChild(row);
}

export function getNLEqs(container) {
  return [...container.querySelectorAll(".eq-row")].map((r) => ({
    expr: r.querySelector(".expr").value,
    color: r.querySelector(".color").value,
  }));
}
