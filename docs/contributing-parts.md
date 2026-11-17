# Adding boards, parts, projects and lessons

Everything lives in `index.html`. Search for the names below. After any change, run the tests (`cd tests && python -m pytest -q`); `test_registry_and_ui.py` fails if a part is missing an icon, info sheet or 3D model.

## A new part

1. **`DEFS`**: name, category, size and pins. `pn(id, x, y, label)` places a pin.
2. **`ART2`**: the 2D drawing (an SVG string built with the `Y` helpers).
3. **`ICONS`**: the small palette icon.
4. **3D**: a model in `DISCRETE` or `EXTRAS`, or a flat module via `SLAB_H` / `SLAB_COL` / `SLAB_RECT`.
5. **Behaviour**: a `case` in the visuals switch (`V[c.id] = ...`) for what it shows, plus warnings for wrong wiring.
6. **Library** (if code talks to it): a class inside `makeApi()`, its name in `CLASSES`, and for I²C parts an entry in `I2C_TYPES` so address clashes and scanners see it.
7. **`PARTINFO`**: the info sheet with `PI({...})`: what it does, pins, voltage, current, protocol, libraries, wiring, mistakes, limits, uses and a source. Use ≈ and `vary:true` for numbers that differ between modules.
8. **Live reading**: a `case` in `liveText()` for the Inspector and Monitor.
9. **A test**: a library example sketch in `tests/test_parts.py`.

## A new board

1. **`BOARDS`**: pin rows with `P(id, label, kind, num, flags)`, plus `fam`, `logic`, `adcBits`, `pinMaxmA` and `consts` (A0, LED_BUILTIN, SDA…).
2. **`BINFO`**: the spec sheet. Fill `unc` with anything you couldn't confirm from the manufacturer and `src` with links.
3. **`BOARD_GROUPS`**: add it to the board menu (skip this for `refOnly` boards).
4. **Test**: add its key to `test_board_blink_and_adc` in `tests/test_boards.py`.

## A new project

Add an entry to `PROJECTS` with `board`, optional `lang:'py'`, `comps` (`[type, x, y, props]`), `wires` (`'#0.VCC'` = first part's VCC, `'B.5V'` = the board's 5V pin), `code`, and an `expect` that the test can verify (`serial`, `files`, `lcd` regexes or `servoMoves`). Then add its id to `tests/test_projects_and_lessons.py`.

## A new lesson

Add an entry to `LESSONS`: `body` (2–3 short paragraphs), `formula`, `tryit` (a small circuit + code + steps) and a `quiz` with one correct answer and an explanation. Keep the wording plain; the audience is students meeting the idea for the first time.
