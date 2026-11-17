"""Every Practice challenge's reference solution passes its checker (inputs driven the way a student would)."""
import pytest

DRIVE = {
    "button": "for (let k = 0; k < 16; k++){ const c = comps.find(c => c.type === 'button'); c.pressed = k % 2 === 0; bump(); await wait(350); }",
    "potservo": "for (let k = 0; k < 12; k++){ const c = comps.find(c => c.type === 'pot'); c.props.pos = [0.1, 0.5, 0.9][k % 3]; bump(); await wait(450); }",
    "night": "for (let k = 0; k < 8; k++){ const c = comps.find(c => c.type === 'ldr'); c.props.light = k % 2 ? 0.9 : 0.1; bump(); await wait(500); }",
    "parking": "for (let k = 0; k < 8; k++){ const c = comps.find(c => c.type === 'hc'); c.props.dist = k % 2 ? 80 : 10; bump(); await wait(600); }",
    "thermo": "for (let k = 0; k < 4; k++){ const c = comps.find(c => c.type === 'tmp'); c.props.temp = k % 2 ? 30 : 18; bump(); await wait(1200); }",
    "weather": "for (let k = 0; k < 4; k++){ const c = comps.find(c => c.type === 'dht'); c.props.temp = k % 2 ? 31 : 19; c.props.hum = k % 2 ? 70 : 40; bump(); await wait(2600); }",
    "motor": "for (let k = 0; k < 9; k++){ const c = comps.find(c => c.type === 'joy'); c.props.y = [0.05, 0.95, 0.5][k % 3]; bump(); await wait(1600); }",
    "alarm": "for (let k = 0; k < 6; k++){ const c = comps.find(c => c.type === 'pir'); c.props.hold = k % 2 === 0; bump(); await wait(k % 2 ? 2500 : 900); }",
    "keypad": "const c = comps.find(c => c.type === 'keypad'); for (const [r, col] of [[0,0],[1,1],[2,2],[3,3],[0,3]]){ c.keyDown = [r, col]; keyQueue.push({id:c.id, r, c:col}); obs.keys.push(KP[r][col]); bump(); await wait(300); c.keyDown = null; bump(); await wait(200); }",
}
AUTO = ["blink", "fade", "lcd", "oled", "neopixel", "transistor"]
JS = """async ([id, drive]) => { const wait = t => new Promise(r => setTimeout(r, t)); const c = CH.find(x => x.id === id);
  setBoard('uno'); completed.delete(id); activeCh = id; hist = []; loadSolution(c); warnings.clear(); void start(); await wait(600);
  if (drive) await (new Function('wait', 'return (async () => {' + drive + '})()'))(wait);
  let t = 0; while (t < 7000 && !completed.has(id)){ await wait(250); t += 250; }
  const ok = completed.has(id); stop(); activeCh = null; return ok; }"""


@pytest.mark.parametrize("cid", AUTO + list(DRIVE))
def test_challenge_solution_passes(lab, cid):
    assert lab.evaluate(JS, [cid, DRIVE.get(cid)])
