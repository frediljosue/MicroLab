# How the languages work (for developers)

Both languages turn your program into **async JavaScript** that runs inside the page and talks to the simulated hardware through one API object (`makeApi()` in `index.html`). `delay()` and `time.sleep()` become real awaits, and every loop yields regularly, so an endless `loop()` never freezes the browser.

## Arduino C++: `CPP`

`CPP.compile(source, {board, classes, apiNames, asyncNames})` returns `{js, warnings}` or throws a `CErr` with a line number.

1. **Lexer**: tokens with line numbers; comments, raw strings, char literals and number suffixes (`UL`, `f`).
2. **Preprocessor**: `#define` (object- and function-like, `#`, `##`), `#if/#ifdef/#elif/#else/#endif`, `#undef`, `#error`. Board macros (`ESP32`, `__AVR__`, `ARDUINO_ARCH_RP2040`, `__DATE__`, `__TIME__`…) come from `boardModel()`.
3. **Two passes**: pass 1 records types, structs, enums and function signatures (so functions can be called before they are defined, like the Arduino IDE allows). Pass 2 compiles declarations and bodies in source order.
4. **Typed expressions**: every expression is compiled to `{js, t}` where `t` is its C type. Binary operators apply the usual arithmetic conversions. Integer results are wrapped with `$i16`, `$u32`… and signed overflow goes through `$ov16`/`$ov32`, which warn once per line.
5. **Line alignment**: output statements stay on their source line, so runtime errors report the right line.

Runtime helpers live in `CPP.runtime()` and are passed in as `__C`: integer wrapping, checked array access, `CBuf` (char arrays), `String` methods, `sprintf`, `dtostrf`, struct cloning, reference objects for `int &x` parameters.

To support a new library, add its class to `CLASSES` and implement it inside `makeApi()`. If a method returns a float or an int, add its name to `RET_F` / `RET_I` so printing and arithmetic use the right type.

## MicroPython: `MPY`

`MPY.compile(source)` returns a JavaScript function body or throws a `PySyntax` (`SyntaxError`/`IndentationError` with a line).

1. **Tokenizer** with INDENT/DEDENT, implicit line joining inside brackets, all string prefixes and f-strings.
2. **Parser** to a small AST.
3. **Scope analysis**: Python's rule that any name assigned in a function is local unless declared `global`/`nonlocal`.
4. **Emitter**: every operation goes through the runtime `R` (`R.op`, `R.cmp`, `R.call`, `R.ga`…) so Python semantics hold: ints are `BigInt`, floats are single precision, `/` always returns a float, `//` floors.

`MPY.runtime(api, ctx)` holds the semantics, the builtins and the hardware modules. Library objects extend `LibObj` and receive `(args, kwargs)`. Each stack frame records its current line, so uncaught exceptions print a MicroPython-style traceback.

To add a MicroPython module, create it with `mod('name', {...})` inside `MPY.runtime` and register it in `MODS`. Modules that can't be simulated go in `NOT_SIM` so `import` explains why instead of failing silently.
