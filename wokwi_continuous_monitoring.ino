
#include <math.h>

const float FAULT_THRESHOLD = 1.442362666f;
const int WINDOW_SIZE = 100;

float simulatedBaseLevels[] = {
    0.40f, 0.50f, 0.60f, 1.20f, 1.50f, 1.80f
};

const int numberOfLevels =
    sizeof(simulatedBaseLevels) / sizeof(simulatedBaseLevels[0]);

int levelIndex = 0;

float samples[WINDOW_SIZE];

void generateSamples(float baseLevel) {
    // Simulated vibration samples, not real sensor readings.
    for (int i = 0; i < WINDOW_SIZE; i++) {
        float variation = 0.10f * sinf(2.0f * PI * i / 10.0f);
        samples[i] = baseLevel + variation;
    }
}

void extractFeatures(float &rms, float &standardDeviation,
                     float &peakAmplitude) {
    float sum = 0.0f;
    float sumSquares = 0.0f;
    peakAmplitude = 0.0f;

    for (int i = 0; i < WINDOW_SIZE; i++) {
        float value = samples[i];
        sum += value;
        sumSquares += value * value;

        float absoluteValue = fabsf(value);
        if (absoluteValue > peakAmplitude) {
            peakAmplitude = absoluteValue;
        }
    }

    float mean = sum / WINDOW_SIZE;
    float variance = 0.0f;

    for (int i = 0; i < WINDOW_SIZE; i++) {
        float difference = samples[i] - mean;
        variance += difference * difference;
    }

    variance /= WINDOW_SIZE;
    rms = sqrtf(sumSquares / WINDOW_SIZE);
    standardDeviation = sqrtf(variance);
}

bool classifyMotor(float peakAmplitude) {
    return peakAmplitude > FAULT_THRESHOLD;
}

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("AI Predictive Maintenance");
    Serial.println("Window-Based Feature Extraction");
    Serial.println("--------------------------------");
}

void loop() {
    float rms;
    float standardDeviation;
    float peakAmplitude;

    generateSamples(simulatedBaseLevels[levelIndex]);
    extractFeatures(rms, standardDeviation, peakAmplitude);

    Serial.print("Window ");
    Serial.print(levelIndex + 1);

    Serial.print(" | RMS: ");
    Serial.print(rms, 3);

    Serial.print(" | Std Dev: ");
    Serial.print(standardDeviation, 3);

    Serial.print(" | Peak: ");
    Serial.print(peakAmplitude, 3);

    Serial.print(" | Condition: ");

    if (classifyMotor(peakAmplitude)) {
        Serial.println("ABNORMAL - Inspect motor");
    } else {
        Serial.println("NORMAL");
    }

    levelIndex = (levelIndex + 1) % numberOfLevels;
    delay(2000);
}
