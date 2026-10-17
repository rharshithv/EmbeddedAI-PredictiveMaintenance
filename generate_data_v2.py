import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(123)
samples_per_signal = 500
time = np.linspace(0, 1, samples_per_signal, endpoint=False)

def simulate_motor(condition):
    # Variation between individual simulated motor signals
    amplitude = rng.uniform(0.55, 0.95)
    frequency = rng.uniform(23, 27)
    noise_level = rng.uniform(0.12, 0.28)

    signal = amplitude * np.sin(2 * np.pi * frequency * time)
    signal += rng.normal(0, noise_level, samples_per_signal)

    if condition == "abnormal":
        # Fault-like vibration varies and sometimes is subtle
        fault_amplitude = rng.uniform(0.05, 0.65)
        fault_frequency = rng.uniform(55, 95)
        signal += fault_amplitude * np.sin(
            2 * np.pi * fault_frequency * time
        )
        signal += rng.normal(0, rng.uniform(0.05, 0.25),
                             samples_per_signal)

    return signal

rows = []
examples = {}

for condition in ["normal", "abnormal"]:
    for sample_number in range(200):
        signal = simulate_motor(condition)

        if sample_number == 0:
            examples[condition] = signal.copy()

        rows.append({
            "rms": np.sqrt(np.mean(signal ** 2)),
            "standard_deviation": np.std(signal),
            "peak_amplitude": np.max(np.abs(signal)),
            "condition": condition
        })

df = pd.DataFrame(rows)
df.to_csv("motor_vibration_dataset_v2.csv", index=False)

print("Version 2 dataset created.")
print("\nSamples per class:")
print(df["condition"].value_counts())
print("\nDataset shape:", df.shape)
print("\nFeature summary:")
print(df.groupby("condition")[
    ["rms", "standard_deviation", "peak_amplitude"]
].mean().round(3))

plt.figure(figsize=(10, 5))
plt.plot(time, examples["normal"], label="Normal example")
plt.plot(time, examples["abnormal"], label="Abnormal example",
         alpha=0.8)
plt.title("Version 2: Simulated Motor Vibration")
plt.xlabel("Time (seconds)")
plt.ylabel("Simulated vibration amplitude")
plt.legend()
plt.tight_layout()
plt.savefig("motor_vibration_plot_v2.png", dpi=150)
plt.show()
