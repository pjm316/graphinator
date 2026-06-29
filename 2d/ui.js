import {
  el,
  COLORS,
  lbl,
  eqLine,
  removeBtn,
  num,
  chk,
  txt,
} from "../shared-ui.js";

export function makePointRow(container, rerender, coordLabels, opts = {}) {
  const row = el("div", { class: "eq-row" });
  const c0 = el("input", {
    class: "c0",
    type: "number",
    value: opts[coordLabels[0]] ?? 0,
    step: "0.5",
  });
  const c1 = el("input", {
    class: "c1",
    type: "number",
    value: opts[coordLabels[1]] ?? 0,
    step: "0.5",
  });
  const displayLabels = opts.displayLabels ?? coordLabels;
  const color = el("input", {
    class: "color",
    type: "color",
    value: opts.color ?? COLORS[0],
  });
  const filled = el("input", { class: "filled", type: "checkbox" });
  filled.checked = opts.filled !== false;
  const ptLabel = el("input", {
    class: "pt-label",
    type: "text",
    placeholder: "label",
  });
  ptLabel.value = opts.label ?? "";
  const dx = el("input", {
    class: "pt-offset",
    type: "number",
    value: opts.label_dx ?? 6,
    step: "1",
  });
  const dy = el("input", {
    class: "pt-offset",
    type: "number",
    value: opts.label_dy ?? 6,
    step: "1",
  });
  row.append(
    eqLine(
      lbl(displayLabels[0], c0),
      lbl(displayLabels[1], c1),
      lbl("Color", color, "color-grp"),
      removeBtn(container, row, c0, rerender),
    ),
    eqLine(
      lbl("Filled", filled, "mini-grp"),
      lbl("Label", ptLabel),
      lbl("dx", dx, "mini-grp"),
      lbl("dy", dy, "mini-grp"),
    ),
  );
  container.appendChild(row);
}

function readPointRow(r, c0Key, c1Key) {
  const offsets = r.querySelectorAll(".pt-offset");
  return {
    [c0Key]: Number.parseFloat(r.querySelector(".c0").value),
    [c1Key]: Number.parseFloat(r.querySelector(".c1").value),
    color: r.querySelector(".color").value,
    filled: r.querySelector(".filled").checked,
    label: r.querySelector(".pt-label").value,
    label_dx: Number.parseFloat(offsets[0]?.value || "6"),
    label_dy: Number.parseFloat(offsets[1]?.value || "6"),
    size: 7,
  };
}

export const getXYPoints = (container) =>
  [...container.querySelectorAll(".eq-row")].map((r) =>
    readPointRow(r, "x", "y"),
  );

export const getRTPoints = (container) =>
  [...container.querySelectorAll(".eq-row")].map((r) =>
    readPointRow(r, "r", "theta"),
  );

export function xyWindowSettings(prefix) {
  const xStep = num(`${prefix}-xstep`);
  const yStep = num(`${prefix}-ystep`);
  return {
    x0: num(`${prefix}-xmin`),
    x1: num(`${prefix}-xmax`),
    x_step: xStep,
    y0: num(`${prefix}-ymin`),
    y1: num(`${prefix}-ymax`),
    y_step: yStep,
    x_minor: xStep / 2,
    y_minor: yStep / 2,
  };
}

export function cartesianLikeStyleSettings(prefix) {
  return {
    line_width: num(`${prefix}-lw`),
    show_grid: chk(`${prefix}-grid`),
    show_minor_grid: chk(`${prefix}-minor-grid`),
    show_labels: chk(`${prefix}-tick-labels`),
    axis_arrows: chk(`${prefix}-arrows`),
    x_label: txt(`${prefix}-xlabel`),
    y_label: txt(`${prefix}-ylabel`),
  };
}
