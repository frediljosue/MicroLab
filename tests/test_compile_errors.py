"""Compile errors and teaching warnings: students get the right message on the right line."""
import pytest
from conftest import run

CASES = {
 'missing_semicolon': 'void setup(){ pinMode(13, OUTPUT)\n  digitalWrite(13, HIGH); }\nvoid loop(){}',
 'undeclared': 'void setup(){ Serial.begin(9600); Serial.println(ledPin); }\nvoid loop(){}',
 'typo_fn': 'void setup(){ pinmode(13, OUTPUT); }\nvoid loop(){}',
 'no_loop': 'void setup(){ }',
 'unclosed': 'void setup(){ if (1) {\n}\nvoid loop(){}',
 'const_assign': 'const int LED = 13;\nvoid setup(){ LED = 12; }\nvoid loop(){}',
 'string_cond': 'String s = "a";\nvoid setup(){ if (s) {} }\nvoid loop(){}',
 'printf_avr': 'void setup(){ Serial.begin(9600);\n Serial.printf("%d", 5); }\nvoid loop(){}',
 'unknown_lib': '#include <Adafruit_BMP085.h>\nAdafruit_BMP085 bmp;\nvoid setup(){}\nvoid loop(){}',
 'code_outside': 'pinMode(13, OUTPUT);\nvoid setup(){}\nvoid loop(){}',
 'chars_dq': "void setup(){ char c = 'ab'; }\nvoid loop(){}",
 'bufsmall': 'char b[4] = "hello";\nvoid setup(){}\nvoid loop(){}',
 # runtime / warnings (should still run)
 'w_assign_if': 'int x = 0;\nvoid setup(){ Serial.begin(9600);\n if (x = 5) Serial.println("yes"); }\nvoid loop(){}',
 'w_overflow_const': 'void setup(){ Serial.begin(9600);\n unsigned long ms = 60 * 1000;\n Serial.println(ms); }\nvoid loop(){}',
 'w_oob': 'int a[3];\nvoid setup(){ Serial.begin(9600);\n for (int i = 0; i <= 3; i++) a[i] = i;\n Serial.println(a[2]); }\nvoid loop(){}',
 'w_ptr_add': 'int v = 5;\nvoid setup(){ Serial.begin(9600);\n Serial.println("Value: " + v); }\nvoid loop(){}',
 'w_div0': 'int z = 0;\nvoid setup(){ Serial.begin(9600);\n Serial.println(10 / z); }\nvoid loop(){}',
 'w_sprintf_f_avr': 'char buf[20];\nvoid setup(){ Serial.begin(9600);\n sprintf(buf, "T=%.1f", 21.5);\n Serial.println(buf); }\nvoid loop(){}',
 'w_semicolon_if': 'void setup(){ Serial.begin(9600);\n if (millis() > 99999999);\n Serial.println("always"); }\nvoid loop(){}',
 'w_charcmp': 'char a[] = "on";\nvoid setup(){ Serial.begin(9600);\n if (a == "on") Serial.println("same"); else Serial.println("diff"); }\nvoid loop(){}',
 'class_blinker': 'class Blinker {\n  int pin; unsigned long last = 0; bool on = false;\npublic:\n  Blinker(int p) : pin(p) {}\n  void begin(){ pinMode(pin, OUTPUT); }\n  void update(unsigned long now){ if (now - last >= 200){ last = now; on = !on; digitalWrite(pin, on); } }\n  bool state(){ return on; }\n};\nBlinker led(13);\nint flips = 0;\nvoid setup(){ Serial.begin(9600); led.begin(); }\nvoid loop(){ bool b = led.state(); led.update(millis()); if (b != led.state()) { flips++; if (flips == 3) Serial.println("3 flips"); } }',
 'enum_switch': 'enum State { IDLE, RUN, DONE };\nState st = IDLE;\nvoid setup(){ Serial.begin(9600); }\nvoid loop(){ switch (st) { case IDLE: Serial.println("idle"); st = RUN; break; case RUN: Serial.println("run"); st = DONE; break; default: break; } }',
 'typedef_struct': 'typedef struct { float t; int n; } Reading;\nReading r = {21.5, 3};\nReading copyOf(Reading x){ x.n = 99; return x; }\nvoid setup(){ Serial.begin(9600); Reading c = copyOf(r); Serial.println(r.n); Serial.println(c.n); Serial.println(r.t); }\nvoid loop(){}',
}

ERRORS = {
    "missing_semicolon": (1, "Expected ';'"),
    "undeclared": (1, "'ledPin' was not declared"),
    "typo_fn": (1, "Did you mean 'pinMode'?"),
    "no_loop": (1, "needs a void loop()"),
    "unclosed": (3, "never closed"),
    "const_assign": (2, "is const"),
    "string_cond": (2, "can’t be used as a condition"),
    "printf_avr": (2, "doesn't exist on AVR"),
    "unknown_lib": (2, "isn't simulated in MicroLab"),
    "code_outside": (1, "must be inside a function"),
    "chars_dq": (1, "Use \"double quotes\""),
    "bufsmall": (1, "needs 6 bytes"),
}
WARNINGS = {
    "w_assign_if": ("yes", "Did you mean ==?"),
    "w_overflow_const": ("4294961760", "overflows"),
    "w_oob": ("2", "outside the array"),
    "w_ptr_add": (":", "moves the text pointer"),
    "w_div0": ("-1", "Division by zero"),
    "w_sprintf_f_avr": ("T=?", "dtostrf"),
    "w_semicolon_if": ("always", "ends the if"),
    "w_charcmp": ("diff", "strcmp"),
}
RUNS = {"class_blinker": "3 flips", "enum_switch": "run", "typedef_struct": "3|99|21.50"}


@pytest.mark.parametrize("name", list(ERRORS))
def test_compile_error(lab, name):
    line, text = ERRORS[name]
    r = run(lab, CASES[name])
    assert r["errLine"] == line
    assert any(text in m and f"line {line}" in m for m in r["critical"]), r["critical"]


@pytest.mark.parametrize("name", list(WARNINGS))
def test_warning_and_still_runs(lab, name):
    out, text = WARNINGS[name]
    r = run(lab, CASES[name], ms=1200)
    assert r["lines"] and r["lines"][-1].rstrip() == out
    assert any(text in w["msg"] for w in r["warns"]), r["warns"]


@pytest.mark.parametrize("name", list(RUNS))
def test_language_features(lab, name):
    r = run(lab, CASES[name], ms=1200)
    assert not r["critical"], r["critical"]
    assert RUNS[name] in "|".join(l.rstrip() for l in r["lines"])
