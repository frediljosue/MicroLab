"""MicroPython: language semantics, errors/tracebacks and the hardware modules."""
import pytest
from conftest import run

CASES = {
 'semantics': ('pico', [], [], '''print(7 / 2, 7 // 2, -7 // 2, -7 % 3, 2 ** 100)
print(0.1 + 0.2, 1 / 3, 3.0, 1e10, round(2.5), round(3.5), round(2.675, 2))
x = [1, 2, 3]
x.append(4)
print(x, x[-1], x[1:3], len(x), sum(x), x * 2)
d = {"a": 1, "b": 2}
d["c"] = 3
for k, v in d.items():
    print(k, v, end="; ")
print()
print(f"{3.14159:.2f} {42:05d} {'hi':>5}|", "%d-%s" % (7, "x"), "{} {}".format(1, 2))
s = "Hello, World"
print(s.upper(), s.split(", "), s[::-1], "World" in s, s.find("o"))
print([i * i for i in range(6) if i % 2 == 0], {k: v * 10 for k, v in d.items()})
print(int("42") + 1, float("2.5") * 2, str(10) + "!", bool([]), None, True + 1)
a, b = 1, 2
a, b = b, a
print(a, b, max(3, 9, 2), min([4, 1, 7]), abs(-3.5), divmod(17, 5), hex(255), bin(5))
print(sorted([3, 1, 2], reverse=True), list(enumerate("ab")), list(zip([1, 2], "xy")))
'''),
 'functions_classes': ('esp32', [], [], '''def area(w, h=2, *rest, scale=1, **opts):
    return w * h * scale, rest, opts

print(area(3), area(3, 4, 5, 6, scale=10, unit="cm"))

class Counter:
    total = 0
    def __init__(self, name, start=0):
        self.name = name
        self.n = start
    def bump(self, by=1):
        self.n += by
        Counter.total += by
        return self
    def __str__(self):
        return f"{self.name}={self.n}"

c = Counter("clicks")
c.bump().bump(5)
print(c, Counter.total, c.n)

count = 0
def inc():
    global count
    count += 1
inc(); inc()
print(count)
f = lambda x: x * 2
print(list(map(f, [1, 2, 3])), list(filter(lambda v: v > 1, [0, 1, 2, 3])))
'''),
 'exceptions': ('pico', [], [], '''try:
    x = [1, 2][5]
except IndexError as e:
    print("caught:", e)
try:
    int("abc")
except ValueError as e:
    print("caught:", e)
try:
    {}["k"]
except KeyError as e:
    print("caught key", e)
finally:
    print("finally ran")
def bad(n):
    return 10 / n
print("about to fail")
bad(0)
'''),
 'unbound': ('pico', [], [], '''count = 0
def inc():
    count += 1
inc()
'''),
 'syntax': ('pico', [], [], '''from machine import Pin
led = Pin(15, Pin.OUT)
while True
    led.toggle()
'''),
 'indent': ('pico', [], [], '''x = 1
if x:
print("no indent")
'''),
 'typeerr': ('pico', [], [], '''temp = 21
print("Temp: " + temp)
'''),
 'blink_pico': ('pico', [['res', 760, 300], ['led', 880, 230]], [['B.GP15','#0.1'],['#0.2','#1.A'],['#1.K','B.GND4']], '''from machine import Pin
import time
led = Pin(15, Pin.OUT)
for i in range(6):
    led.toggle()
    print("led", led.value())
    time.sleep(0.1)
'''),
 'adc_pico': ('pico', [['pot', 760, 480, {'pos': 0.25}]], [['#0.VCC','B.3V3'],['#0.GND','B.GND6'],['#0.OUT','B.GP26']], '''from machine import ADC, Pin
pot = ADC(Pin(26))
v = pot.read_u16()
print(v, round(v * 3.3 / 65535, 2))
t = ADC(4).read_u16() * 3.3 / 65535
print("temp", round(27 - (t - 0.706) / 0.001721, 1))
'''),
 'adc_esp32_atten': ('esp32', [['pot', 760, 480, {'pos': 0.6}]], [['#0.VCC','B.3V3'],['#0.GND','B.GND2'],['#0.OUT','B.G34']], '''from machine import ADC, Pin
a = ADC(Pin(34))
print(a.read())
b = ADC(Pin(34), atten=ADC.ATTN_11DB)
print(b.read())
'''),
 'dht22_esp32': ('esp32', [['dht22', 760, 480, {'temp': 26.4, 'hum': 61.2}]], [['#0.VCC','B.3V3'],['#0.GND','B.GND2'],['#0.DATA','B.G15']], '''from machine import Pin
import dht
s = dht.DHT22(Pin(15))
s.measure()
print(s.temperature(), s.humidity())
s2 = dht.DHT22(Pin(4))
try:
    s2.measure()
except OSError as e:
    print("err", e)
'''),
 'i2c_oled': ('pico', [['oled', 820, 440], ['bme', 720, 470]], [['#0.VCC','B.3V3'],['#0.GND','B.GND2'],['#0.SDA','B.GP4'],['#0.SCL','B.GP5'],['#1.VCC','B.3V3'],['#1.GND','B.GND3'],['#1.SDA','B.GP4'],['#1.SCL','B.GP5']], '''from machine import Pin, I2C
import ssd1306
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
print([hex(a) for a in i2c.scan()])
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.text("Hello Pico", 0, 0)
oled.show()
print("shown")
'''),
 'neopixel': ('esp32', [['neo', 820, 440]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.DIN','B.G16']], '''from machine import Pin
from neopixel import NeoPixel
np = NeoPixel(Pin(16), 8)
np[0] = (255, 0, 0)
np[7] = (0, 0, 255)
np.write()
print(np[0], len(np))
'''),
 'servo_pwm': ('pico', [['servo', 760, 480]], [['#0.VCC','B.VBUS'],['#0.GND','B.GND6'],['#0.SIG','B.GP16']], '''from machine import Pin, PWM
import time
s = PWM(Pin(16))
s.freq(50)
s.duty_u16(int(2400 / 20000 * 65535))
time.sleep(1)
print("done")
'''),
 'timer_irq': ('pico', [['button', 760, 300], ['res', 760, 200], ['led', 880, 150]], [['#0.1','B.GP14'],['#0.2','B.GND4'],['B.GP15','#1.1'],['#1.2','#2.A'],['#2.K','B.GND4']], '''from machine import Pin, Timer
import time
led = Pin(15, Pin.OUT)
ticks = 0
def tick(t):
    global ticks
    ticks += 1
tm = Timer(period=100, mode=Timer.PERIODIC, callback=tick)
presses = 0
def pressed(p):
    global presses
    presses += 1
btn = Pin(14, Pin.IN, Pin.PULL_UP)
btn.irq(handler=pressed, trigger=Pin.IRQ_FALLING)
time.sleep(1.5)
print("ticks>=10", ticks >= 10, "presses", presses)
'''),
}
BUTTON = "await wait(300); for (let k = 0; k < 6; k++){ const bt = comps.find(c => c.type === 'button'); bt.pressed = k % 2 === 0; bump(); await wait(150); } await wait(1300);"

EXPECT = {
    "semantics": ["3.5 3 -4 2 1267650600228229401496703205376", "0.3 0.3333333 3.0 1e+10 2 4", "[1, 2, 3, 4] 4 [2, 3] 4 10 [1, 2, 3, 4, 1, 2, 3, 4]",
                  "a 1; b 2; c 3;", "3.14 00042    hi| 7-x 1 2", "HELLO, WORLD ['Hello', 'World'] dlroW ,olleH True 4", "[0, 4, 16] {'a': 10, 'b': 20, 'c': 30}",
                  "43 5.0 10! False None 2", "2 1 9 1 3.5 (3, 2) 0xff 0b101", "[3, 2, 1] [(0, 'a'), (1, 'b')] [(1, 'x'), (2, 'y')]"],
    "functions_classes": ["(6, (), {}) (120, (5, 6), {'unit': 'cm'})", "clicks=6 6 6", "2", "[2, 4, 6] [2, 3]"],
    "exceptions": ["caught: list index out of range", "caught: invalid syntax for integer with base 10", "caught key k", "finally ran", "about to fail",
                   "Traceback (most recent call last):", '  File "main.py", line 18, in <module>', '  File "main.py", line 16, in bad', "ZeroDivisionError: divide by zero"],
    "unbound": ["NameError: local variable referenced before assignment"],
    "syntax": ["SyntaxError: expected ':'"],
    "indent": ["IndentationError: expected an indented block"],
    "typeerr": ["TypeError: unsupported types for __add__: 'str', 'int'"],
    "blink_pico": ["led 1", "led 0", "led 1", "led 0", "led 1", "led 0"],
    "adc_pico": ["temp 27.0"],
    "adc_esp32_atten": ["4095"],
    "dht22_esp32": ["26.4 61.2", "err [Errno 110] ETIMEDOUT"],
    "i2c_oled": ["['0x3c', '0x77']", "shown"],
    "neopixel": ["(255, 0, 0) 8"],
    "servo_pwm": ["done"],
    "timer_irq": ["ticks>=10 True presses 3"],
}


@pytest.mark.parametrize("name", list(CASES))
def test_micropython(lab, name):
    board, parts, wires, code = CASES[name]
    ms = 1600 if name == "servo_pwm" else 100 if name == "timer_irq" else 900
    r = run(lab, code, board, parts, wires, ms=ms, lang="py", act=BUTTON if name == "timer_irq" else None)
    text = "\n".join(l.rstrip() for l in r["lines"])
    for line in EXPECT[name]:
        if name == "semantics" and line.startswith("0.3 0.3333333"):
            assert line in text  # round(2.675, 2) is left out: float32 rounding there is not verified
        else:
            assert line in text, f"missing {line!r} in:\n{text}"
    if name == "servo_pwm":
        assert r["parts"][0]["angle"] > 170
    if name == "adc_pico":  # 0.25 of 3.3 V, with the ADC's real ±1-count noise
        raw, volts = r["lines"][0].split()
        assert 16100 < int(raw) < 16600 and 0.80 <= float(volts) <= 0.84
    if name == "adc_esp32_atten":
        assert 2400 < int(r["lines"][1]) < 2520
        assert any("ATTN_11DB" in w for w in r["warning"])
