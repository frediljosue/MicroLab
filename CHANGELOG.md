# Changelog

## 2.2.0 — 2026-11-17
- **Practice keeps your board:** Load solution no longer switches to the Uno. Each solution is re-pinned for the board you picked: I²C goes to the board's SDA/SCL, analog inputs to ADC pins, other pins keep their number when they can, and flash, serial, input-only, analog-only and boot-strapping pins are skipped. On 3.3 V boards sensors run from 3V3, ADC math is scaled, and an HC-SR04 gets a 1 kΩ / 2 kΩ divider on ECHO. The console lists every pin that moved. If a board doesn't have enough free pins (keypad and robot on the ESP8266 / D1 Mini), it loads on the Uno and says why. Every solution is tested on the Uno, ESP32, Pico, Nano and Mega.
- **My projects:** press 💾 Save (or `Ctrl+S`), name what's on the bench, and it appears under ★ Projects with Load, Delete and rename (double-click the name). Saving again with the same name updates that save. Board, language, code, parts, rotation and wires are all kept.
- **Project files:** ⬇ File downloads a project as `.microlab.json` and ⬆ Open file brings it back, to back up, share, or move between devices.
- **Rotate parts:** select a part and press `R` (clockwise) or `Shift+R` (counter-clockwise), or use the Rotate buttons in the Inspector. Pins, wires, wire routing, breadboard holes, the 3D view and saved layouts all follow the rotation. The breadboard itself doesn't rotate, and rotation is locked while a sketch runs.
- Breadboard snapping now picks the position that seats the most legs in holes, so a resistor turned upright lands with both legs plugged in.

## 2.1.0 — 2026-11-17
- New project: **Retro Racer**, a color TFT game for ESP32 with joystick and buttons, using flicker-free partial redraws.
- **Layout lock while running:** parts and wires can't be moved, added, rewired or deleted by accident while a sketch runs. Buttons, keypads, knobs, joysticks and the Inspector still work. A "Layout locked while running" badge shows next to the 2D/3D switch; press Stop to rearrange.
- Fix: a wire's invisible click band could cover a push button or keypad and swallow the press. Controls now win over overlapping wires.

## 2.0.0 — 2026-11-16
- **C++ compiler** replaces the regex translator: per-board integer sizes, integer division, overflow warnings, `char`, structs, classes, references, `static` locals, `sizeof`, `sprintf`/`dtostrf`, and compile errors with line numbers and suggestions.
- **MicroPython** on Pico and ESP boards: `machine`, `time`, `math`, `random`, `dht`, `neopixel`, `ssd1306`; MicroPython-style tracebacks.
- **Monitor tab**: serial plotter and live pin/part dashboard.
- **Projects** (9) and **Learn** (12 lessons with try-it circuits and quizzes).
- I²C scanning via `Wire.beginTransmission`/`endTransmission`.
- Spec corrections (UNO R4 WiFi USB path, Pico W Bluetooth, ESP32 hall sensor, PIR current, sound sensor pins); missing info sheets and 3D models added.
- GPS buffer overflow only reported when the sketch's own `delay()` causes it.

## 1.0.0 — 2026-11-16
- Renamed to MicroLab. 25 boards with specs, clickable pinouts and comparison; component library with 75 info sheets; 13 new simulated parts (BME280, MPU6050, DS3231, HX711, PCA9685, NEO-6M GPS, microSD, ILI9341, DHT22, MQ-135, MG90S, MG995, bench supply).
