"""C/C++ semantics: MicroLab compiles sketches with the real rules of the selected board."""
import pytest
from conftest import run

CASES = {
 'intdiv': ('uno', 'void setup(){ Serial.begin(9600); int a = 7; int b = 2; Serial.println(a / b); Serial.println(7 / 2); float f = 7 / 2; Serial.println(f); Serial.println(7.0 / 2); long m = -7 / 2; Serial.println(m); Serial.println(-7 % 3); } void loop(){}', '3|3|3.00|3.50|-3|-1'),
 'overflow_avr': ('uno', 'void setup(){ Serial.begin(9600); int x = 32767; x = x + 1; Serial.println(x); byte b = 255; b++; Serial.println(b); unsigned int u = 0; u--; Serial.println(u); } void loop(){}', '-32768|0|65535'),
 'overflow_esp': ('esp32', 'void setup(){ Serial.begin(115200); int x = 32767; x = x + 1; Serial.println(x); } void loop(){}', '32768'),
 'char_math': ('uno', "void setup(){ Serial.begin(9600); char c = 'A'; c = c + 2; Serial.println(c); Serial.println((int)c); Serial.println('0' + 5); } void loop(){}", 'C|67|53'),
 'print_fmt': ('uno', 'void setup(){ Serial.begin(9600); Serial.println(255, HEX); Serial.println(5, BIN); Serial.println(3.14159, 3); Serial.println(2.5); Serial.print("a"); Serial.println(); } void loop(){}', 'FF|101|3.142|2.50|a'),
 'string_ops': ('uno', 'void setup(){ Serial.begin(9600); String s = "Temp: "; s += 21; s += "C"; Serial.println(s); Serial.println(s.length()); Serial.println(s.substring(0,4)); Serial.println(String(3.14159, 2)); Serial.println(s.indexOf("21")); } void loop(){}', 'Temp: 21C|9|Temp|3.14|6'),
 'static_ref': ('uno', 'void bump(int &v){ v += 10; } int counter(){ static int n = 0; n++; return n; } void setup(){ Serial.begin(9600); int a = 1; bump(a); Serial.println(a); counter(); counter(); Serial.println(counter()); } void loop(){}', '11|3'),
 'arrays_switch': ('uno', 'int pins[] = {2, 3, 4}; const int N = sizeof(pins) / sizeof(pins[0]); void setup(){ Serial.begin(9600); Serial.println(N); for (int i = 0; i < N; i++){ switch (pins[i]) { case 2: Serial.println("two"); break; case 3: Serial.println("three"); break; default: Serial.println("other"); } } } void loop(){}', '3|two|three|other'),
 'macros': ('uno', '#define SQ(x) ((x) * (x))\n#define LED 13\nvoid setup(){ Serial.begin(9600); Serial.println(SQ(4)); Serial.println(LED); Serial.println(bitRead(5, 2)); Serial.println(map(512, 0, 1023, 0, 255)); Serial.println(constrain(300, 0, 255)); } void loop(){}', '16|13|1|127|255'),
 'sprintf': ('uno', 'char buf[20]; void setup(){ Serial.begin(9600); sprintf(buf, "T=%d H=%d", 21, 55); Serial.println(buf); } void loop(){}', 'T=21 H=55'),
 'printf_esp': ('esp32', 'void setup(){ Serial.begin(115200); Serial.printf("v=%d %.1f\\n", 3, 2.25); } void loop(){}', 'v=3 2.2'),
 'struct': ('uno', 'struct Pt { int x; int y; }; Pt p = {3, 4}; void setup(){ Serial.begin(9600); Serial.println(p.x + p.y); } void loop(){}', '7'),
 'millis_timing': ('uno', 'unsigned long last = 0; int n = 0; void setup(){ Serial.begin(9600); } void loop(){ if (millis() - last >= 200){ last = millis(); n++; if (n == 3) Serial.println("tick3"); } }', 'tick3'),
 'while_serial': ('uno', 'void setup(){ Serial.begin(9600); while (!Serial) { } Serial.println("ready"); } void loop(){}', 'ready'),
 'float_to_int': ('uno', 'void setup(){ Serial.begin(9600); float f = 3.99; int i = f; Serial.println(i); int j = (int)(-2.7); Serial.println(j); Serial.println(round(2.5)); } void loop(){}', '3|-2|3'),
}

@pytest.mark.parametrize("name", list(CASES))
def test_semantics(lab, name):
    board, code, expected = CASES[name]
    r = run(lab, code, board)
    assert not r["critical"], r["critical"]
    assert "|".join(l.rstrip() for l in r["lines"]) == expected
