# Getting started with MicroLab

This guide takes about 15 minutes. You need a browser (Chrome, Edge or Firefox) and nothing else.

## 1. Open the lab

Go to https://frediljosue.github.io/MicroLab/ or open `index.html` from this repo. Your circuit and code save automatically in the browser.

## 2. Your first circuit: an LED

1. The board menu at the top should say **Arduino Uno R3**.
2. From the **Parts bin** on the left, click **Resistor**, then **LED**. They appear on the bench.
3. Wire them. Click a pin, then click another pin:
   - Uno **D13** → resistor end 1
   - resistor end 2 → LED **A** (anode, the long leg)
   - LED **K** (cathode) → Uno **GND**
4. Click **▶ Upload & Run**. The default Blink sketch blinks the LED.
5. Click the LED to see its current in the **Inspector**.

Now break it on purpose: select the resistor, set it to 47 Ω and run again. The console explains why that's too much current for the pin.

## 3. Read the board's messages

- **Console** (bottom): warnings in plain language, ranked *critical*, *warning* or *info*.
- **Serial** tab: text your sketch prints with `Serial.println()`. Type in the box at the bottom to send text back.
- **Monitor** tab: the same numbers drawn as a live chart, plus every pin's state and every part's reading.

## 4. Load a complete project

Press **★ Projects** and load any card. Each one is a working circuit with commented code and a list of what it teaches. Change it, break it, fix it.

## 5. Learn a concept

Press **◎ Learn**. Each lesson is short, has a **Load the try-it circuit** button, and ends with a check question.

## 6. Practice

The **Practice** tab has 17 challenges. Build the circuit, write the code, run it, and the lab checks it automatically. Stuck? Each one has tips and a reference solution.

## 7. Try MicroPython

Switch the board to **Raspberry Pi Pico** (or an ESP32), then press **MicroPython** above the code editor. Pick an example from the dropdown and run it. Output and tracebacks appear in the Serial tab, just like on a real board.

## Tips

- Select a part and press **R** to rotate it 90° clockwise (**Shift+R** for counter-clockwise), or use the Rotate buttons in the Inspector.
- **Tidy wires** routes every wire neatly. **Keep tidy** re-routes as you move parts.
- Hover any pin to see its name and live voltage.
- **Boards** and **Parts** open the reference library with specs, pinouts and common mistakes.
- `Ctrl` + `Enter` uploads and runs from the editor.
