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

A subsequent run of the active Wokwi monitoring sketch verified the classifier boundary tests (5/5 passed), normal-signal handling, three-consecutive-fault detection, and recovery. Windows 1–3 were classified as HEALTHY with measured peaks of 1.200. Windows 4–5 reached WARNING after consecutive abnormal windows, and Window 6 returned to HEALTHY with the fault counter reset. Windows 7–9 triggered FAULT DETECTED on the third consecutive abnormal window, followed by recovery to HEALTHY at Window 10. The measured processing time was approximately 69.96–70.17 ms per 500-sample window in Wokwi. These measurements are simulator results, not physical ESP32 performance measurements.

## 12. NASA IMS Bearing Dataset Investigation

The NASA IMS Bearing Dataset's second test set was explored as an additional source of real vibration recordings. A total of 984 timestamped files were processed, and RMS, standard deviation, and peak amplitude were calculated from the first sensor channel.

Two recordings, timestamped `2004.02.19.06.12.39` and `2004.02.19.06.22.39`, contained near-zero measurements. Inspection of the original recordings confirmed that these low values were present in the source data across all four inspected sensor channels.

For the first channel, RMS decreased from approximately 0.483835 at 06:02:39 to 0.002103 at 06:12:39 and 0.001533 at 06:22:39 on February 19, 2004. These records were flagged for further investigation because the cause of the abrupt change has not been established.

This was an exploratory data-quality investigation. No fault labels were assigned to individual files, and no fault-detection accuracy was calculated from this dataset. The observed changes alone do not establish the onset of a bearing fault.

Further work should examine the dataset documentation, acquisition process, additional sensor channels, and temporal features before drawing conclusions.

See `nasa_data_quality_report.md` for the detailed findings.

## 13. Final Classifier Verification

### Python/C Agreement Test

The Python deployment model and compiled C classifier were compared across the 400 samples in the synthetic dataset.

- Total dataset samples: 400
- Matching predictions: 400
- Mismatches: 0
- Python/C agreement: 100.00%
- Result: PASS

This confirms implementation consistency on the tested dataset. It does not establish accuracy on real motor data.

### Boundary Tests

Five boundary values were tested against the expected classification results.

| Peak Amplitude | Expected Result | Actual Result |
|---:|---|---|
| 1.4000 | Normal | Normal |
| 1.4420 | Normal | Normal |
| 1.442362666 | Normal | Normal |
| 1.4430 | Abnormal | Abnormal |
| 1.5000 | Abnormal | Abnormal |

- Boundary tests passed: 5/5
- Result: PASS

Ten additional peak-amplitude inputs were tested against the Python deployment model and compiled C classifier.

Test inputs: 1.30, 1.4420, 1.442362666, 1.4430, 1.50, 1.5328, 1.60, 1.75, 1.80, 2.00.

- Python predictions: 10
- C predictions: 10
- Matching predictions: 10
- Mismatches: 0
- Result: PASS

### Deployment Model Comparison

The three-feature evaluation model and one-feature deployment model were compared on the same official held-out test split.

- Official test samples: 80
- Three-feature evaluation model accuracy: 81.25%
- One-feature deployment model accuracy: 81.25%
- Matching predictions: 80/80
- Mismatches: 0
- Prediction agreement: 100%

### Split Sensitivity

The one-feature deployment model was evaluated on five stratified 80/20 train/test splits of the same synthetic dataset.

| Random seed | Test accuracy |
|---:|---:|
| 10 | 86.25% |
| 20 | 82.50% |
| 30 | 78.75% |
| 42 | 81.25% |
| 50 | 77.50% |
| **Mean** | **81.25%** |

Accuracy ranged from 77.50% to 86.25%. These are exploratory evaluations on the same synthetic dataset, not independent validation on five different datasets. Results show sensitivity to the selected test samples and do not establish performance on real motor vibration data.

## 14. Validation Experiment: Decision Tree vs Fixed Peak Threshold

Both methods were evaluated on the same 80-sample validation set from the synthetic motor vibration dataset.

| Metric | Decision Tree | Fixed threshold (1.30) |
|---|---:|---:|
| Accuracy | 78.75% | 78.75% |
| Abnormal recall | 77.50% | 90.00% |
| Missed faults | 9 | 4 |
| False alarms | 8 | 13 |

The fixed threshold detected five additional abnormal samples but produced five additional false alarms. Both methods achieved the same overall accuracy of 78.75%.

**Interpretation:** The fixed threshold prioritizes detecting abnormal cases, whereas the Decision Tree produces fewer false alarms. The preferred approach depends on the relative consequences of missed faults and false alarms.

**Limitation:** These results come from a synthetic dataset and a validation set. They do not establish performance on real motor hardware.

## 15. Exploratory Threshold Sensitivity on the Held-Out Test Set

An additional experiment compared six fixed peak-amplitude thresholds on the same 80-sample held-out synthetic test set. The purpose was to examine the trade-off between abnormal-condition detection and false alarms.

| Peak-amplitude threshold | Accuracy | Abnormal recall | Missed faults | False alarms |
|---:|---:|---:|---:|---:|
| 1.20 | 66.25% | 97.50% | 1 | 26 |
| 1.25 | 67.50% | 97.50% | 1 | 25 |
| 1.30 | 72.50% | 92.50% | 3 | 19 |
| 1.35 | 75.00% | 87.50% | 5 | 15 |
| 1.40 | 78.75% | 85.00% | 6 | 11 |
| 1.4424 | 81.25% | 80.00% | 8 | 7 |

Lower thresholds detected more abnormal samples but produced more false alarms. The threshold of 1.20 missed one abnormal sample but incorrectly flagged 26 normal samples. The threshold of 1.4424 achieved the highest accuracy in this comparison but missed eight abnormal samples.

**Limitation:** These results were obtained by comparing thresholds on the held-out test set. Therefore, this experiment is exploratory and must not be treated as an independent final evaluation of a newly selected threshold. The official model result remains unchanged. Any future threshold selection should use training and validation data, followed by evaluation on a fresh, untouched test set.

## 16. ESP32 Firmware Resource Measurements

The firmware was compiled successfully using Arduino CLI with ESP32 Arduino Core version 3.3.12.

**Build target:** `esp32:esp32:esp32` (ESP32 Dev Module)

| Metric | Result |
|---|---:|
| Program storage used | 274,444 bytes (20%) |
| Maximum program storage | 1,310,720 bytes |
| Static/global RAM used | 22,548 bytes (6%) |
| Maximum RAM reported | 327,680 bytes |
| RAM remaining according to compiler | 305,132 bytes |
| Compilation status | Successful |

**Interpretation:** The firmware fits within the selected target's reported Flash and RAM limits. These figures are compiler-reported resource measurements, not runtime free-memory measurements.

**Limitation:** The firmware generates simulated vibration samples rather than reading a physical vibration sensor. The exact Wokwi board configuration has not yet been verified, and physical hardware performance has not been measured.

**Compilation command:**

`arduino-cli compile --fqbn esp32:esp32:esp32 --build-path /tmp/esp32-build --warnings all /tmp/esp32-sketch`

## 17. Host-Side C Classifier Timing Experiment

The threshold-based C classifier was benchmarked on the development Mac using an optimized Clang build and a monotonic wall-clock timer.

| Metric | Result |
|---|---:|
| Iterations | 10,000,000 |
| Total measured wall time | 0.021511 seconds |
| Reported average per call | 2.15 ns |
| Abnormal classifications | 5,000,000 |
| Platform | macOS host |
| Compiler optimization | `-O2` |

**Interpretation:** This experiment provides an initial host-side timing result for the simple threshold classifier.

**Limitation:** The reported average is specific to the benchmark harness and host environment. It is not a definitive isolated function-latency measurement and must not be presented as ESP32 inference latency. ESP32 timing remains unmeasured.


## Conclusion

This project developed and evaluated a simulation-first predictive-maintenance classifier using synthetic motor-vibration features. The selected lightweight Decision Tree achieved 81.25% accuracy on the held-out synthetic test set. A simplified one-feature deployment model reproduced the three-feature model's predictions on all 80 test samples, and the Python and C implementations agreed on all 400 synthetic dataset samples.

A separate validation experiment showed that a fixed peak-amplitude threshold of 1.30 achieved the same accuracy as the Decision Tree while detecting more abnormal samples at the cost of additional false alarms. The Wokwi ESP32 simulation demonstrated the intended monitoring and fault-alert logic using generated signals. An exploratory analysis of 984 NASA IMS bearing recordings also identified two near-zero records requiring further investigation.

These results demonstrate the implementation and testing of a simulation-first prototype. Because the classifier was evaluated using synthetic data and no physical motor or embedded-board deployment was validated, its real-world fault-detection performance remains unestablished. Further work should focus on real sensor measurements, improved validation, and target-specific embedded testing.
