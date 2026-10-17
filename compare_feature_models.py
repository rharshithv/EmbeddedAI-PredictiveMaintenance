
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

# Load synthetic motor vibration data
df = pd.read_csv("motor_vibration_dataset_v2.csv")
y = df["condition"]

# Reserve the final test set before model selection
train_val_df, test_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Split the remaining data into training and validation sets
train_df, val_df = train_test_split(
    train_val_df,
    test_size=0.25,
    random_state=42,
    stratify=train_val_df["condition"],
)

feature_sets = {
    "Peak amplitude only": ["peak_amplitude"],
    "RMS + standard deviation": ["rms", "standard_deviation"],
    "All three features": [
        "rms",
        "standard_deviation",
        "peak_amplitude",
    ],
}

results = []

print("VALIDATION RESULTS")
print("=" * 65)

for feature_name, columns in feature_sets.items():
    for depth in [1, 2, 3, 4]:
        model = DecisionTreeClassifier(
            max_depth=depth,
            class_weight="balanced",
            random_state=42,
        )

        model.fit(train_df[columns], train_df["condition"])
        predictions = model.predict(val_df[columns])

        result = {
            "features": feature_name,
            "columns": columns,
            "depth": depth,
            "model": model,
            "accuracy": accuracy_score(
                val_df["condition"], predictions
            ),
            "abnormal_precision": precision_score(
                val_df["condition"],
                predictions,
                pos_label="abnormal",
                zero_division=0,
            ),
            "abnormal_recall": recall_score(
                val_df["condition"],
                predictions,
                pos_label="abnormal",
                zero_division=0,
            ),
            "abnormal_f1": f1_score(
                val_df["condition"],
                predictions,
                pos_label="abnormal",
                zero_division=0,
            ),
        }

        results.append(result)

        print(
            f"{feature_name:27} | depth={depth} | "
            f"accuracy={result['accuracy']:.3f} | "
            f"abnormal recall={result['abnormal_recall']:.3f} | "
            f"F1={result['abnormal_f1']:.3f} | "
            f"nodes={model.tree_.node_count}"
        )

# Select using validation abnormal-class F1.
# Break ties by fewer nodes, then higher validation accuracy.
best = max(
    results,
    key=lambda r: (
        r["abnormal_f1"],
        -r["model"].tree_.node_count,
        r["accuracy"],
    ),
)

print("\nSELECTED MODEL")
print("=" * 65)
print("Features:", best["features"])
print("Depth:", best["depth"])
print("Nodes:", best["model"].tree_.node_count)
print(f"Validation accuracy: {best['accuracy']:.3f}")
print(f"Abnormal recall: {best['abnormal_recall']:.3f}")
print(f"Abnormal F1: {best['abnormal_f1']:.3f}")

# Evaluate the selected model once on the untouched test set
test_predictions = best["model"].predict(
    test_df[best["columns"]]
)

print("\nFINAL HELD-OUT TEST RESULTS")
print("=" * 65)
print(f"Test accuracy: {accuracy_score(test_df['condition'], test_predictions):.3f}")
print(
    "Abnormal precision:",
    f"{precision_score(test_df['condition'], test_predictions, pos_label='abnormal', zero_division=0):.3f}",
)
print(
    "Abnormal recall:",
    f"{recall_score(test_df['condition'], test_predictions, pos_label='abnormal', zero_division=0):.3f}",
)
print(
    "Abnormal F1:",
    f"{f1_score(test_df['condition'], test_predictions, pos_label='abnormal', zero_division=0):.3f}",
)

print("\nNote: results are based on synthetic data, not real motor measurements.")

import joblib
import json

joblib.dump(best["model"], "motor_fault_feature_model.joblib")

with open("motor_fault_feature_list.json", "w") as f:
    json.dump(best["columns"], f, indent=2)

print("\nSaved model: motor_fault_feature_model.joblib")
print("Selected features:", best["columns"])
print("Tree depth:", best["model"].get_depth())
print("Tree nodes:", best["model"].tree_.node_count)