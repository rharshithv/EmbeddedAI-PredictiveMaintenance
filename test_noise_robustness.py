
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv("motor_vibration_dataset_v2.csv")
model = joblib.load("motor_fault_feature_model.joblib")

X = df[["peak_amplitude"]].copy()
y = df["condition"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.4, random_state=42, stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
)

results = []

def record_result(noise_std):
    if noise_std == 0:
        X_noisy = X_test.copy()
    else:
        rng = np.random.default_rng(123)
        X_noisy = X_test.copy()
        X_noisy["peak_amplitude"] += rng.normal(
            0, noise_std, size=len(X_noisy)
        )

    predictions = model.predict(X_noisy)

    results.append({
        "noise_std": noise_std,
        "accuracy": accuracy_score(y_test, predictions),
        "abnormal_recall": recall_score(
            y_test, predictions, pos_label="abnormal"
        )
    })

for noise_std in [0, 0.01, 0.03, 0.05, 0.10]:
    record_result(noise_std)

results_df = pd.DataFrame(results)
results_df.to_csv("noise_robustness_results.csv", index=False)

print("\nNOISE ROBUSTNESS RESULTS")
print(results_df.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
print("\nSaved results to noise_robustness_results.csv")
print("Note: This is synthetic feature perturbation, not real sensor noise.")
