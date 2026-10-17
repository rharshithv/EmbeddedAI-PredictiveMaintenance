
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

# Load the dataset and final trained model
df = pd.read_csv("motor_vibration_dataset_v2.csv")
model = joblib.load("motor_fault_tree_final.joblib")

features = df[["rms", "standard_deviation", "peak_amplitude"]]
labels = df["condition"]

# Recreate the same train/validation/test split
X_remaining, X_test, y_remaining, y_test = train_test_split(
    features,
    labels,
    test_size=0.20,
    random_state=42,
    stratify=labels,
)

X_train, X_val, y_train, y_val = train_test_split(
    X_remaining,
    y_remaining,
    test_size=0.25,
    random_state=42,
    stratify=y_remaining,
)

# Predict the held-out test samples
predictions = model.predict(X_test)

# Find abnormal samples predicted as normal
false_negatives = (
    (y_test.to_numpy() == "abnormal")
    & (predictions == "normal")
)

missed = X_test.loc[false_negatives].copy()
missed["actual"] = y_test.loc[missed.index]
missed["predicted"] = predictions[false_negatives]

print("Held-out test samples:", len(X_test))
print("Confusion matrix (rows=actual, columns=predicted):")
print(confusion_matrix(y_test, predictions, labels=["abnormal", "normal"]))

print("\nFalse negatives:", len(missed))
print("\nMissed abnormal samples:")
print(missed.to_string())

# Save the findings for later analysis
missed.to_csv("false_negative_samples.csv", index=False)
print("\nSaved results to false_negative_samples.csv")
