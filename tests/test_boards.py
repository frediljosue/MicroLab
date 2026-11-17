"""Every placeable board runs Blink + analogRead, and board-specific rules are enforced."""
import pytest
from conftest import run

BOARD_RUN = """async (k) => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  setBoard(k); setLang('cpp', true); comps = []; wires = []; const b = B();
  const g = b.pins.find(p => p.kind === 'GND'), gpio = b.pins.find(p => p.kind === 'gpio' && !p.flash && !p.inOnly && !p.anaOnly && !p.strap && !(b.serialPins||[]).includes(p.num) && p.num !== b.led);
  const adc = b.pins.find(p => p.kind === 'gpio' && p.adc), v = b.pins.find(p => p.kind === '3V3') || b.pins.find(p => p.kind === '5V');
  const r = addComp('res', 700, 300), l = addComp('led', 820, 240), pot = addComp('pot', 900, 520);
  addWire('B.' + gpio.id, r.id + '.1'); addWire(r.id + '.2', l.id + '.A'); addWire(l.id + '.K', 'B.' + g.id);
  if (adc && v){ addWire(pot.id + '.VCC', 'B.' + v.id); addWire(pot.id + '.GND', 'B.' + g.id); addWire(pot.id + '.OUT', 'B.' + adc.id); }
  document.getElementById('code').value = `void setup(){ Serial.begin(115200); pinMode(${gpio.num}, OUTPUT); }
void loop(){ digitalWrite(${gpio.num}, HIGH); ${adc ? `Serial.println(analogRead(${adc.num}));` : ''} delay(100); }`;
  document.getElementById('serialOut').textContent = ''; warnings.clear();
  void start(); await wait(700);
  const res = {led: (vis[l.id] || {}).b || 0, hasAdc: !!adc, serial: (document.getElementById('serialOut').textContent + serialBuf).trim().split('\\n').slice(-1)[0],
    critical: [...warnings.values()].filter(x => x.level === 'critical').map(x => x.msg)};
  stop(); return res; }"""


def boards(lab):
    return lab.evaluate("BOARD_GROUPS.flatMap(g => g[1])")


def test_board_count(lab):
    assert len(boards(lab)) == 23
    assert lab.evaluate("Object.keys(BINFO).length") == 25


@pytest.mark.parametrize("key", ["uno", "r4wifi", "nano", "mega", "leonardo", "micro", "promini", "due", "esp32", "wroom32", "s3", "c3", "esp8266",
                                 "d1mini", "xiao", "pico", "picow", "pico2", "pico2w", "bluepill", "nucleo", "teensy40", "teensy41"])
def test_board_blink_and_adc(lab, key):
    r = lab.evaluate(BOARD_RUN, key)
    assert not r["critical"], r["critical"]
    assert r["led"] > 0
    if r["hasAdc"]:
        assert r["serial"].isdigit(), r


def test_leonardo_a6_alias(lab):
    r = run(lab, "void setup(){ Serial.begin(9600); } void loop(){ Serial.println(analogRead(A6)); delay(50); }", "leonardo",
            [["pot", 800, 500, {"pos": 0.25}]], [["#0.VCC", "B.5V"], ["#0.GND", "B.GND2"], ["#0.OUT", "B.D4"]], ms=500)
    assert 230 < int(r["lines"][-1]) < 290


def test_due_rejects_5v(lab):
    r = run(lab, "void setup(){} void loop(){ delay(10); }", "due", [], [["B.5V", "B.D7"]], ms=300)
    assert any("3.3 V" in m for m in r["critical"])


def test_r4_pin_current_limit(lab):
    r = run(lab, "void setup(){ pinMode(9, OUTPUT); digitalWrite(9, HIGH); } void loop(){ delay(10); }", "r4wifi",
            [["res", 700, 300, {"ohms": 220}], ["led", 820, 240]], [["B.D9", "#0.1"], ["#0.2", "#1.A"], ["#1.K", "B.GND2"]], ms=300)
    assert any("8 mA" in w["msg"] for w in r["warns"])
