import { bootAndMountPage } from "../../pyodide.js";
import { renderCartesian } from "./render.js";
import { setup } from "./setup.js";

await bootAndMountPage({
  files: [
    ["../../shared.py", "shared.py"],
    ["../../math_utils.py", "math_utils.py"],
    ["../../axis_utils.py", "axis_utils.py"],
    ["./__init__.py", "cartesian/__init__.py"],
  ],
  importName: "cartesian",
  exportName: "render_cartesian",
  fnKey: "cartesian",
  setup,
  render: renderCartesian,
});
