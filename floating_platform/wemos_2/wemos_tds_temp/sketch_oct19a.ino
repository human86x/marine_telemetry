#include <OneWire.h>
#include <DallasTemperature.h>

// Pin configuration
#define ONE_WIRE_BUS D2  // Digital pin for Dallas temperature sensor
#define TDS_PIN A0       // Analog pin for TDS sensor

// Dallas Temperature setup
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Constants for TDS sensor
const float VREF = 3.3;             // Analog reference voltage
const int SAMPLES = 30;             // Number of samples for smoothing
const float TDS_FACTOR = 0.5;       // TDS calibration factor for the sensor

void setup() {
  Serial.begin(9600);
  sensors.begin();
}

void loop() {
  // Read temperature from Dallas sensor
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);

  // Read TDS sensor
  int analogValue = 0;
  for (int i = 0; i < SAMPLES; i++) {  // Take multiple readings for averaging
    analogValue += analogRead(TDS_PIN);
  }
  analogValue /= SAMPLES;

  // Convert analog value to voltage
  float voltage = analogValue * (VREF / 1024.0);
  
  // Convert voltage to TDS in ppm (parts per million)
  float tdsValue = (voltage * TDS_FACTOR) * 1000;  // Adjust based on calibration

  // Print formatted serial output
  Serial.print("A:");
  Serial.print(tempC, 2);  // Print temperature with 2 decimal points
  Serial.print(" B:");
  Serial.println(tdsValue, 2);  // Print TDS with 2 decimal points

  delay(2000);  // Wait 2 seconds before the next reading
}
