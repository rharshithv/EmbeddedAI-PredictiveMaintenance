
import joblib
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent


def test_deployment_model_loads():
    """Check that the saved deployment model loads successfully."""
    model_path = PROJECT_DIR / "motor_fault_feature_model.joblib"

    model = joblib.load(model_path)

    assert model is not None


def test_normal_and_abnormal_signals():
    """Check predictions for representative normal and abnormal peaks."""
    model_path = PROJECT_DIR / "motor_fault_feature_model.joblib"
    model = joblib.load(model_path)

    normal_peak = 1.2
    abnormal_peak = 2.0

    normal_input = pd.DataFrame({
        "peak_amplitude": [normal_peak]
    })

    abnormal_input = pd.DataFrame({
        "peak_amplitude": [abnormal_peak]
    })

    normal_prediction = model.predict(normal_input)[0]
    abnormal_prediction = model.predict(abnormal_input)[0]

    assert normal_prediction == "normal"
    assert abnormal_prediction == "abnormal"
