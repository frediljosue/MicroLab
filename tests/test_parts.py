"""Simulated parts run real Arduino library examples, and the simulator catches classic wiring and code mistakes."""
import pytest
from conftest import run

T = {}
T['mpu'] = ['uno', [['mpu', 700, 450, {'pitch': 30, 'roll': -20}]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SDA','B.A4'],['#0.SCL','B.A5']],
"""#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
Adafruit_MPU6050 mpu;
void setup(void) {
  Serial.begin(115200);
  if (!mpu.begin()) { Serial.println("Failed to find MPU6050 chip"); while (1) { delay(10); } }
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}
void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);
  float pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180.0 / PI;
  float roll = atan2(a.acceleration.y, a.acceleration.z) * 180.0 / PI;
  Serial.print("pitch "); Serial.print(pitch, 1); Serial.print(" roll "); Serial.print(roll, 1); Serial.print(" T "); Serial.println(temp.temperature, 1);
  delay(100);
}""", 900, None]
T['mpu_ds_clash'] = ['uno', [['mpu', 700, 450], ['ds3231', 860, 450]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SDA','B.A4'],['#0.SCL','B.A5'],['#1.VCC','B.5V'],['#1.GND','B.GND3'],['#1.SDA','B.A4'],['#1.SCL','B.A5']],
"""#include <Adafruit_MPU6050.h>
Adafruit_MPU6050 mpu;
void setup(){ Serial.begin(9600); Serial.println(mpu.begin() ? "ok" : "fail"); } void loop(){ delay(100); }""", 500, None]
T['bme'] = ['esp32', [['bme', 700, 500, {'addr': 0x76, 'hum': 61}]], [['#0.VCC','B.3V3'] if False else ['#0.VCC','B.G23'], ['#0.GND','B.GND2'],['#0.SDA','B.G21'],['#0.SCL','B.G22']],
"""#include <Adafruit_BME280.h>
Adafruit_BME280 bme;
void setup(){ pinMode(23, OUTPUT); digitalWrite(23, HIGH); Serial.begin(115200); if (!bme.begin(0x76)) Serial.println("no BME"); }
void loop(){ Serial.print(bme.readTemperature()); Serial.print(" C "); Serial.print(bme.readHumidity()); Serial.print(" % "); Serial.print(bme.readPressure() / 100.0F); Serial.println(" hPa"); delay(200); }""", 700, None]
T['rtc'] = ['uno', [['ds3231', 700, 450]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SDA','B.A4'],['#0.SCL','B.A5']],
"""#include <RTClib.h>
RTC_DS3231 rtc;
char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};
void setup () {
  Serial.begin(57600);
  if (!rtc.begin()) { Serial.println("Couldn't find RTC"); while (1) delay(10); }
  if (rtc.lostPower()) { Serial.println("RTC lost power, let's set the time!"); rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); }
}
void loop () {
  DateTime now = rtc.now();
  Serial.print(now.year(), DEC); Serial.print('/'); Serial.print(now.month(), DEC); Serial.print('/'); Serial.print(now.day(), DEC);
  Serial.print(" ("); Serial.print(daysOfTheWeek[now.dayOfTheWeek()]); Serial.print(") "); Serial.print(now.hour(), DEC); Serial.print(':'); Serial.print(now.minute(), DEC); Serial.print(':'); Serial.println(now.second(), DEC);
  delay(300);
}""", 800, None]
T['hx711'] = ['uno', [['hx711', 700, 500, {'grams': 0}]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.DT','B.D3'],['#0.SCK','B.D2']],
"""#include "HX711.h"
const int LOADCELL_DOUT_PIN = 3;
const int LOADCELL_SCK_PIN = 2;
HX711 scale;
void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale.set_scale(420.0);
  scale.tare();
}
void loop() { Serial.print("Weight: "); Serial.print(scale.get_units(5), 1); Serial.println(" g"); delay(200); }""", 500,
"comps.find(c=>c.id===ids[0]).props.grams = 750; bump(); await wait(700);"]
T['pca'] = ['uno', [['pca', 640, 420], ['servo', 640, 600], ['psu', 1000, 600, {'volts': 5}]],
 [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SDA','B.A4'],['#0.SCL','B.A5'],['#2.P','#0.VT'],['#2.N','#0.GT'],['#2.N','B.GND3'],['#1.SIG','#0.P0'],['#1.VCC','#0.V0'],['#1.GND','#0.G0']],
"""#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
#define SERVOMIN  150
#define SERVOMAX  600
void setup() { pwm.begin(); pwm.setOscillatorFrequency(27000000); pwm.setPWMFreq(50); }
void loop() { pwm.setPWM(0, 0, map(135, 0, 180, SERVOMIN, SERVOMAX)); delay(500); }""", 1500, None]
T['pca_nofreq'] = ['uno', [['pca', 640, 420], ['servo', 640, 600]],
 [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SDA','B.A4'],['#0.SCL','B.A5'],['#1.SIG','#0.P0'],['#1.VCC','#0.V0'],['#1.GND','#0.G0']],
"""#include <Adafruit_PWMServoDriver.h>
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
void setup() { pwm.begin(); }
void loop() { pwm.setPWM(0, 0, 300); delay(300); }""", 900, None]
T['gps_uno'] = ['uno', [['gps', 700, 480, {'city': 'london', 'kmh': 36}]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.TX','B.D4'],['#0.RX','B.D3']],
"""#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
static const int RXPin = 4, TXPin = 3;
static const uint32_t GPSBaud = 9600;
TinyGPSPlus gps;
SoftwareSerial ss(RXPin, TXPin);
void setup() { Serial.begin(115200); ss.begin(GPSBaud); }
void loop() {
  while (ss.available() > 0)
    if (gps.encode(ss.read())) {
      if (gps.location.isValid()) { Serial.print(gps.location.lat(), 6); Serial.print(F(",")); Serial.print(gps.location.lng(), 6); Serial.print(" sats "); Serial.print(gps.satellites.value()); Serial.print(" kmh "); Serial.println(gps.speed.kmph(), 1); }
    }
}""", 3200, None]
T['gps_delay'] = ['uno', [['gps', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.TX','B.D4'],['#0.RX','B.D3']],
"""#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>
TinyGPSPlus gps; SoftwareSerial ss(4, 3);
void setup() { Serial.begin(9600); ss.begin(9600); }
void loop() { while (ss.available()) gps.encode(ss.read()); Serial.println(gps.failedChecksum()); delay(2000); }""", 4800, None]
T['gps_esp32'] = ['esp32', [['gps', 700, 480, {'city': 'tokyo'}]], [['#0.VCC','B.3V3'] if False else ['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.TX','B.G16'],['#0.RX','B.G17']],
"""#include <TinyGPSPlus.h>
TinyGPSPlus gps;
void setup() { Serial.begin(115200); Serial2.begin(9600, SERIAL_8N1, 16, 17); }
void loop() { while (Serial2.available()) gps.encode(Serial2.read()); if (gps.location.isUpdated()) { Serial.print(gps.location.lat(), 4); Serial.print(' '); Serial.println(gps.location.lng(), 4); } }""", 2600, None]
T['sd_uno'] = ['uno', [['sd', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.MISO','B.D12'],['#0.MOSI','B.D11'],['#0.SCK','B.D13'],['#0.CS','B.D10']],
"""#include <SPI.h>
#include <SD.h>
const int chipSelect = 10; int n = 0;
void setup() { Serial.begin(9600); if (!SD.begin(chipSelect)) { Serial.println("Card failed"); while (1); } Serial.println("card initialized."); }
void loop() {
  File dataFile = SD.open("datalog.txt", FILE_WRITE);
  if (dataFile) { dataFile.println(String("reading ") + n); dataFile.close(); Serial.println(n); } else { Serial.println("error opening datalog.txt"); }
  n++; delay(200);
}""", 1000, None]
T['sd_noclose'] = ['uno', [['sd', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.MISO','B.D12'],['#0.MOSI','B.D11'],['#0.SCK','B.D13'],['#0.CS','B.D10']],
"""#include <SD.h>
File f;
void setup() { SD.begin(10); f = SD.open("LOG.TXT", FILE_WRITE); }
void loop() { f.println("data"); delay(200); }""", 3200, None]
T['sd_esp32'] = ['esp32', [['sd', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.MISO','B.G19'],['#0.MOSI','B.G23'],['#0.SCK','B.G18'],['#0.CS','B.G5']],
"""#include <SD.h>
void setup() { Serial.begin(115200); SD.begin(5); File f = SD.open("log.txt", FILE_WRITE); Serial.println(f ? "opened" : "null"); }
void loop() { delay(100); }""", 500, None]
T['tft'] = ['esp32', [['tft', 680, 330]], [['#0.VCC','B.3V3'],['#0.GND','B.GND2'],['#0.CS','B.G15'],['#0.DC','B.G2'],['#0.RESET','B.G4'],['#0.MOSI','B.G23'],['#0.SCK','B.G18'],['#0.LED','B.3V3'],['#0.MISO','B.G19']],
"""#include "SPI.h"
#include "Adafruit_GFX.h"
#include "Adafruit_ILI9341.h"
#define TFT_DC 2
#define TFT_CS 15
#define TFT_RST 4
Adafruit_ILI9341 tft = Adafruit_ILI9341(TFT_CS, TFT_DC, TFT_RST);
int n = 0;
void setup() { tft.begin(); tft.setRotation(1); tft.fillScreen(ILI9341_BLACK); }
void loop() {
  tft.fillRect(0, 0, 320, 60, ILI9341_NAVY);
  tft.setCursor(10, 10); tft.setTextColor(ILI9341_WHITE); tft.setTextSize(3); tft.println("MicroLab");
  tft.setTextSize(2); tft.setTextColor(ILI9341_YELLOW, ILI9341_BLACK); tft.setCursor(10, 80); tft.print("count: "); tft.println(n++);
  tft.fillCircle(240, 160, 40, ILI9341_RED); tft.drawLine(0, 239, 319, 120, ILI9341_GREEN); tft.fillRoundRect(20, 150, 120, 60, 10, tft.color565(0, 160, 255));
  delay(300);
}""", 900, None]
T['dht22_mismatch'] = ['uno', [['dht22', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.DATA','B.D2']],
"""#include <DHT.h>
DHT dht(2, DHT11);
void setup(){ Serial.begin(9600); dht.begin(); } void loop(){ Serial.println(dht.readTemperature()); delay(300); }""", 600, None]
T['mg995'] = ['uno', [['mg995', 700, 480]], [['#0.VCC','B.5V'],['#0.GND','B.GND2'],['#0.SIG','B.D9']],
"""#include <Servo.h>
Servo s; void setup(){ s.attach(9); s.write(150); } void loop(){ delay(100); }""", 900, None]

CHECKS = {
    "mpu": lambda r: (lambda w: abs(float(w[1]) - 30) < 0.5 and abs(float(w[3]) + 20) < 0.5)(r["lines"][-1].split()),
    "mpu_ds_clash": lambda r: any("Address clash at 0x68" in m for m in r["critical"]),
    "bme": lambda r: r["lines"][-1].startswith(("22.9", "23.0")) and "hPa" in r["lines"][-1],
    "rtc": lambda r: "lost power" in r["out"] and "(" in r["lines"][-1],
    "hx711": lambda r: r["lines"][-1] == "Weight: 750.0 g",
    "pca": lambda r: r["parts"][1]["angle"] > 150,
    "pca_nofreq": lambda r: any("V+" in m for m in r["warning"]),
    "gps_uno": lambda r: r["lines"][-1].startswith("51.507") and "kmh 36.0" in r["lines"][-1],
    "gps_delay": lambda r: any("buffer overflowed" in m for m in r["warning"]),
    "gps_esp32": lambda r: r["lines"][-1] == "35.6762 139.6503",
    "sd_uno": lambda r: "reading 0" in r["parts"][0]["files"]["datalog.txt"],
    "sd_noclose": lambda r: True,
    "sd_esp32": lambda r: any('must start with "/"' in m for m in r["warning"]),
    "tft": lambda r: not r["critical"],
    "dht22_mismatch": lambda r: any("Your code says DHT11" in m for m in r["warning"]),
    "mg995": lambda r: any("MG995" in m for m in r["warning"]) and r["parts"][0]["angle"] > 140,
}


@pytest.mark.parametrize("name", list(T))
def test_part(lab, name):
    board, parts, wires, code, ms, act = T[name]
    act = act.replace("bump(); await wait(700);", "bump(); await wait(700);") if act else None
    r = run(lab, code, board, parts, wires, ms=ms, act=act)
    assert CHECKS[name](r), r


def test_sd_data_without_close_never_reaches_card(lab):
    board, parts, wires, code, ms, act = T["sd_noclose"]
    r = run(lab, code, board, parts, wires, ms=1500)
    assert r["parts"][0]["files"].get("LOG.TXT") == ""
