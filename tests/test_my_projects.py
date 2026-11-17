"""People can save their own projects by name, load them back, and move them around as files."""
import json

BUILD = """() => { stop(); localStorage.removeItem('microlab.projects'); setBoard('esp32'); setLang('cpp', true); comps = []; wires = [];
  const t = addComp('tft', 700, 300), l = addComp('led', 950, 200); rotateComp(t, 1);
  addWire(t.id + '.VCC', 'B.3V3'); addWire(l.id + '.K', 'B.GND1');
  document.getElementById('code').value = '// my racer\\nvoid setup(){}\\nvoid loop(){}'; bump(); save(); return [t.id, l.id]; }"""

BENCH = """(() => ({board: boardKey, lang: LANG, code: document.getElementById('code').value,
  comps: comps.map(c => [c.type, c.x, c.y, c.turn || 0]), wires: wires.map(w => [w.a, w.b])}))()"""


def test_save_load_from_the_projects_tab(lab):
    lab.evaluate(BUILD)
    before = lab.evaluate(BENCH)
    lab.click("#saveBtn")
    assert lab.evaluate("document.activeElement.id") == "mineName", "Save focuses the name box"
    lab.fill("#mineName", "My Racer")
    lab.click("#mineSave")
    assert lab.locator(".pcard.mine").count() == 1
    assert "My Racer" in lab.inner_text(".pcard.mine")
    # wipe the bench, then load the save back
    lab.evaluate("() => { closeLib(); setBoard('uno'); comps = []; wires = []; document.getElementById('code').value = ''; bump(); }")
    lab.click("#projBtn")
    lab.click(".pcard.mine [data-mact=load]")
    assert lab.evaluate(BENCH) == before
    assert not lab.is_visible("#lib .libwin")


def test_same_name_updates_instead_of_duplicating(lab):
    lab.evaluate(BUILD)
    lab.evaluate("saveMine('Racer')")
    lab.evaluate("document.getElementById('code').value = '// v2'; saveMine('racer')")
    saves = lab.evaluate("mineList()")
    assert len(saves) == 1
    assert saves[0]["name"] == "racer" and saves[0]["state"]["code"] == "// v2"
    lab.evaluate("saveMine('Second one')")
    assert [p["name"] for p in lab.evaluate("mineList()")] == ["Second one", "racer"]


def test_saves_survive_a_reload_and_delete_needs_two_clicks(lab):
    lab.evaluate(BUILD)
    lab.evaluate("saveMine('Keep me')")
    lab.reload(); lab.wait_for_function("typeof start === 'function'")
    lab.click("#projBtn")
    assert "Keep me" in lab.inner_text(".pcard.mine")
    lab.click(".pcard.mine [data-mact=del]")
    assert lab.locator(".pcard.mine").count() == 1, "first click only arms delete"
    lab.click(".pcard.mine [data-mact=del]")
    assert lab.locator(".pcard.mine").count() == 0
    lab.keyboard.press("Escape")


def test_download_and_open_file_round_trip(lab, tmp_path):
    lab.evaluate(BUILD)
    before = lab.evaluate(BENCH)
    lab.evaluate("saveMine('File test')")
    lab.click("#projBtn")
    with lab.expect_download() as dl:
        lab.click(".pcard.mine [data-mact=file]")
    path = tmp_path / dl.value.suggested_filename
    dl.value.save_as(path)
    assert dl.value.suggested_filename == "File-test.microlab.json"
    data = json.loads(path.read_text())
    assert data["format"] == "microlab-project" and data["name"] == "File test"

    # fresh browser storage, then open the file
    lab.evaluate("() => { localStorage.removeItem('microlab.projects'); setBoard('uno'); comps = []; wires = []; bump(); renderLib(); }")
    lab.set_input_files("#mineFile", str(path))
    lab.wait_for_function("mineList().length === 1")
    assert lab.evaluate(BENCH) == before
    assert lab.evaluate("mineList()[0].name") == "File test"


def test_bad_file_is_rejected_politely(lab, tmp_path):
    lab.evaluate(BUILD)
    before = lab.evaluate(BENCH)
    bad = tmp_path / "notes.json"; bad.write_text('{"hello": 1}')
    lab.click("#projBtn")
    lab.set_input_files("#mineFile", str(bad))
    lab.wait_for_timeout(200)
    assert lab.evaluate(BENCH) == before, "a bad file must not touch the bench"
    assert lab.evaluate("[...warnings.values()].some(w => /isn't a MicroLab project/.test(w.msg))")
    lab.keyboard.press("Escape")


def test_micropython_project_restores_its_language(lab):
    lab.evaluate("() => { stop(); localStorage.removeItem('microlab.projects'); setBoard('pico'); setLang('py', true); comps = []; wires = []; document.getElementById('code').value = 'print(\"hi\")'; }")
    lab.evaluate("saveMine('Py one')")
    lab.evaluate("() => { setLang('cpp', true); setBoard('uno'); }")
    lab.evaluate("loadMine(mineList()[0].id)")
    assert lab.evaluate("[boardKey, LANG, document.getElementById('code').value]") == ["pico", "py", 'print("hi")']
