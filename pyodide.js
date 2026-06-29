import { el } from "./shared-ui.js";

const svgState = {};

function appendWarnings(graphEl, warnings) {
  for (const warning of warnings) {
    const w = el("div", { class: "warning" });
    w.textContent = `Warning: ${warning}`;
    graphEl.appendChild(w);
  }
}

async function loadPyodideFiles(pyodide, files) {
  await Promise.all(
    files.map(async ([url, dst]) => {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status} ${res.statusText}`);
      const text = await res.text();
      if (dst.includes("/")) {
        pyodide.FS.mkdirTree("/home/pyodide/" + dst.slice(0, dst.lastIndexOf("/")));
      }
      pyodide.FS.writeFile("/home/pyodide/" + dst, text);
    }),
  );
}

async function bootPyodidePage({
  statusId = "status",
  files,
  importName,
  exportName,
}) {
  const statusEl = document.getElementById(statusId);

  try {
    statusEl.textContent = "Loading Pyodide...";
    const pyodide = await globalThis.loadPyodide();

    statusEl.textContent = "Loading packages...";
    await pyodide.loadPackage(["sympy", "matplotlib"]);

    statusEl.textContent = "Loading modules...";
    await loadPyodideFiles(pyodide, files);

    pyodide.runPython(`import ${importName}`);
    const fn = pyodide.runPython(`${importName}.${exportName}`);

    statusEl.remove();
    return { pyodide, fn };
  } catch (error) {
    statusEl.innerHTML = `<strong>Error:</strong> ${error.message}`;
    console.error(error);
    return null;
  }
}

export async function bootAndMountPage({
  statusId = "status",
  files,
  importName,
  exportName,
  fnKey,
  setup,
  render,
}) {
  const boot = await bootPyodidePage({
    statusId,
    files,
    importName,
    exportName,
  });

  if (!boot) {
    return null;
  }

  const fns = { [fnKey]: boot.fn };
  setup(boot.pyodide, fns);
  render(boot.pyodide, fns[fnKey]);
  return boot;
}

export function showResult(pid, result) {
  const errEl = document.getElementById(pid + "-error");
  const graphEl = document.getElementById(pid + "-graph");
  const dlBtn = document.getElementById(pid + "-dl");
  if (svgState[pid]) {
    URL.revokeObjectURL(svgState[pid]);
    svgState[pid] = null;
  }
  if (result.error) {
    errEl.textContent = result.error;
    graphEl.replaceChildren();
    dlBtn.disabled = true;
    return;
  }
  errEl.textContent = "";
  const warnings = Array.isArray(result.warnings) ? result.warnings : [];
  const { svg } = result;
  svgState[pid] = URL.createObjectURL(new Blob([svg], { type: "image/svg+xml" }));
  const img = el("img");
  img.src = svgState[pid];
  img.alt = "Graph";
  graphEl.replaceChildren();
  appendWarnings(graphEl, warnings);
  graphEl.appendChild(img);
  dlBtn.disabled = false;
  dlBtn.onclick = () => {
    const a = el("a");
    a.href = svgState[pid];
    a.download = pid + ".svg";
    a.click();
  };
}

export function callPython(pyodide, fn, settings) {
  const p = pyodide.toPy(settings);
  const proxy = fn(p);
  p.destroy();
  const result = proxy.toJs({ dict_converter: Object.fromEntries });
  proxy.destroy();
  return result;
}

export function renderToPanel(pyodide, fn, pid, settings) {
  showResult(pid, callPython(pyodide, fn, settings));
}
