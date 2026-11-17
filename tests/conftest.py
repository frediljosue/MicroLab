"""Shared helpers for the MicroLab browser tests.

Everything runs offline: three.js (used by the 3D view) is served from
tests/node_modules instead of the CDN, and every sketch runs inside the page.
"""
import os
import pathlib

import pytest
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
APP = (ROOT / "index.html").as_uri()
THREE = HERE / "node_modules" / "three"
CHROME_ARGS = ["--use-angle=swiftshader", "--enable-unsafe-swiftshader"]


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        exe = os.environ.get("CHROME_PATH")  # optional: use an installed Chrome
        b = p.chromium.launch(executable_path=exe or None, args=CHROME_ARGS)
        yield b
        b.close()


def _serve_three(route):
    rel = route.request.url.split("three@0.128.0/", 1)[1].split("?")[0]
    route.fulfill(path=str(THREE / rel))


@pytest.fixture(scope="module")
def lab(browser):
    """One MicroLab page per test file. JavaScript errors are collected in lab.errors."""
    ctx = browser.new_context(viewport={"width": 1600, "height": 950})
    page = ctx.new_page()
    page.errors = []
    page.on("pageerror", lambda e: page.errors.append(str(e)))
    page.route("**/three@0.128.0/**", _serve_three)
    page.goto(APP)
    page.wait_for_function("typeof start === 'function' && typeof CPP === 'object'")
    yield page
    assert not page.errors, f"JavaScript errors on the page: {page.errors}"
    ctx.close()


RUN = """async ([board, lang, parts, wl, code, ms, act]) => {
  const wait = t => new Promise(r => setTimeout(r, t));
  setBoard(board); setLang(lang, true); comps = []; wires = [];
  const ids = parts.map(([t, x, y, pr]) => addComp(t, x, y, pr || {}).id);
  for (const [a, b] of wl) addWire(a.replace(/#(\\d+)/, (_, i) => ids[i]), b.replace(/#(\\d+)/, (_, i) => ids[i]));
  document.getElementById('code').value = code; document.getElementById('serialOut').textContent = ''; warnings.clear();
  lastCompileErr = null; void start(); await wait(ms);
  if (act) await (new Function('ids', 'wait', 'return (async () => {' + act + '})()'))(ids, wait);
  serialBuf && (document.getElementById('serialOut').textContent += serialBuf, serialBuf = '');
  const out = document.getElementById('serialOut').textContent.replace(/\\r/g, '');
  const warns = [...warnings.values()].filter(x => x.level !== 'ok').map(x => ({level: x.level, msg: x.msg}));
  const parts2 = ids.map(id => { const c = comps.find(x => x.id === id); return {type: c.type, angle: c.angle ?? null, files: c.props.files || null}; });
  const errLine = lastCompileErr; stop();
  return {out, lines: out.trim() ? out.trim().split('\\n') : [], warns, parts: parts2, errLine}; }"""


def run(page, code, board="uno", parts=(), wires=(), ms=900, lang="cpp", act=None):
    """Load a circuit + sketch, run it for `ms` milliseconds and return serial output and warnings."""
    r = page.evaluate(RUN, [board, lang, list(parts), list(wires), code, ms, act])
    r["critical"] = [w["msg"] for w in r["warns"] if w["level"] == "critical"]
    r["warning"] = [w["msg"] for w in r["warns"] if w["level"] == "warning"]
    return r
