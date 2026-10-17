# NASA IMS Bearing Dataset — Data Quality Report

## Dataset overview

- Dataset: NASA IMS Bearing Dataset, second test set
- Files processed: 984
- Sensor channel analysed: First channel
- Features calculated: RMS, standard deviation, and peak amplitude
- Sampling records: One vibration file per timestamp

## Key findings

The first sensor channel showed increased vibration variability toward the end of the recorded sequence. The maximum observed RMS was approximately 0.725, and the maximum peak amplitude was 5.0.

Two files had RMS values below 0.01:

| Timestamp | RMS | Peak amplitude |
|---|---:|---:|
| 2004.02.19.06.12.39 | 0.002103 | 0.005 |
| 2004.02.19.06.22.39 | 0.001533 | 0.005 |

Both files were checked against their original recordings. The raw data also contains very low values across all four inspected sensor channels, confirming that the low values are present in the source recordings and are not solely a CSV-export artifact.

For the first channel, RMS dropped from 0.483835 at 06:02:39 to 0.002103 at 06:12:39, then to 0.001533 at 06:22:39 on February 19, 2004. This represents an abrupt change in recorded vibration amplitude.

The two files are flagged for further investigation.

## Interpretation and limitations

The near-zero measurements may reflect a recording or sensor issue, or another change in the measurement process. The cause has not been established.

The observed vibration changes do not, by themselves, establish the exact onset of a bearing fault. No fault labels were assigned to individual files, and no real-world fault-detection accuracy is claimed from this exploratory analysis.

## Next steps

1. Inspect the dataset documentation and acquisition details.
2. Preserve the original measurements.
3. Flag the two near-zero records during exploratory analysis.
4. Evaluate additional channels and temporal features before drawing conclusions.
