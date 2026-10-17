
import subprocess
import joblib
import pandas as pd

# Load the dataset and trained decision tree
df = pd.read_csv("motor_vibration_dataset_v2.csv")
model = joblib.load("motor_fault_feature_model.joblib")

features = df[["peak_amplitude"]]
python_predictions = [str(value) for value in model.predict(features)]

# Compile the C classifier
subprocess.run(
    ["clang", "-O2", "motor_classifier.c", "-o", "motor_classifier_final"],
    check=True,
)

# Send the same peak amplitudes to the C program
input_data = "\n".join(
    str(value) for value in df["peak_amplitude"]
) + "\n"

result = subprocess.run(
    ["./motor_classifier_final"],
    input=input_data,
    capture_output=True,
    text=True,
    check=True,
)

c_predictions = result.stdout.strip().splitlines()

# Compare all predictions
matches = sum(
    py == c for py, c in zip(python_predictions, c_predictions)
)

print("Total dataset samples:", len(df))
print("Matching predictions:", matches)
print("Mismatches:", len(df) - matches)
print(f"Python/C agreement: {matches / len(df) * 100:.2f}%")

if python_predictions == c_predictions:
    print("PYTHON/C VERIFICATION: PASS")
else:
    print("PYTHON/C VERIFICATION: FAIL")
