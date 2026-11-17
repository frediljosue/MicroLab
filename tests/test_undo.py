"""Undo / redo for circuit edits."""

FRESH = """() => { stop(); setBoard('uno'); comps = []; wires = []; bump(); clearTimeout(saveT); histRecord();
  HIST.undo = []; HIST.redo = []; HIST.cur = circuitKey(); histUI(); }"""
COUNT = "[comps.length, wires.length]"


def settle(lab):
    lab.wait_for_timeout(450)          # save() is debounced 300 ms


def test_undo_redo_add_wire_move_delete(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { window.__l = addComp('led', 700, 200); save(); })()"); settle(lab)
    lab.evaluate("(() => { addWire(__l.id + '.A', 'B.D13'); save(); })()"); settle(lab)
    lab.evaluate("(() => { __l.x = 900; bump(); save(); })()"); settle(lab)
    lab.evaluate("(() => { selected = {kind:'comp', id: __l.id}; deleteSelected(); })()"); settle(lab)
    assert lab.evaluate(COUNT) == [0, 0]
    lab.locator("#svgWrap").hover()
    lab.keyboard.press("Control+z"); assert lab.evaluate(COUNT) == [1, 1], "delete undone, wire comes back too"
    assert lab.evaluate("comps[0].x") == 900
    lab.keyboard.press("Control+z"); assert lab.evaluate("comps[0].x") == 700, "move undone"
    lab.keyboard.press("Control+z"); assert lab.evaluate(COUNT) == [1, 0]
    lab.keyboard.press("Control+z"); assert lab.evaluate(COUNT) == [0, 0]
    assert lab.is_disabled("#undoBtn")
    lab.keyboard.press("Control+Shift+z"); assert lab.evaluate(COUNT) == [1, 0]
    lab.keyboard.press("Control+y"); assert lab.evaluate(COUNT) == [1, 1]
    lab.click("#redoBtn"); lab.click("#redoBtn")
    assert lab.evaluate(COUNT) == [0, 0]
    assert lab.is_disabled("#redoBtn")
    lab.click("#undoBtn"); assert lab.evaluate(COUNT) == [1, 1]


def test_new_edit_clears_redo(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { addComp('led', 700, 200); save(); })()"); settle(lab)
    lab.click("#undoBtn"); assert not lab.is_disabled("#redoBtn")
    lab.evaluate("(() => { addComp('res', 700, 300); save(); })()"); settle(lab)
    assert lab.is_disabled("#redoBtn")


def test_undo_clear_circuit_and_rotation(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { const t = addComp('tft', 700, 200); save(); })()"); settle(lab)
    lab.evaluate("(() => { rotateComp(comps[0], 1); bump(); save(); })()"); settle(lab)
    lab.evaluate("(() => { comps = []; wires = []; bump(); save(); })()"); settle(lab)
    lab.click("#undoBtn"); assert lab.evaluate("comps.map(c => c.turn)") == [1]
    lab.click("#undoBtn"); assert lab.evaluate("comps[0].turn || 0") == 0


def test_undo_board_switch(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { addComp('led', 700, 200); addWire(comps[0].id + '.A', 'B.D13'); save(); })()"); settle(lab)
    lab.evaluate("setBoard('esp32')"); settle(lab)
    assert lab.evaluate("[boardKey, wires.length]") == ["esp32", 0]
    lab.click("#undoBtn")
    assert lab.evaluate("[boardKey, wires.length]") == ["uno", 1], "board and the wires it dropped both come back"


def test_ctrl_z_in_code_editor_is_text_undo(lab):
    lab.evaluate(FRESH)
    lab.evaluate("(() => { addComp('led', 700, 200); save(); })()"); settle(lab)
    lab.click("#code"); lab.keyboard.press("Control+z")
    assert lab.evaluate(COUNT) == [1, 0], "Ctrl+Z inside the editor must not undo the circuit"


def test_running_sketch_inputs_are_not_recorded_and_undo_is_locked(lab):
    lab.evaluate(FRESH)
    lab.evaluate("""(() => { const p = addComp('pot', 700, 200); addWire(p.id + '.W', 'B.A0'); addWire(p.id + '.VCC', 'B.5V'); addWire(p.id + '.GND', 'B.GND1');
      document.getElementById('code').value = 'void setup(){} void loop(){ analogRead(A0); delay(10); }'; save(); })()"""); settle(lab)
    n = lab.evaluate("HIST.undo.length")
    lab.click("#runBtn"); lab.wait_for_timeout(300)
    lab.evaluate("(() => { comps[0].props.pos = 0.9; bump(); save(); })()"); settle(lab)
    assert lab.evaluate("HIST.undo.length") == n
    lab.click("#undoBtn")
    assert lab.evaluate(COUNT) == [1, 3], "undo is locked while running"
    lab.click("#runBtn"); lab.wait_for_timeout(200)
