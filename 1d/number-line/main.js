import { bootAndMountPage } from "../../pyodide.js";
import { render } from "./render.js";
import { setup } from "./setup.js";

await bootAndMountPage({
  files: [
    ["../../shared.py", "shared.py"],
    ["../../math_utils.py", "math_utils.py"],
    ["../../axis_utils.py", "axis_utils.py"],
    ["./number_line.py", "number_line.py"],
    ["./number_line_parse.py", "number_line_parse.py"],
    ["./number_line_draw.py", "number_line_draw.py"],
  ],
  importName: "number_line",
  exportName: "render_number_line",
  fnKey: "numberLine",
  setup,
  render,
});
