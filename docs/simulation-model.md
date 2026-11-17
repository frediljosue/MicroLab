# What MicroLab simulates, and how accurately

MicroLab is a teaching tool. It aims to be **right about the things beginners get wrong** and **honest about what it leaves out**.

## Electrical model

- Every wire, breadboard strip and part pin is merged into *nets*. Each net knows whether it is driven by a pin, a supply rail, a pull-up/pull-down or nothing at all (floating).
- **Currents** through LEDs, lamps and resistors use Ohm's law with typical forward voltages (red ≈ 2.0 V, blue/white ≈ 3.0 V).
- **Per-board limits** come from the datasheets: for example 20 mA recommended per Uno pin, 8 mA on the UNO R4, 4 mA recommended on Teensy 4, and inputs that are **not 5 V tolerant** on ESP32, Pico, Teensy 4 and Due.
- Motors, servos, relays and LED strips check where their power comes from. A servo on a GPIO pin, an MG995 on USB power, or a missing shared ground each produce a specific warning.

**Simplified:** exact timing, analog noise (only a small ±1-count ADC jitter), temperature and heat, rise times, ESD, battery discharge, and inrush currents.

## Buses and protocols

- **I²C**: devices answer at their real addresses (BME280 0x76/0x77, MPU6050 0x68/0x69 via AD0, DS3231 0x68 plus its module EEPROM at 0x57…). Clashes, swapped SDA/SCL and unpowered devices are detected. `Wire.beginTransmission`/`endTransmission` work, so I²C scanner sketches find real addresses.
- **SPI**: CS/MOSI/MISO/SCK wiring is checked against your code. SD cards keep a real file list you can read in the Inspector. Files are only written after `close()` or `flush()`.
- **UART**: a GPS module streams real NMEA sentences at 9600 baud into a buffer of the real size (64 bytes for SoftwareSerial, 256 for ESP32 hardware serial). Sketches that stall in `delay()` lose data and fail checksums, as on hardware.

## Languages

### Arduino C++

Sketches are compiled by a small typed C++ compiler, not a find-and-replace translator:

| Rule | Example |
|---|---|
| Integer sizes follow the board | `int` is 16-bit on AVR, 32-bit elsewhere |
| Integer division truncates | `7 / 2` is `3`, `7.0 / 2` is `3.5` |
| Overflow wraps, with a warning | `60 * 1000` on an Uno becomes `-5536` |
| Signed/unsigned conversions | `-1 < 1u` behaves as in C |
| `char` is a number | `'A' + 2` is `67`; printing a `char` prints a letter |
| Text pitfalls | `"Value: " + 5` skips letters; `==` on char arrays compares addresses |
| AVR `sprintf` has no `%f` | prints `?`, as on a real Uno |

Supported: functions, references, default arguments, `static` locals, arrays (multi-dimensional), `struct`, simple `class` (constructors, initializer lists, methods), `enum`, `typedef`, `#define` (including function-like macros), `#if/#ifdef` with board macros (`ESP32`, `__AVR__`…), `sizeof`, `String`, `sprintf`/`snprintf`/`dtostrf`/`strcpy`/…

Not supported (yet): templates, inheritance, overloading, `new`/`delete`, exceptions, pointer arithmetic, function pointers other than passing a function name.

### MicroPython

A MicroPython subset with MicroPython's semantics: arbitrary-size ints, single-precision floats, floor division and Python-style modulo, banker's rounding, exceptions with MicroPython wording and tracebacks.

Supported: functions (defaults, `*args`, `**kwargs`, keyword arguments), closures, `global`/`nonlocal`, simple classes, list/dict comprehensions, f-strings, `%` and `.format()`, `try/except/else/finally`, slicing, tuples, dicts, sets.
Modules: `machine` (Pin with irq, ADC, PWM, I2C/SoftI2C with `scan()`, Timer, `time_pulse_us`), `time`/`utime`, `math`, `random`, `dht`, `neopixel`, `ssd1306`, `sys`, `gc`.
Not supported: generators, `with`, inheritance, decorators, files, UART, SPI, networking.

Port details are modelled where they matter: the ESP32 ADC defaults to no attenuation (about 0.1–0.95 V; use `atten=ADC.ATTN_11DB`), the Pico ADC reads GP26–28 and the internal temperature sensor (channel 4), `Pin.toggle()` exists on RP2 and ESP32 ports, `Pin.irq()` is polled every 2 ms.

## What is not executable

Wi-Fi, Bluetooth, USB devices (HID/MIDI), PIO, CAN, Ethernet, deep sleep, watchdogs and bootloaders. Boards and info sheets list these as "not simulated" rather than pretending.

## Known uncertainties

Values that vary between clones and module makers are marked with ≈ or "varies" in the info sheets. A few specific figures (for example total I/O current on the UNO R4 WiFi) come from third-party pinout guides rather than the manufacturer, and say so.
