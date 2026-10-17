
# ESP32 Predictive Maintenance Simulation — Test Results

## Test environment
- Platform: Wokwi ESP32 simulator
- Signal: Simulated noisy motor vibration
- Samples per window: 100
- Fault threshold: 1.30
- Consecutive faults required: 3

## Test 1: Normal and abnormal detection
- Normal signals classified as healthy.
- First consecutive abnormal window: warning.
- Second consecutive abnormal window: warning.
- Third consecutive abnormal window: fault detected.

## Test 2: Fault recovery
- Normal signal resets the consecutive fault counter.
- A later sequence of three consecutive abnormal signals triggers the alert again.
- The following normal signal returns the status to healthy.

## Conclusion
The simulated monitoring logic passed the normal-condition,
fault-detection, and fault-recovery sequence tests.

This validates the implemented simulation logic only. It does not
establish performance on a physical motor or real sensor data.

## Test 3: ESP32 classifier integration

- Original trained-model threshold: 1.442362666
- Normal simulated peak: 1.070
- Abnormal simulated peak: 1.870
- Consecutive fault warning: PASS
- Third-consecutive-fault alert: PASS
- Fault counter reset on normal signal: PASS

The Wokwi simulation passed the normal, fault-detection,
and recovery sequence tests. Testing near the exact threshold
is still required.


## Test 4: Signal processing performance

- Platform: Wokwi ESP32 simulator
- Samples per window: 100
- Measured processing time: 3430–3468 microseconds
- Approximate processing time: 3.43–3.47 ms
- Fault detection and recovery: PASS

The measured interval covers simulated vibration generation
and peak-amplitude calculation. It does not represent isolated
classifier inference time or a physical ESP32 benchmark.


## Test 5: Sample-window comparison

| Measurement | 100 samples | 500 samples |
|---|---:|---:|
| Processing time | 3.43–3.47 ms | 69.96–70.17 ms |
| Normal peak | 1.070 | 1.080 |
| Abnormal peak | 1.870 | 1.880 |
| Fault detection | PASS | PASS |
| Recovery | PASS | PASS |

Increasing the sample window increased processing time
substantially. Both configurations retained the expected
fault-detection and recovery behavior.

These timings are Wokwi simulation measurements, not
physical ESP32 performance measurements.

## Test 6: Noise amplitude 0.20

- Sample window: 500 samples
- Normal peak: 1.200
- Abnormal peak: 2.000
- Processing time: approximately 70 ms
- Fault detection: PASS
- Recovery after normal signal: PASS

At noise amplitude 0.50, the normal signal crossed the
classification threshold and produced false alarms.
At 0.20, the expected monitoring sequence worked correctly.

These results use simulated signals and do not establish
robustness on real motor vibration data.

## Test 7: Python and Wokwi Signal Comparison

Objective: Verify that Python and Wokwi generate matching
peak amplitudes for the same simulated vibration settings.

Settings:
- Samples per window: 500
- Sample rate: 1000 Hz
- Base frequency: 25 Hz
- Added component frequency: 137 Hz
- Noise amplitude: 0.20

Results:

| Feature | Normal | Abnormal |
|---|---:|---:|
| Peak amplitude | 1.2000 | 2.0000 |
| RMS | 0.7211 | 1.2806 |
| Standard deviation |

## Test 8: ESP32 Configuration Verification

Configuration checked:
- Samples per window: 500
- Noise amplitude: 0.20
- Fault threshold: 1.442362666
- Consecutive abnormal windows required: 3

Result: PASS

Conclusion:
The Wokwi simulation configuration matches the intended
test settings. The existing classifier and fault-alert
logic are retained without modification.

Note:
This verifies the configured simulation settings. It does
not establish real-hardware performance or validate the
classifier on real motor measurements.