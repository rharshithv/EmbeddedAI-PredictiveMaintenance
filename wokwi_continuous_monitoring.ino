
const float FAULT_THRESHOLD = 1.442362666f;

const float simulatedReadings[] = {
  1.20f, 1.40f, 1.442f, 1.443f, 1.60f, 1.80f
};

const int numberOfReadings =
  sizeof(simulatedReadings) / sizeof(simulatedReadings[0]);

int readingIndex = 0;

bool classifyMotor(float peakAmplitude) {
  return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("AI Predictive Maintenance");
  Serial.println("Continuous Monitoring Started");
  Serial.println("--------------------------------");
}

void loop() {
  float peak = simulatedReadings[readingIndex];

  Serial.print("Reading ");
  Serial.print(readingIndex + 1);
  Serial.print(" | Peak amplitude: ");
  Serial.print(peak, 3);
  Serial.print(" | Condition: ");

  if (classifyMotor(peak)) {
    Serial.println("ABNORMAL - Inspect motor");
  } else {
    Serial.println("NORMAL");
  }

  readingIndex = (readingIndex + 1) % numberOfReadings;

  delay(2000);
}
