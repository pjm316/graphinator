import { bootAndMountPage } from "../../pyodide.js";
import { renderPolar } from "./render.js";
import { setup } from "./setup.js";

await bootAndMountPage({
  files: [
    ["../../shared.py", "shared.py"],
    ["../../math_utils.py", "math_utils.py"],
    ["../../axis_utils.py", "axis_utils.py"],
    ["./__init__.py", "polar/__init__.py"],
  ],
  importName: "polar",
  exportName: "render_polar",
  fnKey: "polar",
  setup,
  render: renderPolar,
});
