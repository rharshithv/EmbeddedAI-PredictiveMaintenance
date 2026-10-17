
const float FAULT_THRESHOLD = 1.442362666f;
const int REQUIRED_CONSECUTIVE_FAULTS = 3;

const float simulatedReadings[] = {
  1.20f, 1.40f, 1.443f, 1.60f, 1.80f, 1.30f
};

const int numberOfReadings =
  sizeof(simulatedReadings) / sizeof(simulatedReadings[0]);

int readingIndex = 0;
int consecutiveFaults = 0;
bool alertActive = false;

bool classifyMotor(float peakAmplitude) {
  return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("AI Predictive Maintenance");
  Serial.println("Consecutive Fault Detection");
  Serial.println("--------------------------------");
}

void loop() {
  float peak = simulatedReadings[readingIndex];
  bool abnormal = classifyMotor(peak);

  Serial.print("Peak amplitude: ");
  Serial.print(peak, 3);

  if (abnormal) {
    consecutiveFaults++;
    Serial.print(" | ABNORMAL");
  } else {
    consecutiveFaults = 0;
    Serial.print(" | NORMAL");
  }

  Serial.print(" | Consecutive faults: ");
  Serial.println(consecutiveFaults);

  if (consecutiveFaults >= REQUIRED_CONSECUTIVE_FAULTS &&
      !alertActive) {
    Serial.println(
      "!!! ALERT: Persistent abnormal readings detected !!!"
    );
    alertActive = true;
  }

  if (!abnormal) {
    alertActive = false;
  }

  Serial.println("--------------------------------");

  readingIndex = (readingIndex + 1) % numberOfReadings;
  delay(2000);
}
