#include <OneWire.h>
#include <DallasTemperature.h>

// Pin where the sensor is connected
#define ONE_WIRE_BUS D2

// Setup a oneWire instance to communicate with the DS18B20
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to DallasTemperature
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(115200);
  sensors.begin(); // Start the sensor
}

void loop() {
  sensors.requestTemperatures(); // Request temperature readings
  float temperatureC = sensors.getTempCByIndex(0); // Get temperature in Celsius

  if (temperatureC != DEVICE_DISCONNECTED_C) {
    Serial.print("A: ");
    Serial.print(temperatureC);
    Serial.println("");
  } else {
    Serial.println("Error: Could not read temperature data.");
  }

  delay(1000); // Wait 1 second before the next reading
}
