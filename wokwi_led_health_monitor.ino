
const float FAULT_THRESHOLD = 1.442362666f;
const int REQUIRED_CONSECUTIVE_FAULTS = 3;

const int GREEN_LED = 25;
const int YELLOW_LED = 26;
const int RED_LED = 27;

const float simulatedReadings[] = {
  1.20f, 1.40f, 1.443f, 1.60f, 1.80f, 1.30f
};

const int numberOfReadings =
  sizeof(simulatedReadings) / sizeof(simulatedReadings[0]);

int readingIndex = 0;
int consecutiveFaults = 0;

bool classifyMotor(float peakAmplitude) {
  return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
  Serial.begin(115200);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  Serial.println("AI Predictive Maintenance");
  Serial.println("ESP32 Motor Health Monitoring");
  Serial.println("--------------------------------");
}

void loop() {
  float peak = simulatedReadings[readingIndex];
  bool abnormal = classifyMotor(peak);

  if (abnormal) {
    consecutiveFaults++;
  } else {
    consecutiveFaults = 0;
  }

  // Turn all LEDs off first.
  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);

  const char* status;

  if (consecutiveFaults >= REQUIRED_CONSECUTIVE_FAULTS) {
    status = "FAULT DETECTED";
    digitalWrite(RED_LED, HIGH);
  } else if (consecutiveFaults > 0) {
    status = "WARNING";
    digitalWrite(YELLOW_LED, HIGH);
  } else {
    status = "HEALTHY";
    digitalWrite(GREEN_LED, HIGH);
  }

  Serial.print("Peak: ");
  Serial.print(peak, 3);
  Serial.print(" | Consecutive faults: ");
  Serial.print(consecutiveFaults);
  Serial.print(" | Status: ");
  Serial.println(status);

  if (consecutiveFaults == REQUIRED_CONSECUTIVE_FAULTS) {
    Serial.println("ALERT: Inspect motor immediately!");
  }

  Serial.println("--------------------------------");

  readingIndex = (readingIndex + 1) % numberOfReadings;
  delay(2000);
}
