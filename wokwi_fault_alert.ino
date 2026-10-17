
#include <math.h>

// Motor fault detection settings
const float FAULT_THRESHOLD = 1.442362666f;
const int REQUIRED_CONSECUTIVE_FAULTS = 3;

// ESP32 LED pins
const int GREEN_LED = 25;
const int YELLOW_LED = 26;
const int RED_LED = 27;

// Simulated vibration signal settings
const int SAMPLES_PER_WINDOW = 100;
const float SAMPLE_RATE_HZ = 1000.0f;
const float SIGNAL_FREQUENCY_HZ = 25.0f;
const float NOISE_FREQUENCY_HZ = 137.0f;
const float NOISE_AMPLITUDE = 0.08f;
const float TWO_PI_VALUE = 6.28318530718f;

// Monitoring variables
int readingIndex = 0;
int consecutiveFaults = 0;
const int TOTAL_WINDOWS = 6;

// Generate a simulated vibration signal with noise
// and calculate its peak absolute amplitude.
float simulateVibrationPeak(bool abnormal) {
  float peakAmplitude = 0.0f;

  for (int i = 0; i < SAMPLES_PER_WINDOW; i++) {
    float timeSeconds = (float)i / SAMPLE_RATE_HZ;

    // Base motor vibration
    float amplitude = sin(
      TWO_PI_VALUE * SIGNAL_FREQUENCY_HZ * timeSeconds
    );

    // Increase amplitude to simulate an abnormal motor
    if (abnormal) {
      amplitude *= 1.8f;
    }

    // Add a small, repeatable high-frequency component
    float noise = NOISE_AMPLITUDE * sin(
      TWO_PI_VALUE * NOISE_FREQUENCY_HZ * timeSeconds
    );

    amplitude += noise;

    // Find peak absolute amplitude
    float absoluteAmplitude = fabs(amplitude);

    if (absoluteAmplitude > peakAmplitude) {
      peakAmplitude = absoluteAmplitude;
    }
  }

  return peakAmplitude;
}

// Threshold-based motor classification
bool classifyMotor(float peakAmplitude) {
  return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
  Serial.begin(115200);

  pinMode(GREEN_LED, OUTPUT);
  pinMode(YELLOW_LED, OUTPUT);
  pinMode(RED_LED, OUTPUT);

  digitalWrite(GREEN_LED, LOW);
  digitalWrite(YELLOW_LED, LOW);
  digitalWrite(RED_LED, LOW);

  Serial.println();
  Serial.println("AI Predictive Maintenance");
  Serial.println("ESP32 Noisy Vibration Monitoring");
  Serial.println("================================");
  Serial.println("Starting signal analysis...");
}

// Continuously monitor simulated motor vibration
void loop() {
  // Windows 1-3 are normal; windows 4-6 are abnormal
  bool abnormalSignal = (readingIndex >= 3);

  // Generate vibration and calculate its peak
  float peak = simulateVibrationPeak(abnormalSignal);

  // Classify the calculated peak
  bool abnormal = classifyMotor(peak);

  // Update consecutive fault counter
  if (abnormal) {
    consecutiveFaults++;
  } else {
    consecutiveFaults = 0;
  }

  // Turn off all LEDs before selecting the new status
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

  // Display results
  Serial.print("Window: ");
  Serial.print(readingIndex + 1);

  Serial.print(" | Intended signal: ");
  Serial.print(abnormalSignal ? "ABNORMAL" : "NORMAL");

  Serial.print(" | Measured peak: ");
  Serial.print(peak, 3);

  Serial.print(" | Consecutive faults: ");
  Serial.print(consecutiveFaults);

  Serial.print(" | Motor status: ");
  Serial.println(status);

  // Trigger an alert on the third consecutive classified fault
  if (consecutiveFaults == REQUIRED_CONSECUTIVE_FAULTS) {
    Serial.println("!!! ALERT: Inspect motor immediately !!!");
  }

  Serial.println("--------------------------------");

  // Move to the next signal window
  readingIndex = (readingIndex + 1) % TOTAL_WINDOWS;

  delay(2000);
}
