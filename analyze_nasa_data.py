
from pathlib import Path
import numpy as np
import pandas as pd

DATA_DIR = Path("data/nasa_bearings/extracted/2nd_test")
OUTPUT_FILE = Path("data/nasa_bearings/nasa_vibration_features.csv")

files = sorted(path for path in DATA_DIR.iterdir() if path.is_file())
results = []

for index, file_path in enumerate(files, start=1):
    try:
        data = pd.read_csv(file_path, sep=r"\s+", header=None).to_numpy(dtype=float)

        # Analyse the first vibration sensor channel.
        signal = data[:, 0]
        signal = signal[np.isfinite(signal)]

        if signal.size == 0:
            continue

        results.append({
            "timestamp": file_path.name,
            "rms": float(np.sqrt(np.mean(signal ** 2))),
            "standard_deviation": float(np.std(signal)),
            "peak_amplitude": float(np.max(np.abs(signal))),
        })

    except (ValueError, OSError) as error:
        print(f"Skipping {file_path.name}: {error}")

    if index % 100 == 0:
        print(f"Processed {index}/{len(files)} files")

features = pd.DataFrame(results)
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
features.to_csv(OUTPUT_FILE, index=False)

print("\nAnalysis complete.")
print(f"Files analysed: {len(features)}")
print(f"Saved to: {OUTPUT_FILE}")
print("\nFeature summary:")
print(features[["rms", "standard_deviation", "peak_amplitude"]].describe())
print("\nFirst five rows:")
print(features.head())
