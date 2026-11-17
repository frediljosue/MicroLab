"""While a sketch runs, parts can't be moved or rewired by accident, but inputs still work."""

SETUP = """() => { stop(); setBoard('uno'); setLang('cpp', true); comps = []; wires = [];
  const b = addComp('button', 820, 330), l = addComp('led', 900, 200);
  addWire(b.id + '.1', 'B.D2'); addWire(b.id + '.2', 'B.GND1');
  document.getElementById('code').value = 'void setup(){ Serial.begin(9600); pinMode(2, INPUT_PULLUP); } void loop(){ Serial.println(digitalRead(2) == LOW ? "pressed" : "released"); delay(50); }';
  fit(); return [b.id, l.id]; }"""


def center(lab, sel):
    box = lab.locator(sel).first.bounding_box()
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


def drag(lab, sel, dx=120, dy=60):
    x, y = center(lab, sel)
    lab.mouse.move(x, y); lab.mouse.down(); lab.mouse.move(x + dx / 2, y + dy / 2, steps=4); lab.mouse.move(x + dx, y + dy, steps=4); lab.mouse.up()


def pos(lab, cid):
    return lab.evaluate(f"(() => {{ const c = comps.find(c => c.id === '{cid}'); return [c.x, c.y]; }})()")


def test_parts_locked_while_running_and_free_after_stop(lab):
    lab.click("[data-tab=serial]")
    bid, lid = lab.evaluate(SETUP)
    lab.wait_for_timeout(300)
    lab.click("#runBtn"); lab.wait_for_timeout(400)
    assert lab.is_visible("#lockBadge")

    before = pos(lab, lid)
    drag(lab, f"[data-comp='{lid}']")
    assert pos(lab, lid) == before, "LED moved while the sketch was running"

    wires_before = lab.evaluate("wires.length")
    lab.click("[data-pin='B.D7']"); lab.click(f"[data-pin='{lid}.A']")
    assert lab.evaluate("wires.length") == wires_before, "a wire was added while running"

    lab.evaluate(f"selected = {{kind:'comp', id:'{lid}'}}"); lab.keyboard.press("Delete")
    assert lab.evaluate(f"comps.some(c => c.id === '{lid}')"), "a part was deleted while running"

    x, y = center(lab, f"[data-press='{bid}']")       # pressing the button still works
    lab.mouse.move(x, y); lab.mouse.down(); lab.wait_for_timeout(250)
    assert "pressed" in lab.evaluate("document.getElementById('serialOut').textContent.trim().split('\\n').slice(-2).join(' ') + serialBuf")
    lab.mouse.up()
    assert any("locked while the sketch runs" in m for m in lab.evaluate("[...warnings.values()].map(w => w.msg)"))

    lab.click("#runBtn"); lab.wait_for_timeout(200)   # Stop
    assert not lab.is_visible("#lockBadge")
    drag(lab, f"[data-comp='{lid}']")
    assert pos(lab, lid) != before, "LED should move after Stop"
