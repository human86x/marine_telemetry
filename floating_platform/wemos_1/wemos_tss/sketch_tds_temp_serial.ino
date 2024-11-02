// Pin configuration
#define TSS_PIN A0  // Analog pin for TSS (Turbidity) sensor

// Constants for TSS sensor
const float VREF = 3.3;               // Analog reference voltage
const int SAMPLES = 30;               // Number of samples for smoothing
const float TURBIDITY_SCALE = -1120.4;  // Calibration values for turbidity (NTU)
const float TURBIDITY_OFFSET = 5742.3;  // Calibration offset for turbidity

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Read TSS sensor
  int analogValue = 0;
  for (int i = 0; i < SAMPLES; i++) {  // Take multiple readings for averaging
    analogValue += analogRead(TSS_PIN);
  }
  analogValue /= SAMPLES;

  // Convert analog value to voltage
  float voltage = analogValue * (VREF / 1024.0);

  // Convert voltage to turbidity (NTU)
  float turbidity = TURBIDITY_SCALE * voltage + TURBIDITY_OFFSET;

  // Print formatted serial output
  Serial.print("C:");
  Serial.print(analogValue);
  Serial.print(" D:");
  Serial.print(voltage, 2);  // Print voltage with 2 decimal points
  Serial.print(" E:");
  Serial.println(turbidity, 2);  // Print turbidity with 2 decimal points

  delay(2000);  // Wait 2 seconds before the next reading
}
