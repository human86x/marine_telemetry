// Pin definition for Wemos D1 Mini
#define TdsSensorPin A0  // Connect the analog output pin (AOUT) of the TDS sensor to A0

// Calibration values
float VREF = 5.0;  // Reference voltage of the Wemos D1 Mini (5V)
float ADC_RESOLUTION = 1024.0;  // ADC resolution (10-bit)

float Temperature = 25;  // Temperature compensation for the TDS calculation
float AnalogValue = 0;  // Variable to store the analog value from the sensor
float Voltage = 0;  // Voltage corresponding to the analog value
float TdsValue = 0;  // Final TDS value

void setup() {
  Serial.begin(115200);  // Start the serial communication
}

void loop() {
  AnalogValue = analogRead(TdsSensorPin);  // Read the analog value from the sensor
  Voltage = AnalogValue * (VREF / ADC_RESOLUTION);  // Convert analog value to voltage
  
  // The TDS sensor equation to calculate TDS value
  // TDS = (Voltage in mV) * 500 / VREF / (1 + 0.02 * (Temperature - 25))
  TdsValue = (Voltage * 500 / VREF) / (1 + 0.02 * (Temperature - 25)); 
  
  Serial.print("TDS Value: ");
  Serial.print(TdsValue, 2);  // Print TDS value with 2 decimal places
  Serial.println(" ppm");

  delay(1000);  // Wait for 1 second before reading again
}
