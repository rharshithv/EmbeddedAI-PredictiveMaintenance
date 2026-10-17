
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

# Load the synthetic motor dataset
df = pd.read_csv("motor_vibration_dataset_v2.csv")

X = df[["rms", "standard_deviation", "peak_amplitude"]]
y = df["condition"]

# First, reserve 20% as the final test set
X_remaining, X_test, y_remaining, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

# Split the remaining data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X_remaining,
    y_remaining,
    test_size=0.25,
    random_state=42,
    stratify=y_remaining,
)

print("Dataset split")
print("--------------------")
print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Final test samples:", len(X_test))

# Choose tree depth using validation data only
depths = [1, 2, 3, 4, 5, 6, 8, None]
results = []

print("\nValidation results")
print("--------------------")

for depth in depths:
    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42,
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_val)

    accuracy = accuracy_score(y_val, predictions)

    results.append((depth, accuracy, model))

    print(
        f"Depth={str(depth):>4} | "
        f"Validation accuracy={accuracy:.2%} | "
        f"Nodes={model.tree_.node_count}"
    )

# Select the simplest model among those with the best validation accuracy
best_accuracy = max(result[1] for result in results)

best_depth, _, best_model = min(
    (result for result in results if result[1] == best_accuracy),
    key=lambda result: (
        result[2].tree_.node_count,
        0 if result[0] is None else result[0],
    ),
)

print("\nSelected tree depth:", best_depth)
print("Validation accuracy:", f"{best_accuracy:.2%}")

# Evaluate the selected model ONCE on the untouched test set
test_predictions = best_model.predict(X_test)

print("\nFinal test results")
print("--------------------")
print("Test accuracy:", f"{accuracy_score(y_test, test_predictions):.2%}")

print("\nClassification report")
print(classification_report(y_test, test_predictions, zero_division=0))

print("Confusion matrix")
print("Label order:", list(best_model.classes_))
print(confusion_matrix(y_test, test_predictions))

# Save the selected model
import joblib

joblib.dump(best_model, "motor_fault_tree_final.joblib")
print("\nSaved model: motor_fault_tree_final.joblib")
