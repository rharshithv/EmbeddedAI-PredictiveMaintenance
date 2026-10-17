
const float FAULT_THRESHOLD = 1.442362666f;

const float simulatedReadings[] = {
  1.20f,
  1.40f,
  1.442f,
  1.443f,
  1.60f,
  1.80f
};

const int numberOfReadings =
  sizeof(simulatedReadings) / sizeof(simulatedReadings[0]);

bool classifyMotor(float peakAmplitude) {
  return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("AI-Based Predictive Maintenance");
  Serial.println("ESP32 Simulation");
  Serial.println("------------------------------");

  for (int i = 0; i < numberOfReadings; i++) {
    float peak = simulatedReadings[i];

    Serial.print("Peak amplitude: ");
    Serial.print(peak, 3);
    Serial.print(" | Condition: ");

    if (classifyMotor(peak)) {
      Serial.println("ABNORMAL - Inspect motor");
    } else {
      Serial.println("NORMAL");
    }
  }

  Serial.println("------------------------------");
  Serial.println("Simulation complete.");
}

void loop() {
  // Run the demonstration once.
}
