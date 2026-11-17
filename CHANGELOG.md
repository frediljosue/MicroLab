# Changelog

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
