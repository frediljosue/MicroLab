"""Every gallery project produces what its card promises, and every lesson's try-it circuit runs."""
import pytest

PROJECT = """async (id) => { const wait = t => new Promise(r => setTimeout(r, t)); const pr = PROJECTS.find(p => p.id === id);
  loadProject(pr); document.getElementById('serialOut').textContent = ''; warnings.clear(); void start();
  const a0 = comps.filter(c => c.type === 'servo').map(c => c.angle);
  if (pr.expect && pr.expect.act) await (new Function('wait', 'return (async () => {' + pr.expect.act + '})()'))(wait);
  await wait(id === 'logger' ? 4800 : id === 'gpsspeed' ? 3500 : 2600);
  const ser = document.getElementById('serialOut').textContent + serialBuf;
  const sd = comps.find(c => c.type === 'sd'), files = sd ? JSON.stringify(sd.props.files) : '';
  const lcdO = lcdObjs[0], lcd = lcdO && lcdO.buf ? lcdO.buf.map(r => r.join('')).join(' / ') : '';
  const a1 = comps.filter(c => c.type === 'servo').map(c => c.angle), e = pr.expect || {}, checks = {};
  if (e.serial) checks.serial = e.serial.test(ser); if (e.files) checks.files = e.files.test(files); if (e.lcd) checks.lcd = e.lcd.test(lcd);
  if (e.servoMoves) checks.servo = a1.every((v, i) => v != null && Math.abs(v - (a0[i] ?? 90)) > 5);
  const critical = [...warnings.values()].filter(x => x.level === 'critical').map(x => x.msg); stop();
  return {checks, critical, tail: ser.trim().split('\\n').slice(-2)}; }"""
LESSON = """async (id) => { const wait = t => new Promise(r => setTimeout(r, t)); const l = LESSONS.find(x => x.id === id);
  loadProject({title:l.title, board:l.tryit.board, comps:l.tryit.comps, wires:l.tryit.wires, code:l.tryit.code});
  document.getElementById('serialOut').textContent = ''; warnings.clear(); void start(); await wait(1500);
  const r = {ser: (document.getElementById('serialOut').textContent + serialBuf).trim(), warns: [...warnings.values()].filter(x => x.level !== 'ok').map(x => x.msg)}; stop(); return r; }"""
LESSON_EXPECT = {
    "pullup": ("released", None), "adc": ("raw:", None), "ints": ("-32768", "overflows"), "i2c": ("Device at 0x68", None), "spi": ("Wrote HELLO.TXT", None),
    "uart": (", -80.19", None), "levels": ("4095", "only goes up to 3.3 V"), "power": ("", "MG995"),
}


def ids(lab, what):
    return lab.evaluate(f"{what}.map(x => x.id)")


@pytest.mark.parametrize("pid", ["weather", "gpsspeed", "logger", "scale", "tilt", "servos", "nightlight", "mpweather", "airq", "racer"])
def test_project(lab, pid):
    r = lab.evaluate(PROJECT, pid)
    assert r["checks"] and all(r["checks"].values()), r
    assert not r["critical"], r["critical"]


@pytest.mark.parametrize("lid", ["ohm", "pullup", "adc", "pwm", "millis", "ints", "i2c", "spi", "uart", "levels", "power", "debounce"])
def test_lesson_tryit(lab, lid):
    r = lab.evaluate(LESSON, lid)
    out, warn = LESSON_EXPECT.get(lid, ("", None))
    assert out in r["ser"], r
    if warn:
        assert any(warn in w for w in r["warns"]), r["warns"]


def test_every_project_and_lesson_is_tested(lab):
    assert len(ids(lab, "PROJECTS")) == 10 and len(ids(lab, "LESSONS")) == 12
