"""Data consistency (every part has an icon, info sheet and 3D model; every board has specs) and the main UI screens."""


def test_every_part_is_documented(lab):
    missing = lab.evaluate("""() => Object.keys(DEFS).flatMap(k => [
      ...(ICONS[k] ? [] : ['icon:' + k]), ...(partKeyInfo(k) ? [] : ['info:' + k]),
      ...(DISCRETE[k] || EXTRAS[k] || SLAB_H[k] || SLAB_RECT[k] || DEFS[k].fam === 'amod' || DEFS[k].fam === 'dmod' ? [] : ['3d:' + k])])""")
    assert not missing, missing


def test_info_sheets_point_at_real_parts(lab):
    assert lab.evaluate("PARTINFO.filter(p => p.k && !DEFS[p.k]).map(p => p.k)") == []


def test_every_board_has_specs_and_unique_pins(lab):
    problems = lab.evaluate("""() => Object.entries(BOARDS).flatMap(([k, b]) => {
      const out = BINFO[k] ? [] : ['no BINFO: ' + k], seen = new Set();
      for (const p of b.pins){ if (seen.has(p.id)) out.push(k + ' duplicate pin ' + p.id); seen.add(p.id); }
      return out; })""")
    assert not problems, problems


def test_library_tabs_render(lab):
    lab.click("#libBtn")
    for tab in ["boards", "compare", "parts", "projects", "learn"]:
        lab.click(f"[data-ltab={tab}]")
        assert len(lab.inner_text("#libBody")) > 200, tab
    lab.click("[data-lesson=ints]")
    lab.click("[data-qa='1']")
    assert "Correct." in lab.inner_text("#libBody")
    lab.click("#libClose")


def test_plotter_charts_serial_numbers(lab):
    lab.evaluate("""() => { setBoard('uno'); setLang('cpp', true); comps = []; wires = [];
      document.getElementById('code').value = 'int n = 0; void setup(){ Serial.begin(9600); } void loop(){ Serial.print("a:"); Serial.print(n % 10); Serial.print(" b:"); Serial.println(n * 2 % 7); n++; delay(30); }';
      void start(); }""")
    lab.click("[data-tab=plot]")
    lab.wait_for_timeout(1500)
    names = lab.evaluate("PLOT.series.map(s => s.name)")
    lab.evaluate("stop()")
    assert names == ["a", "b"]


def test_language_switch_keeps_both_programs(lab):
    lab.evaluate("setBoard('pico'); setLang('cpp', true); document.getElementById('code').value = '// my cpp'; setLang('py', true); document.getElementById('code').value = '# my py'; setLang('cpp', true)")
    assert lab.evaluate("document.getElementById('code').value") == "// my cpp"
    lab.evaluate("setLang('py', true)")
    assert lab.evaluate("document.getElementById('code').value") == "# my py"
    lab.evaluate("setBoard('uno')")  # MicroPython isn't available on the Uno, so the editor switches back
    assert lab.evaluate("LANG") == "cpp"
