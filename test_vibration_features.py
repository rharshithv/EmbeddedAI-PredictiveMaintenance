
import numpy as np
import pandas as pd
import joblib

# Match the current Wokwi configuration
SAMPLE_RATE_HZ = 1000.0
SAMPLES_PER_WINDOW = 500
SIGNAL_FREQUENCY_HZ = 25.0
NOISE_FREQUENCY_HZ = 137.0
NOISE_AMPLITUDE = 0.20
FAULT_THRESHOLD = 1.442362666

# Load the trained peak-amplitude classifier
model = joblib.load("motor_fault_feature_model.joblib")

time = np.arange(SAMPLES_PER_WINDOW) / SAMPLE_RATE_HZ

def generate_signal(abnormal):
    amplitude = np.sin(
        2 * np.pi * SIGNAL_FREQUENCY_HZ * time
    )

    if abnormal:
        amplitude *= 1.8

    noise = NOISE_AMPLITUDE * np.sin(
        2 * np.pi * NOISE_FREQUENCY_HZ * time
    )

    return amplitude + noise

def extract_features(signal):
    return {
        "peak_amplitude": float(np.max(np.abs(signal))),
        "rms": float(np.sqrt(np.mean(signal ** 2))),
        "standard_deviation": float(np.std(signal)),
    }

for name, abnormal in [
    ("Normal", False),
    ("Abnormal", True),
]:
    signal = generate_signal(abnormal)
    features = extract_features(signal)

    model_input = pd.DataFrame({
        "peak_amplitude": [features["peak_amplitude"]]
    })

    prediction = model.predict(model_input)[0]

    print(f"\n{name} signal")
    print(f"Peak amplitude: {features['peak_amplitude']:.4f}")
    print(f"RMS: {features['rms']:.4f}")
    print(f"Standard deviation: {features['standard_deviation']:.4f}")
    print(f"Model prediction: {prediction}")

    if name == "Normal":
        assert prediction == "normal", "Normal signal misclassified"
    else:
        assert prediction == "abnormal", "Abnormal signal misclassified"

print("\nPYTHON SIGNAL TEST: PASS")
