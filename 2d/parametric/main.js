import { bootAndMountPage } from "../../pyodide.js";
import { renderParametric } from "./render.js";
import { setup } from "./setup.js";

await bootAndMountPage({
  files: [
    ["../../shared.py", "shared.py"],
    ["../../math_utils.py", "math_utils.py"],
    ["../../axis_utils.py", "axis_utils.py"],
    ["./__init__.py", "parametric/__init__.py"],
  ],
  importName: "parametric",
  exportName: "render_parametric",
  fnKey: "parametric",
  setup,
  render: renderParametric,
});
