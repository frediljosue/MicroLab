# MicroLab tests

Browser tests with pytest + Playwright. They load `../index.html`, run sketches inside the page and check the output. Everything is offline: three.js comes from `node_modules`.

```bash
npm install
pip install -r requirements.txt
python -m playwright install chromium
python -m pytest -q            # about 4 minutes
CHROME_PATH=/usr/bin/google-chrome python -m pytest -q   # optional: use an installed Chrome
```

| File | What it checks |
|---|---|
| `test_cpp_semantics.py` | C/C++ rules: integer division, overflow, char, String, structs, references, sprintf… |
| `test_compile_errors.py` | compile errors point at the right line; teaching warnings fire and the sketch still runs |
| `test_parts.py` | each simulated part runs its library's example, and classic mistakes are caught |
| `test_boards.py` | every placeable board runs Blink + analogRead; board-specific rules |
| `test_challenges.py` | every challenge solution passes its checker |
| `test_projects_and_lessons.py` | every project's promised output; every lesson's try-it circuit |
| `test_micropython.py` | MicroPython semantics, errors and hardware modules |
| `test_registry_and_ui.py` | data consistency, library tabs, plotter, language switch |
