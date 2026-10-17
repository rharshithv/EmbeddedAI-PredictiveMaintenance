# AI-Based Predictive Maintenance Using TinyML

## Project Overview

This project explores a simulation-first approach to AI-based predictive maintenance using embedded systems. A machine-learning classifier analyses simulated motor vibration features to classify motor conditions as normal or abnormal.

The project combines Python-based model development, C-based classification, and ESP32 simulation using Wokwi.

## Objectives

- Generate a synthetic motor vibration dataset.
- Train and evaluate a lightweight decision-tree classifier.
- Implement a compatible classification rule in C.
- Test the classifier using boundary cases and Python/C comparisons.
- Simulate vibration monitoring and fault alerts on an ESP32 in Wokwi.

## Technologies Used

- Python
- NumPy and Pandas
- scikit-learn
- C
- VS Code
- ESP32 simulation with Wokwi

## Machine Learning Results

The final evaluation model achieved **81.25% test accuracy** on 80 held-out samples from a synthetic dataset.

- Validation accuracy: 78.75%
- Abnormal recall: 80%
- Normal recall: 82%
- Model: Decision tree with maximum depth 2

These metrics apply to the three-feature evaluation model and the synthetic dataset.

## Embedded Implementation

A separate one-feature decision-tree model uses `peak_amplitude`. Its C implementation was tested against the Python model:

- Dataset predictions compared: 400
- Matching predictions: 400
- Mismatches: 0
- Additional boundary inputs compared: 10
- Boundary mismatches: 0

## Simulation

The ESP32 simulation in Wokwi generates simulated vibration signals and demonstrates normal/abnormal classification, consecutive-fault detection, and recovery behavior.

**[Run the simulation on Wokwi](https://wokwi.com/projects/478114371222432769)**

Simulation timings are not equivalent to measurements on physical ESP32 hardware.

## Limitations

- The dataset is synthetic, not collected from a real motor.
- Real-world accuracy has not been established.
- Wokwi results do not establish physical hardware performance.
- The project is a prototype and requires further validation before practical deployment.

## Future Work

- Test with real motor vibration data.
- Evaluate false alarms and missed faults under realistic operating conditions.
- Deploy and measure the classifier on physical ESP32 hardware.
- Evaluate memory use, inference latency, and power consumption.

## Project Reports

- `benchmark_report.md` — model evaluation, implementation checks, and benchmarking.
- `wokwi_test_results.md` — ESP32 simulation test results.

## ESP32 Simulation

Explore the working ESP32 predictive maintenance simulation in Wokwi:

**[Run the simulation on Wokwi](https://wokwi.com/projects/478114371222432769)**

The simulation demonstrates vibration signal generation, normal/abnormal classification, consecutive fault detection, and recovery behavior.