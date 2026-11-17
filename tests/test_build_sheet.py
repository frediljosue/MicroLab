"""The Build it sheet: parts list, placement, wiring steps and code for building the circuit for real."""


def sheet(lab):
    return lab.evaluate("buildSheet()")


def test_racer_sheet(lab):
    lab.evaluate("() => { loadProject(PROJECTS.find(p => p.id === 'racer')); }")
    S = sheet(lab)
    assert ["ESP32 DevKit V1", 1] in S["bom"] and ["Push button", 2] in S["bom"] and ["Jumper wires", 18] in S["bom"]
    steps = [w["text"] for w in S["wiring"]]
    assert len(steps) == 18
    assert [w["group"] for w in S["wiring"]][:4] == ["Ground"] * 4, "ground wires come first"
    assert "Joystick GND → ESP32 pin GND" in steps, "no doubled part names"
    assert "TFT 2.8\" ILI9341 CS (chip select) → ESP32 pin GPIO15" in steps
    assert S["libs"] == ["Adafruit GFX Library", "Adafruit ILI9341"]
    assert "esp32 by Espressif" in S["core"]


def test_breadboard_placement_and_rails(lab):
    lab.evaluate("""() => { stop(); setBoard('uno'); comps = []; wires = [];
      const bb = addComp('bb', 400, 500), r = addComp('res', 0, 0, {ohms: 220});
      const h = nearestHole(bb, 480, 560); r.x = h.hx - DEFS.res.pins[0].x; r.y = h.hy - DEFS.res.pins[0].y; snapToBreadboard(r);
      const top = h.hy - 12;  addWire('B.D13', bb.id + '.a' + (h.i + 0)); addWire('B.GND1', bb.id + '.TN3'); bump(); }""")
    S = sheet(lab)
    assert ["Resistor, 220 Ω", 1] in S["bom"]
    assert S["place"] and "Resistor (220 Ω)" in S["place"][0] and "hole b" in S["place"][0]
    assert S["wiring"][0]["group"] == "Ground" and "top − rail" in S["wiring"][0]["text"]


def test_shared_pin_note_and_ui(lab, tmp_path):
    lab.evaluate("() => { loadProject(PROJECTS.find(p => p.id === 'weather')); }")
    S = sheet(lab)
    assert any("pin A4 has 2 wires" in n for n in S["notes"])
    lab.click("#buildBtn")
    assert "Build sheet: Arduino Uno R3" in lab.inner_text("#libBody")
    assert "already installed" not in lab.inner_text("#libBody")
    with lab.expect_download() as dl:
        lab.click("#bsDown")
    p = tmp_path / dl.value.suggested_filename; dl.value.save_as(p)
    html = p.read_text()
    assert html.startswith("<!DOCTYPE html>") and "Wires: signals" in html and "Copy as text" not in html
    text = lab.evaluate("buildText(buildSheet())")
    assert "WIRES: GROUND" in text and "#include <Adafruit_BME280.h>" in text
    lab.keyboard.press("Escape")


def test_empty_bench_and_micropython(lab):
    lab.evaluate("() => { stop(); comps = []; wires = []; bump(); }")
    lab.click("#buildBtn")
    assert "Add some parts" in lab.inner_text("#libBody")
    lab.keyboard.press("Escape")
    lab.evaluate("() => { setBoard('pico'); setLang('py', true); addComp('led', 700, 200); }")
    assert sheet(lab)["py"] is True
    assert "main.py" in lab.evaluate("buildText(buildSheet())")


def test_esp32_servo_note(lab):
    lab.evaluate("""() => { stop(); setBoard('esp32'); setLang('cpp', true); comps = []; wires = []; addComp('servo', 700, 200);
      document.getElementById('code').value = '#include <Servo.h>\\nvoid setup(){}\\nvoid loop(){}'; }""")
    assert any("ESP32Servo" in n for n in sheet(lab)["notes"])
