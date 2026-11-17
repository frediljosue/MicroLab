"""Parts can be rotated in 90° steps. Pins, wires, breadboard holes and the 3D view follow."""
import pytest

from conftest import run

FRESH = "() => { stop(); setBoard('uno'); setLang('cpp', true); comps = []; wires = []; selected = null; renderInspector(); }"


def screen_rect(lab, cid):
    """The drawn part's box, and where compRect() says it is, both in screen pixels."""
    return lab.evaluate(f"""(() => {{
      bump(); render();
      const c = comps.find(x => x.id === '{cid}'), g = document.querySelector('[data-comp="{cid}"] g[filter]');
      const r = compRect(c), m = svg.getScreenCTM(), a = new DOMPoint(r.x, r.y).matrixTransform(m), b = new DOMPoint(r.x + r.w, r.y + r.h).matrixTransform(m);
      const hit = g.querySelector('rect').getBoundingClientRect();
      return {{hit: [hit.left, hit.top, hit.right, hit.bottom], rect: [a.x, a.y, b.x, b.y], scale: m.a}}; }})()""")


@pytest.mark.parametrize("turn", [0, 1, 2, 3])
def test_drawing_matches_pin_math(lab, turn):
    lab.evaluate(FRESH)
    cid = lab.evaluate(f"(() => {{ const c = addComp('tft', 700, 300); c.turn = {turn}; fit(); return c.id; }})()")
    lab.wait_for_timeout(150)
    r = screen_rect(lab, cid)
    # the invisible hit rectangle is 4 px bigger on three sides, so compare with that margin
    pad = 4 * r["scale"] + 1
    for got, want in zip(r["hit"], r["rect"]):
        assert abs(got - want) <= pad, (turn, r)
    # each pin dot sits where pinXY() puts it
    bad = lab.evaluate(f"""(() => {{ const c = comps.find(x => x.id === '{cid}'); return DEFS[c.type].pins.filter(p => {{
        const el = document.querySelector(`[data-pin="${{c.id}}.${{p.id}}"]`), q = pinXY(c, p);
        return Math.abs(+el.getAttribute('cx') - q.x) > .01 || Math.abs(+el.getAttribute('cy') - q.y) > .01; }}).map(p => p.id); }})()""")
    assert bad == []


def test_rotating_turns_pins_about_the_centre(lab):
    lab.evaluate(FRESH)
    out = lab.evaluate("""(() => {
      const c = addComp('oled', 700, 300), d = DEFS.oled, sda = d.pins.find(p => p.id === 'SDA');
      const r0 = compRect(c), c0 = [r0.x + r0.w / 2, r0.y + r0.h / 2], p0 = pinPos(c.id + '.SDA');
      rotateComp(c, 1);
      const r1 = compRect(c), c1 = [r1.x + r1.w / 2, r1.y + r1.h / 2], p1 = pinPos(c.id + '.SDA');
      rotateComp(c, 1); rotateComp(c, 1); rotateComp(c, 1);
      return {c0, c1, size0: [r0.w, r0.h], size1: [r1.w, r1.h], d0: [p0.dx, p0.dy], d1: [p1.dx, p1.dy], back: [c.x, c.y, c.turn]}; })()""")
    assert out["size1"] == out["size0"][::-1], "width and height swap after a quarter turn"
    assert all(abs(a - b) <= 2 for a, b in zip(out["c0"], out["c1"])), "the part turns about its centre"
    dx, dy = out["d0"]
    assert out["d1"] == [-dy, dx], "the wire's exit direction turns clockwise with the part"
    assert out["back"] == [700, 300, 0], "four turns bring it back exactly"


def test_r_key_and_inspector_buttons(lab):
    lab.evaluate(FRESH)
    cid = lab.evaluate("(() => { const c = addComp('tft', 700, 300); selected = {kind:'comp', id: c.id}; renderInspector(); fit(); return c.id; })()")
    turn = lambda: lab.evaluate(f"comps.find(c => c.id === '{cid}').turn || 0")
    lab.locator("#svgWrap").hover()
    lab.keyboard.press("r"); assert turn() == 1
    lab.keyboard.press("Shift+R"); lab.keyboard.press("Shift+R"); assert turn() == 3
    lab.click("#rotR"); assert turn() == 0
    lab.click("#rotL"); assert turn() == 3
    # the breadboard can't be rotated
    bb = lab.evaluate("(() => { const b = addComp('bb', 400, 600); selected = {kind:'comp', id: b.id}; renderInspector(); return b.id; })()")
    assert lab.locator("#rotR").count() == 0
    lab.keyboard.press("r")
    assert lab.evaluate(f"comps.find(c => c.id === '{bb}').turn || 0") == 0


def test_rotation_is_locked_while_running(lab):
    lab.evaluate(FRESH)
    cid = lab.evaluate("""(() => { const l = addComp('led', 900, 200); addWire(l.id + '.A', 'B.D13'); addWire(l.id + '.K', 'B.GND1');
      document.getElementById('code').value = 'void setup(){} void loop(){ delay(10); }'; selected = {kind:'comp', id: l.id}; renderInspector(); fit(); return l.id; })()""")
    lab.click("#runBtn"); lab.wait_for_timeout(300)
    lab.locator("#svgWrap").hover()
    lab.keyboard.press("r")
    assert lab.evaluate(f"comps.find(c => c.id === '{cid}').turn || 0") == 0
    lab.click("#runBtn"); lab.wait_for_timeout(200)


def test_rotated_parts_still_work(lab):
    # a rotated LED blinks, and a rotated TFT still draws
    r = run(lab, """#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
Adafruit_ILI9341 tft(15, 2, 4);
void setup(){ Serial.begin(115200); pinMode(13, OUTPUT); digitalWrite(13, HIGH); tft.begin(); tft.fillScreen(ILI9341_RED); Serial.println("ok"); }
void loop(){}""", board="esp32",
        parts=[["tft", 680, 330], ["led", 900, 200], ["res", 900, 120]],
        wires=[["#0.VCC", "B.3V3"], ["#0.GND", "B.GND2"], ["#0.CS", "B.G15"], ["#0.DC", "B.G2"], ["#0.RESET", "B.G4"], ["#0.MOSI", "B.G23"],
               ["#0.SCK", "B.G18"], ["#0.LED", "B.3V3"], ["#0.MISO", "B.G19"], ["#2.1", "B.G13"], ["#2.2", "#1.A"], ["#1.K", "B.GND1"]],
        act="for (const id of ids) rotateComp(comps.find(c => c.id === id), 1); bump(); await wait(300); const L = comps.find(c => c.id === ids[1]); window.__lit = !L.burnt && (vis[ids[1]] || {}).b > 0;")
    assert r["critical"] == []
    assert r["lines"] == ["ok"]
    assert lab.evaluate("window.__lit"), "current should flow through the rotated LED"


def test_breadboard_snap_after_rotation(lab):
    lab.evaluate(FRESH)
    out = lab.evaluate("""(() => {
      const bb = addComp('bb', 400, 500), r = addComp('res', 0, 0);
      const h = nearestHole(bb, 480, 560); r.x = h.hx - DEFS.res.pins[0].x; r.y = h.hy - DEFS.res.pins[0].y; snapToBreadboard(r);
      rotateComp(r, 1);
      return DEFS.res.pins.map(p => { const q = pinXY(r, p); return bbHoleAt(q.x, q.y); }); })()""")
    assert all(out), f"both resistor legs should sit in breadboard holes after rotating: {out}"
    assert out[0] != out[1]


def test_rotation_is_saved(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { const c = addComp('oled', 700, 300); rotateComp(c, 1); save(); })()")
    lab.wait_for_timeout(500)
    saved = lab.evaluate("JSON.parse(localStorage.getItem('mcusim.v2')).comps.map(c => c.turn)")
    assert saved == [1]
