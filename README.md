# Bloodless Cell Counter

<div align="center">
  <h1 align="center">Bloodless Cell Counter</h1>
  <p align="center">
    <strong>An exploratory optical-sensing pipeline for non-invasive hemoglobin estimation at the patient level</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Language-Python-3776AB" alt="Python" />
    <img src="https://img.shields.io/badge/Focus-Research%20Prototype-8A2BE2" alt="Research Prototype" />
    <img src="https://img.shields.io/badge/Modeling-Regression-2E8B57" alt="Regression" />
    <img src="https://img.shields.io/badge/Evaluation-LOOCV-D2691E" alt="LOOCV" />
  </p>
</div>

---

## Overview

**Bloodless Cell Counter** is an early-stage research project investigating whether optical sensor signals can support **non-invasive estimation of hemoglobin (`Actual_Hgb`)**. The repository combines:

- raw optical measurements from **AS7341** spectral channels and **MAX30102** PPG channels
- a patient-level feature engineering pipeline
- exploratory data analysis artifacts
- a baseline leave-one-out regression evaluation workflow

At its current stage, the project should be understood as a **research prototype for signal exploration and feature engineering**, not as a clinically validated diagnostic system.

## Research Objective

The central question of this repository is:

> Can aggregated optical features derived from spectral sensing and photoplethysmography provide useful signal for estimating laboratory-measured hemoglobin without invasive blood sampling?

To study that question, the project:

- aggregates repeated sensor readings into a **patient-level tabular dataset**
- derives interpretable optical features such as AC/DC components and ratio features
- inspects feature-target relationships through EDA
- evaluates a baseline regression model with **Leave-One-Out Cross-Validation (LOOCV)**

## Current Project Status

This repository is promising but still in a formative stage.

- A working preprocessing pipeline exists and produces a patient-level dataset.
- An EDA notebook and a written findings report are available.
- A baseline linear regression evaluation script is implemented.
- The `ridge`, `lasso`, and `elastic net` training scripts are currently empty placeholders.
- The repository does **not yet include a proper pinned dependency manifest** (`requirements.py` exists but is empty, and a `requirements.txt` file is not present).
- Experimental assets appear to reflect **multiple dataset iterations**: the current preprocessing script generates a 24-column processed dataset, while the EDA notebook/report reference an earlier processed schema with different engineered fields such as `RED_IR_DIFF`.

That means the README below documents the repository **as it exists now**, while also calling out where harmonization is still needed.

## Dataset Summary

### Raw Data

- Source: [`data/raw/Final Dataset.xlsx - Sheet1.csv`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\data\raw\Final Dataset.xlsx - Sheet1.csv)
- Shape: `78 rows x 13 columns`
- Raw channels:
  - `AS7341_415nm`
  - `AS7341_445nm`
  - `AS7341_480nm`
  - `AS7341_515nm`
  - `AS7341_555nm`
  - `AS7341_590nm`
  - `AS7341_630nm`
  - `AS7341_680nm`
  - `MAX30102_RED`
  - `MAX30102_IR`
- Ground-truth clinical targets:
  - `Actual Hgb`
  - `Original RBC Count`

### Processed Patient-Level Data

- Source: [`data/processed/patient_level_dataset.csv`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\data\processed\patient_level_dataset.csv)
- Shape: `10 rows x 24 columns`
- One row corresponds to one patient after aggregating repeated raw measurements.
- Current target variables:
  - `Actual_Hgb`
  - `Actual_RBC`

### Current Hemoglobin Distribution

From the processed dataset:

- Sample count: `10`
- Mean `Actual_Hgb`: `13.4`
- Standard deviation: `1.89`
- Range: `10.6` to `15.3`

Because the cohort is very small, all quantitative conclusions should be treated as **exploratory**.

## Methodology

### 1. Patient Name Normalization

The preprocessing script forward-fills missing patient names and strips formatting noise so consecutive raw rows can be grouped correctly.

Implemented in:

- [`src/data_preprocessing/build_patient_dataset.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\data_preprocessing\build_patient_dataset.py)

### 2. PPG Feature Engineering

For each patient group, the pipeline computes:

- `AC_RED = max(MAX30102_RED) - min(MAX30102_RED)`
- `AC_IR = max(MAX30102_IR) - min(MAX30102_IR)`
- `DC_RED = mean(MAX30102_RED)`
- `DC_IR = mean(MAX30102_IR)`
- `R_ratio = (AC_RED / DC_RED) / (AC_IR / DC_IR)`

These features aim to summarize pulsatile and baseline components of the PPG signal in a compact, interpretable form.

### 3. Spectral Feature Engineering

For each AS7341 wavelength channel, the pipeline computes:

- channel mean
- channel standard deviation

This produces summary statistics such as:

- `AS7341_415nm_mean`, `AS7341_415nm_std`
- `AS7341_630nm_mean`, `AS7341_630nm_std`
- `AS7341_680nm_mean`, `AS7341_680nm_std`

### 4. Feature Selection for Baseline Modeling

The current baseline feature loader selects five predictors:

- `R_ratio`
- `DC_RED`
- `DC_IR`
- `AS7341_630nm_mean`
- `AS7341_680nm_mean`

Implemented in:

- [`src/utils/data_loader.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\utils\data_loader.py)

### 5. Evaluation Strategy

The current evaluation script uses:

- **Linear Regression**
- **Leave-One-Out Cross-Validation (LOOCV)**
- **StandardScaler** fit separately inside each training fold
- comparison against a **mean baseline**

Implemented in:

- [`src/evaluation/loocv.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\evaluation\loocv.py)

## Current Experimental Findings

### Baseline LOOCV Results

Running the current evaluation workflow on the processed dataset yields:

| Model | RMSE | MAE | R2 |
|------|-----:|----:|---:|
| Linear Regression | `4.15` | `3.53` | `-4.36` |
| Mean Baseline | `1.79` | `1.56` | `0.00` |

### Interpretation

- The current linear model performs **worse than predicting the sample mean**.
- Negative `R2` under LOOCV indicates that the present baseline is not yet extracting stable predictive structure from the available sample.
- This outcome is not surprising given the combination of:
  - very small patient count
  - potential feature-dataset mismatch across project artifacts
  - limited model search
  - absence of uncertainty analysis and repeated validation cohorts

This is still a useful result: it frames the repository honestly as a **signal investigation platform**, not a finished estimator.

## Exploratory Data Analysis

EDA assets are available in:

- Notebook: [`notebooks/01_eda.ipynb`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\notebooks\01_eda.ipynb)
- Report: [`reports/eda_findings.md`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\reports\eda_findings.md)

Generated figures include:

- [`figures/MAX30102_IR vs Hgb Analysis.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\MAX30102_IR vs Hgb Analysis.png)
- [`figures/MAX30102_RED vs Hgb Analysis.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\MAX30102_RED vs Hgb Analysis.png)
- [`figures/630nm vs Hgb Analysis.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\630nm vs Hgb Analysis.png)
- [`figures/680nm vs Hgb Analysis.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\680nm vs Hgb Analysis.png)
- [`figures/RED_IR_DIFF vs Hgb Analysis.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\RED_IR_DIFF vs Hgb Analysis.png)
- [`figures/Correlation heatmap.png`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\figures\Correlation heatmap.png)

The EDA report identifies moderate exploratory relationships for variables such as `MAX30102_IR` and `MAX30102_RED`, but those findings should be read alongside an important caveat:

- the notebook/report appear to use an **older processed feature schema**
- the active preprocessing script currently emits a **different patient-level dataset**

Reconciling those two versions is an important next step for research rigor.

## Repository Structure

```text
Bloodless Cell Counter/
├── data/
│   ├── raw/
│   │   └── Final Dataset.xlsx - Sheet1.csv
│   └── processed/
│       └── patient_level_dataset.csv
├── figures/
│   └── analysis plots and correlation heatmap
├── notebooks/
│   └── 01_eda.ipynb
├── reports/
│   └── eda_findings.md
├── src/
│   ├── data_preprocessing/
│   │   └── build_patient_dataset.py
│   ├── evaluation/
│   │   └── loocv.py
│   ├── models/
│   │   ├── train_linear.py
│   │   ├── train_ridge.py
│   │   ├── train_lasso.py
│   │   └── train_elasticnet.py
│   └── utils/
│       └── data_loader.py
├── README.md
└── requirements.py
```

## Getting Started

### Prerequisites

- Python `3.10+` recommended
- `pip`

### Observed Python Dependencies

The current codebase imports:

- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `seaborn`

Because there is no usable dependency lock file yet, install them manually for now:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

## Reproducing the Current Workflow

### 1. Build the patient-level dataset

```bash
python src/data_preprocessing/build_patient_dataset.py
```

This reads the raw CSV, aggregates repeated measurements by patient, and writes:

```text
data/processed/patient_level_dataset.csv
```

### 2. Run baseline evaluation

```bash
python src/evaluation/loocv.py
```

This evaluates the current five-feature linear regression baseline under LOOCV and compares it against a mean predictor.

### 3. Review exploratory analysis

Open:

- [`notebooks/01_eda.ipynb`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\notebooks\01_eda.ipynb)

Or read the narrative summary:

- [`reports/eda_findings.md`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\reports\eda_findings.md)

## Code Notes

### Implemented

- patient-level data aggregation
- hand-crafted optical feature extraction
- selected-feature loading for baseline modeling
- LOOCV-based evaluation with scaling inside each fold
- EDA notebook, figures, and written report

### Not Yet Implemented

- actual training logic in:
  - [`src/models/train_linear.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\models\train_linear.py)
  - [`src/models/train_ridge.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\models\train_ridge.py)
  - [`src/models/train_lasso.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\models\train_lasso.py)
  - [`src/models/train_elasticnet.py`](C:\Users\athar\OneDrive\Documents\projects\Bloodless Cell Counter\src\models\train_elasticnet.py)
- pinned reproducible dependency file
- train/validation/test experiment management
- statistical confidence reporting
- clinical calibration or prospective validation

## Limitations

- **Very small cohort**: only `10` processed patient records are currently available.
- **Version drift across research assets**: notebook/report outputs do not fully match the current preprocessing schema.
- **No dependency manifest**: exact environment reproduction is not yet guaranteed.
- **Sparse model benchmark coverage**: only a baseline linear regression evaluation is implemented.
- **No clinical claims should be made** from current results.

## Recommended Next Steps

To move this repository toward a stronger research-grade baseline:

1. Consolidate the dataset version used by preprocessing, EDA, and evaluation.
2. Replace `requirements.py` with a real `requirements.txt` or `pyproject.toml`.
3. Implement ridge, lasso, and elastic net baselines with proper hyperparameter search.
4. Expand the cohort size substantially before interpreting performance trends.
5. Add residual analysis, confidence intervals, and feature importance review.
6. Document acquisition protocol, sensor conditions, and any patient-level confounders.

## Research Use Disclaimer

This repository is intended for **research and prototyping purposes only**. It is **not** a medical device, not a validated screening tool, and not suitable for clinical decision-making in its current form.

---

<div align="center">
  <p>Built as an exploratory foundation for non-invasive hemoglobin estimation research.</p>
</div>
