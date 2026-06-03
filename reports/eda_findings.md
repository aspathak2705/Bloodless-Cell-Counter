# EDA Findings Report

## Overview

This report summarizes the exploratory data analysis performed in [01_eda.ipynb](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\notebooks\01_eda.ipynb). The notebook analyzes the processed patient-level dataset and focuses on how optical sensor readings relate to measured hemoglobin (`Actual_Hgb`).

The analysis is based on `10` patient records and `21` columns from `data/processed/patient_level_dataset.csv`. The workflow in the notebook includes:

- dataset inspection
- missing value checking
- descriptive statistics
- feature-to-hemoglobin correlation analysis
- regression plots for selected sensor features
- a full correlation heatmap

## Dataset Snapshot

### Shape

- Rows: `10`
- Columns: `21`

### Data Quality

- No missing values were found in any column used in the notebook.
- The dataset is very small, so the patterns below should be treated as early signals rather than stable conclusions.

### Key Variables Used in the Notebook

- `Actual_Hgb`
- `MAX30102_IR`
- `MAX30102_RED`
- `AS7341_630nm`
- `AS7341_680nm`
- `RED_IR_DIFF`

## Correlation Findings

The notebook computes correlations after excluding the non-numeric `Patient Name` field. When ranked by correlation with `Actual_Hgb`, the main features used for plotting behave as follows:

| Feature | Correlation with `Actual_Hgb` | Interpretation |
|--------|-------------------------------:|----------------|
| `MAX30102_IR` | `-0.501` | Strongest relationship in this notebook; higher IR values tend to align with lower hemoglobin in this small sample. |
| `MAX30102_RED` | `-0.411` | Moderate negative relationship with hemoglobin. |
| `RED_IR_DIFF` | `0.365` | Moderate positive relationship. |
| `AS7341_680nm` | `-0.326` | Weak-to-moderate negative relationship. |
| `AS7341_630nm` | `-0.319` | Weak-to-moderate negative relationship. |

Additional context from the full correlation ranking:

- `Actual_RBC` shows a moderate positive correlation with `Actual_Hgb` at `0.367`.
- Several engineered ratios show only weak relationships with hemoglobin in this dataset.
- No feature in this notebook shows a very strong standalone linear correlation with `Actual_Hgb`.

## Visual EDA

### 1. `RED_IR_DIFF` vs `Actual_Hgb`

This plot suggests a mild positive trend. Patients with less negative `RED_IR_DIFF` values tend to show somewhat higher hemoglobin, but the spread is still wide.

![RED_IR_DIFF vs Hgb](../figures/RED_IR_DIFF%20vs%20Hgb%20Analysis.png)

### 2. `MAX30102_RED` vs `Actual_Hgb`

This regression plot shows a moderate negative trend. Higher red-channel readings from the MAX30102 sensor are generally associated with lower hemoglobin values in this sample.

![MAX30102_RED vs Hgb](../figures/MAX30102_RED%20vs%20Hgb%20Analysis.png)

### 3. `MAX30102_IR` vs `Actual_Hgb`

This is the clearest trend among the plotted features. The negative slope is consistent with the correlation output, making `MAX30102_IR` the most informative single plotted feature in this notebook.

![MAX30102_IR vs Hgb](../figures/MAX30102_IR%20vs%20Hgb%20Analysis.png)

### 4. `AS7341_630nm` vs `Actual_Hgb`

The 630nm channel shows a weak-to-moderate negative pattern. The trend exists, but there is enough variability that this feature alone would not be reliable for prediction.

![630nm vs Hgb](../figures/630nm%20vs%20Hgb%20Analysis.png)

### 5. `AS7341_680nm` vs `Actual_Hgb`

The 680nm channel behaves similarly to the 630nm channel, with a slight negative trend and noticeable scatter around the regression line.

![680nm vs Hgb](../figures/680nm%20vs%20Hgb%20Analysis.png)

### 6. Full Correlation Heatmap

The heatmap provides a broader view of how raw signals, derived ratios, and target variables move together. It confirms that the strongest visible hemoglobin relationships in this notebook are still only moderate, which supports using multivariate modeling instead of relying on a single sensor reading.

![Correlation heatmap](../figures/Correlation%20heatmap.png)

## Main EDA Takeaways

1. `MAX30102_IR` appears to be the most promising single feature among those plotted for estimating hemoglobin.
2. `MAX30102_RED` also carries useful signal, though weaker than the IR channel.
3. `RED_IR_DIFF` may be more informative than simple raw wavelength channels from AS7341 in this small sample.
4. The AS7341 wavelength readings at `630nm` and `680nm` show some relationship with hemoglobin, but not enough to support strong standalone conclusions.
5. Because the dataset contains only `10` records, the current EDA is better suited for direction-finding than for final biomedical claims.

## Recommended Next Steps

- expand the patient dataset before drawing stronger conclusions
- evaluate multivariate models instead of single-feature interpretation only
- test whether engineered ratios and differences improve prediction when combined with raw channels
- validate findings with cross-validation and external samples

## Conclusion

The notebook shows that optical signals do carry some relationship with hemoglobin, especially the MAX30102 IR and red channels. However, the relationships are moderate and the sample size is very limited, so the safest conclusion is that the dataset supports further modeling work rather than definitive sensor-level claims.
