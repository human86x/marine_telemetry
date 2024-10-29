#define turbidityPin A0  // Analog pin connected to the sensor's AOUT pin

void setup() {
  Serial.begin(115200);  // Initialize serial communication
}

void loop() {
  // Read analog value from the sensor
  int analogValue = analogRead(turbidityPin);
  
  // Convert the analog value to voltage
  float voltage = analogValue * (5.0 / 1024.0);  // Assuming 5V system, adjust if necessary
  
  // Use a calibration formula to convert voltage to turbidity in NTU (example formula)
  float turbidity = -1120.4 * voltage * voltage + 5742.3 * voltage - 4352.9;

  // Print debug information
  Serial.print("C:");
  Serial.println(analogValue);
  Serial.print("D:");
  Serial.println(voltage, 3);
  Serial.print("E:");
  Serial.println(turbidity, 2);  // Print turbidity value with 2 decimal places
  

  delay(1000);  // Wait 1 second before reading again
}
