
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

data_path = Path("data/nasa_bearings/nasa_vibration_features.csv")
df = pd.read_csv(data_path)

df["timestamp"] = pd.to_datetime(
    df["timestamp"], format="%Y.%m.%d.%H.%M.%S"
)

fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

axes[0].plot(df["timestamp"], df["rms"])
axes[0].set_title("NASA IMS Bearing Data — RMS Over Time")
axes[0].set_ylabel("RMS")
axes[0].grid(True)

axes[1].plot(df["timestamp"], df["peak_amplitude"])
axes[1].set_title("Peak Amplitude Over Time")
axes[1].set_ylabel("Peak amplitude")
axes[1].set_xlabel("Timestamp")
axes[1].grid(True)

plt.tight_layout()
plt.savefig("data/nasa_bearings/nasa_feature_trends.png", dpi=150)
plt.show()

print("Saved plot to data/nasa_bearings/nasa_feature_trends.png")
