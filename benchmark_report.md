# AI-Based Predictive Maintenance Using TinyML
## Simulation-First Project Benchmark Report

### 1. Project objective

This project explores a lightweight machine-learning classifier for
motor-condition monitoring. Synthetic vibration features are used to
distinguish normal and abnormal motor conditions.

The project follows a simulation-first approach on macOS. The C
implementation demonstrates how a simple classification rule can be
implemented in a compiled language.

### 2. Dataset

- Dataset: Synthetic motor vibration dataset, version 2
- Total samples: 400
- Normal samples: 200
- Abnormal samples: 200
- Extracted features: RMS, standard deviation and peak amplitude
- Data source: Generated programmatically for this project

**Important limitation:** These are synthetic data, not measurements
from a physical motor or vibration sensor.

### 3. Model selection and evaluation

A small Decision Tree classifier was selected using a validation-based
feature/model comparison experiment.

- Selected feature: peak amplitude
- Maximum tree depth: 2
- Number of tree nodes: 7
- Number of leaves: 4

The simplified C implementation uses the effective decision threshold:

`peak_amplitude <= 1.442362666130066` -> normal

`peak_amplitude > 1.442362666130066` -> abnormal

This simplified rule represents the effective decision boundary of the
selected model for the current dataset and model configuration.

### 4. Held-out model evaluation

The main final evaluation used a stratified train/validation/test split.

- Training samples: 240
- Validation samples: 80
- Test samples: 80
- Test accuracy: 81.25%
- Abnormal precision: approximately 82.1%
- Abnormal recall: 80.0%
- Abnormal F1-score: approximately 81.0%

Confusion matrix, with rows as actual classes and columns as predicted
classes in the order abnormal, normal:

| Actual class | Predicted abnormal | Predicted normal |
|---|---:|---:|
| Abnormal | 32 | 8 |
| Normal | 7 | 33 |

The model missed 8 of the 40 abnormal examples in this held-out test
set. This indicates that the classifier is not reliable enough to be
used as a real-world safety or maintenance system without further work.

### 5. Python and C verification

The Python model and simplified C classifier were compared across
the 400 samples in the synthetic dataset.

- Samples compared: 400
- Matching predictions: 400
- Mismatches: 0
- Prediction agreement: 100%

This verifies agreement for the tested dataset and threshold. It does
not establish generalisation to unseen real-world motor data.

### 6. Boundary tests and implementation measurements

- Boundary tests: 5 test values checked
- Boundary test result: PASS
- macOS ARM64 executable size: approximately 33 KB
- Minimal compiled object file size: approximately 536 bytes
- Observed elapsed time for processing 400 inputs through the executable:
  approximately 6 milliseconds

The elapsed time includes process startup and input/output overhead.
It is not a measurement of isolated model-inference latency on a
microcontroller.

The object file and executable measurements are for the macOS
Apple Silicon environment. They must not be presented as measurements
of a deployed microcontroller firmware image or its RAM usage.

### 7. Noise robustness experiment

Synthetic perturbations were added to the extracted peak-amplitude
feature. The results below are loaded from
`noise_robustness_results.csv`.

| Noise standard deviation | Accuracy | Abnormal recall |
|---:|---:|---:|
| 0.00 | 78.75% | 85.00% |
| 0.01 | 77.50% | 85.00% |
| 0.03 | 80.00% | 90.00% |
| 0.05 | 80.00% | 90.00% |
| 0.10 | 81.25% | 90.00% |

The results do not show a consistent decline in performance as
perturbation increases. Small perturbations can change predictions
in either direction, including correcting some baseline errors.

**Limitations:**
- Noise was added to the extracted feature, not to raw vibration signals.
- The experiment does not establish robustness to real sensor noise.
- This experiment used a different test split from the main benchmark.
- Its metrics should therefore be reported separately from the main
  held-out evaluation.

### 8. Limitations

1. The dataset is synthetic and may not represent real motor behaviour.
2. The classifier uses only peak amplitude in its simplified form.
3. Some abnormal samples are misclassified as normal.
4. Python/C agreement confirms implementation consistency, not model
   accuracy on real machines.
5. Runtime and binary sizes were measured on macOS, not on a
   microcontroller.
6. No physical sensor, motor, or embedded-board deployment has been
   validated yet.

### 9. Next steps

1. Review the synthetic data-generation process.
2. Strengthen model validation and evaluation.
3. Investigate false-negative cases and ways to reduce missed faults.
4. Select a microcontroller target and compatible toolchain.
5. Measure target-specific code size, RAM usage and inference time.
6. Evaluate using a suitable real motor-vibration dataset.
7. Document the methodology, results, limitations and future work.

### 10. Automated C classifier tests

- Test cases: 7
- Passed: 7
- Failed: 0
- Result: PASS

The compiled C classifier was tested against normal,
abnormal, and near-threshold peak-amplitude values.

All seven expected predictions matched the actual C output.

The C implementation uses the simplified effective decision
boundary of the trained Decision Tree model. This confirms
the tested classification logic, not performance on real
motor vibration measurements or a physical microcontroller.

### 11. ESP32 simulation experiments

The Wokwi ESP32 simulation was tested with:
- 100-sample and 500-sample windows
- Multiple simulated noise amplitudes
- Normal and abnormal vibration sequences
- Three-consecutive-fault alert logic
- Recovery when normal signals returned
- Classifier decision-boundary test cases

At a noise amplitude of 0.20, the 500-sample configuration
produced normal peaks of approximately 1.200 and abnormal
peaks of approximately 2.000.

The monitoring sequence correctly detected three consecutive
abnormal windows and reset the fault counter after a normal
window.

At a noise amplitude of 0.50, normal signals crossed the
classification threshold and caused false alarms.

Processing times were approximately 3.43–3.47 ms for 100
samples and 69.96–70.17 ms for 500 samples in Wokwi.

These are simulator measurements, not physical ESP32
benchmarks. The generated signals are synthetic and do not
validate performance on a real motor.

## 12. Final Classifier Verification

### Python/C Agreement Test

- Total dataset samples: 400
- Matching predictions: 400
- Mismatches: 0
- Python/C agreement: 100.00%
- Result: PASS

### Boundary Tests

| Peak Amplitude | Expected Result | Actual Result |
|---:|---|---|
| 1.4000 | Normal | Normal |
| 1.4420 | Normal | Normal |
| 1.442362666 | Normal | Normal |
| 1.4430 | Abnormal | Abnormal |
| 1.5000 | Abnormal | Abnormal |

- Boundary tests passed: 5/5
- Result: PASS

Conclusion:
The Python and C classifiers produced identical predictions
for all 400 tested samples. All five boundary tests also
matched their expected predictions. These results verify
implementation consistency on the tested inputs, but do not
establish accuracy on real motor data or prove deployment
performance on a physical microcontroller.

## 13. Final Model Evaluation

### Dataset Split

- Training samples: 240
- Validation samples: 80
- Final test samples: 80

### Model Selection

- Selected decision tree depth: 2
- Validation accuracy: 78.75%
- Tree nodes: 7

### Final Test Results

- Test accuracy: 81.25%
- Abnormal precision: 82%
- Abnormal recall: 80%
- Abnormal F1-score: 81%
- Normal precision: 80%
- Normal recall: 82%
- Normal F1-score: 81%

### Confusion Matrix

Label order: abnormal, normal

| Actual / Predicted | Abnormal | Normal |
|---|---:|---:|
| Abnormal | 32 | 8 |
| Normal | 7 | 33 |

### Interpretation

The model correctly classified 65 of the 80 test samples.
It detected 32 of 40 abnormal samples and missed 8.
It correctly identified 33 of 40 normal samples and
incorrectly flagged 7 as abnormal.

The final test accuracy was 81.25%. These results apply
to the held-out synthetic dataset and do not establish
performance on real motor vibration measurements.

## 14. Direct Python/C Boundary Verification

Ten peak-amplitude inputs were tested against the Python
deployment model and the compiled C classifier.

Test inputs:
1.30, 1.4420, 1.442362666, 1.4430, 1.50,
1.5328, 1.60, 1.75, 1.80, 2.00

Results:
- Python predictions: 10
- C predictions: 10
- Matching predictions: 10
- Mismatches: 0
- Result: PASS

cat >> benchmark_report.md <<'EOF'

### Deployment Model Comparison and Split Sensitivity

The three-feature evaluation model and one-feature deployment model
were compared on the same official held-out test split.

- Official test samples: 80
- Three-feature evaluation model accuracy: 81.25%
- One-feature deployment model accuracy: 81.25%
- Matching predictions: 80/80
- Mismatches: 0
- Prediction agreement: 100%

The deployment model was also evaluated on five separate stratified
80/20 train/test splits using random seeds 10, 20, 30, 42, and 50.

| Random seed | Test accuracy |
|---:|---:|
| 10 | 86.25% |
| 20 | 82.50% |
| 30 | 78.75% |
| 42 | 81.25% |
| 50 | 77.50% |
| **Mean** | **81.25%** |

Accuracy ranged from 77.50% to 86.25% across these splits. These
results show sensitivity to the selected test samples. All evaluations
use the same synthetic dataset and do not establish performance on
real motor vibration data.

The five-split results are additional exploratory evaluations, not
independent validation on five different datasets.
Conclusion:
The Python deployment model and C classifier agreed on
all ten selected boundary and representative inputs.
Together with the 400-sample dataset comparison, this
supports implementation consistency for the tested inputs.
It does not establish performance on real motor data.
