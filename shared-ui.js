export const COLORS = [
  "#0000FF",
  "#FF0000",
  "#008000",
  "#FFA500",
  "#800080",
  "#008080",
];

export function nextColor(container) {
  return COLORS[container.querySelectorAll(".eq-row").length % COLORS.length];
}

export function el(tag, attrs = {}) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "text") e.textContent = v;
    else e.setAttribute(k, v);
  }
  return e;
}

export function styleSelect(selected = "solid", options = ["solid", "dashed"]) {
  const s = el("select", { class: "style", "aria-label": "Style" });
  for (const v of options) {
    const o = el("option", { value: v, text: v });
    if (v === selected) o.selected = true;
    s.appendChild(o);
  }
  return s;
}

export function lbl(text, input, extraClass = "") {
  const g = el("div", {
    class: "lbl-grp" + (extraClass ? " " + extraClass : ""),
  });
  const lab = el("label");
  lab.textContent = text;
  g.append(lab, input);
  return g;
}

export function eqLine(...children) {
  const d = el("div", { class: "eq-line" });
  d.append(...children);
  return d;
}

export function removeBtn(container, row, primaryInput, rerender) {
  const b = el("button", {
    class: "remove-btn",
    type: "button",
    "aria-label": "Remove",
  });
  b.textContent = "x";
  b.onclick = () => {
    if (container.querySelectorAll(".eq-row").length > 1) row.remove();
    else primaryInput.value = "";
    rerender();
  };
  return b;
}

function bindChange(id, handler) {
  document.getElementById(id)?.addEventListener("change", handler);
}

export function bindRerender(ids, rerender) {
  for (const id of ids) {
    bindChange(id, rerender);
  }
}

export const num = (id) => Number.parseFloat(document.getElementById(id).value);
export const chk = (id) => document.getElementById(id).checked;
export const txt = (id) => document.getElementById(id).value;
export const size = (prefix) => ({
  width: num(`${prefix}-width`),
  height: num(`${prefix}-height`),
});
