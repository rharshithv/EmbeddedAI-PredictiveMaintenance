# AI-Based Predictive Maintenance Using TinyML
## Final Project Report

**Project type:** Simulation-first Embedded Systems + AI prototype  
**Primary platform:** macOS, Python, C, and Wokwi ESP32 simulator

## Abstract

Predictive maintenance aims to identify abnormal equipment behavior before failures occur. This project explores a lightweight machine-learning approach for classifying simulated motor-vibration data into normal and abnormal conditions.

A synthetic dataset was generated, numerical vibration features were extracted, and Decision Tree models were evaluated. A simplified peak-amplitude classifier was implemented in C and verified against the Python model. An ESP32 monitoring workflow was also tested using the Wokwi simulator, including consecutive-fault detection and recovery behavior.

The selected model achieved 81.25% accuracy on an 80-sample held-out test set drawn from the synthetic dataset. Python/C prediction agreement was 100% on the 400 generated samples. These results demonstrate a working simulation-first prototype; performance on real motors and physical embedded hardware remains unvalidated.

## 1. Objectives

The main objectives were to:

- Explore machine learning for motor-condition monitoring.
- Generate and analyze simulated vibration data.
- Train and evaluate a lightweight classifier.
- Implement the selected classification rule in C.
- Verify agreement between Python and C predictions.
- Test fault-alert and recovery logic in an ESP32 simulation.
- Investigate robustness, false negatives, and data-quality limitations.
- Document the experiments in a reproducible technical portfolio.

## 2. System Architecture

The project follows this processing pipeline:

1. Generate synthetic motor-vibration signals.
2. Extract numerical features from each signal.
3. Train and evaluate machine-learning models.
4. Select a lightweight peak-amplitude classifier.
5. implement the classification rule in C.
6. Test monitoring and alert behavior in Wokwi.
7. Record results, limitations, and future improvements.

The principal features explored were root mean square (RMS), standard deviation, and peak amplitude.

The simplified deployment classifier uses peak amplitude as its input. The Wokwi simulation demonstrates the monitoring workflow using generated signals rather than measurements from a physical motor.

## 3. Dataset and Methodology

The main evaluation dataset contained 400 synthetic samples:

| Property | Value |
|---|---:|
| Total samples | 400 |
| Normal samples | 200 |
| Abnormal samples | 200 |
| Input features explored | 3 |
| Data source | Programmatically generated |

The three features were RMS, standard deviation, and peak amplitude. The target label was the motor condition: normal or abnormal.

A stratified train/validation/test split was used:

| Subset | Samples |
|---|---:|
| Training | 240 |
| Validation | 80 |
| Held-out test | 80 |

Model and feature selection used validation-based comparisons. The held-out test set was used to evaluate the selected model.

**Dataset limitation:** The samples are synthetic. They do not represent a validated collection of measurements from a physical motor or vibration sensor.

## 4. Model Selection and C Implementation

The selected lightweight Decision Tree configuration used peak amplitude as its feature, with a maximum depth of 2, seven nodes, and four leaves.

The simplified C implementation applies the following rule:

- If `peak_amplitude <= 1.442362666130066`, classify the sample as **normal**.
- If `peak_amplitude > 1.442362666130066`, classify the sample as **abnormal**.

This rule provides a compact implementation for the current model and dataset configuration. The threshold is not a universal motor-fault threshold and should not be applied to real equipment without suitable validation.

## 5. Model Evaluation

The selected three-feature evaluation model achieved the following results on the held-out synthetic test set:

| Metric | Result |
|---|---:|
| Test accuracy | 81.25% |
| Abnormal precision | Approximately 82.1% |
| Abnormal recall | 80.0% |
| Abnormal F1-score | Approximately 81.0% |

The confusion matrix, with rows representing actual classes and columns representing predictions, is:

| Actual class | Predicted abnormal | Predicted normal |
|---|---:|---:|
| Abnormal | 32 | 8 |
| Normal | 7 | 33 |

The classifier correctly identified 32 of the 40 abnormal test samples and missed eight. It also incorrectly flagged seven normal samples as abnormal.

These results demonstrate that the classifier can distinguish the two classes in the synthetic dataset, but its missed detections and false alarms remain important limitations.

## 6. Python/C Verification

The Python deployment model and the compiled C classifier were compared on the 400 synthetic samples.

| Verification measure | Result |
|---|---:|
| Samples compared | 400 |
| Matching predictions | 400 |
| Mismatches | 0 |
| Prediction agreement | 100% |

Additional boundary tests checked inputs close to the classification threshold. The documented boundary tests passed, and the deployment model comparison produced matching predictions on all 80 samples in the official held-out test split.

This verifies implementation consistency for the tested inputs. It does not demonstrate that the classifier is accurate on real motor data.

## 7. Noise-Robustness Experiment

A separate experiment added synthetic perturbations to the extracted peak-amplitude feature.

| Noise standard deviation | Accuracy | Abnormal recall |
|---:|---:|---:|
| 0.00 | 78.75% | 85.00% |
| 0.01 | 77.50% | 85.00% |
| 0.03 | 80.00% | 90.00% |
| 0.05 | 80.00% | 90.00% |
| 0.10 | 81.25% | 90.00% |

The results do not show a consistent decline as the perturbation level increases. Small changes can alter predictions in either direction, including correcting some baseline errors.

This experiment used a different test split from the main benchmark. The perturbations were applied to extracted features rather than raw sensor signals. Therefore, these findings should not be interpreted as proof of robustness to real sensor noise.

## 8. ESP32 Simulation in Wokwi

The monitoring workflow was tested using the Wokwi ESP32 simulator. The experiments covered:

- Different signal-window sizes.
- Normal and abnormal generated signals.
- Multiple simulated noise amplitudes.
- Classification-boundary cases.
- Alerts after three consecutive abnormal windows.
- Recovery when normal signals returned.

The documented simulation showed that the monitoring logic could progress from healthy operation to a warning, trigger a fault alert after consecutive abnormal windows, and return to a healthy state after recovery.

For 500-sample windows, the reported Wokwi processing time was approximately 69.96–70.17 ms. The measured timing is specific to the simulator and must not be presented as a physical ESP32 performance measurement.

**Simulation reference:** https://wokwi.com/projects/478114371222432769

## 9. NASA IMS Bearing Dataset Investigation

The NASA IMS Bearing Dataset was explored as an additional source of vibration recordings. A total of 984 timestamped files from the investigated test set were processed, and vibration features were calculated from the first sensor channel.

Two recordings, timestamped `2004.02.19.06.12.39` and `2004.02.19.06.22.39`, contained near-zero measurements. Inspection indicated that the low measurements were present across the inspected sensor channels.

The cause of the abrupt change was not established. This was a data-quality investigation: individual recordings were not assigned fault labels, and fault-detection accuracy was not calculated from this dataset.

Further investigation would require reviewing the dataset documentation, acquisition process, additional channels, and temporal behavior before drawing conclusions about the observed changes.

See `nasa_data_quality_report.md` for the detailed findings.

## 10. Limitations

The current prototype has several limitations:

1. The primary evaluation dataset is synthetic and may not represent real motor behavior.
2. The simplified C classifier uses only peak amplitude.
3. The held-out evaluation includes eight missed abnormal samples.
4. Python/C agreement demonstrates implementation consistency, not real-world accuracy.
5. Noise experiments use synthetic perturbations and do not establish robustness to real sensor noise.
6. Wokwi processing times are simulator measurements, not physical-device benchmarks.
7. Executable and object-file sizes measured on macOS do not establish microcontroller firmware size or RAM requirements.
8. No physical motor, vibration sensor, or embedded-board deployment has been validated.

The project should therefore be treated as a simulation-first prototype, not a production-ready predictive-maintenance or safety system.

## 11. Future Work

The following extensions would strengthen the project:

1. Acquire or identify suitable real motor-vibration measurements.
2. Review dataset labels, sensor characteristics, and data quality.
3. Improve validation and investigate missed abnormal samples.
4. Evaluate model selection on training and validation data, preserving an untouched test set.
5. Select a physical microcontroller and compatible toolchain.
6. Measure target-specific inference time, RAM usage, firmware size, and power consumption.
7. Test the complete processing pipeline using actual sensor data.
8. Document reproducible setup, execution, and evaluation procedures.

## Conclusion

This project developed a simulation-first predictive-maintenance prototype using synthetic motor-vibration features, a lightweight Decision Tree, a C classification rule, and an ESP32 monitoring simulation.

The selected model achieved 81.25% accuracy on the held-out synthetic test set. The Python and C implementations agreed on all 400 generated samples, and the Wokwi experiments demonstrated the intended consecutive-fault alert and recovery workflow.

The work establishes a documented prototype and a foundation for further embedded-AI development. Real-world detection performance, sensor-noise robustness, and physical microcontroller performance remain open questions that require additional data and hardware validation.