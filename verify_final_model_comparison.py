
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the official synthetic dataset and both saved models
df = pd.read_csv("motor_vibration_dataset_v2.csv")

X = df[["rms", "standard_deviation", "peak_amplitude"]]
y = df["condition"]

# Reproduce the official 240/80/80 stratified split
X_remaining, X_test, y_remaining, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

X_train, X_val, y_train, y_val = train_test_split(
    X_remaining,
    y_remaining,
    test_size=0.25,
    random_state=42,
    stratify=y_remaining,
)

# Load the saved models
three_feature_model = joblib.load("motor_fault_tree_final.joblib")
one_feature_model = joblib.load("motor_fault_feature_model.joblib")

# Generate predictions on the same 80 held-out test samples
predictions_three = three_feature_model.predict(X_test)
predictions_one = one_feature_model.predict(
    X_test[["peak_amplitude"]]
)

matches = (predictions_three == predictions_one).sum()
total = len(y_test)

print("OFFICIAL HELD-OUT TEST COMPARISON")
print(f"Test samples: {total}")
print(f"Three-feature model accuracy: {accuracy_score(y_test, predictions_three):.2%}")
print(f"One-feature model accuracy: {accuracy_score(y_test, predictions_one):.2%}")
print(f"Matching predictions: {matches}/{total}")
print(f"Mismatches: {total - matches}")
print(f"Prediction agreement: {matches / total:.2%}")
