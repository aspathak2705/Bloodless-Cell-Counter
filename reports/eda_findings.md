# Exploratory Data Analysis Findings

## Abstract

This document presents a structured summary of exploratory data analysis conducted in [01_eda.ipynb](/C:/Users/athar/OneDrive/Documents/projects/Bloodless%20Cell%20Counter/notebooks/01_eda.ipynb) for the Bloodless Cell Counter dataset. Analysis focused on whether optical sensor measurements and engineered signal features exhibit interpretable relationships with laboratory-measured hemoglobin (`Actual_Hgb`).

The notebook operates on a processed patient-level dataset containing `10` observations and `21` variables. EDA consisted of dataset inspection, descriptive statistics, completeness checks, pairwise correlation analysis, feature-wise regression visualization, and full correlation heatmap review. Results indicate that `MAX30102_IR` and `MAX30102_RED` show the strongest observable linear relationships with hemoglobin among plotted variables, though all observed effects remain moderate and should be interpreted cautiously given limited sample size.

## Study Context

Non-invasive hemoglobin estimation depends on extracting robust physiological signal patterns from optical measurements. Before model development, it is necessary to determine whether measured channels and derived ratios demonstrate stable directional association with the target biomarker. This EDA serves that purpose: identify promising candidate features, surface weak or unstable relationships, and define realistic expectations for downstream modeling.

## Data Summary

### Dataset Profile

| Item | Value |
|------|-------|
| Source file | `data/processed/patient_level_dataset.csv` |
| Number of records | `10` |
| Number of columns | `21` |
| Primary target | `Actual_Hgb` |
| Secondary clinical variable | `Actual_RBC` |

### Completeness and Quality

- No missing values were observed in any column used by the notebook.
- Dataset includes raw optical channels, engineered ratios, engineered differences, and laboratory ground-truth measurements.
- Sample size is extremely limited; therefore, findings should be treated as exploratory rather than confirmatory.

### Variables of Primary Interest

- `MAX30102_IR`
- `MAX30102_RED`
- `AS7341_630nm`
- `AS7341_680nm`
- `RED_IR_DIFF`
- `Actual_Hgb`

## Analytical Procedure

The notebook follows a compact but standard EDA workflow:

1. Load processed patient-level dataset.
2. Inspect shape, schema, summary statistics, and null counts.
3. Remove non-numeric identifier field (`Patient Name`) for correlation analysis.
4. Compute Pearson correlation matrix across numeric variables.
5. Rank correlations with respect to `Actual_Hgb`.
6. Generate regression plots for selected sensor features against hemoglobin.
7. Review full correlation heatmap for broader multivariate context.

This approach is suitable for early-stage signal screening but not sufficient for causal inference or clinical validation.

## Descriptive Observations

The dataset spans multiple optical sensing channels from AS7341 and MAX30102 devices along with derived ratios and differences. Measured hemoglobin values center around a mean of `13.4`, with observed range from `10.6` to `15.3`. Sensor channels exhibit substantial spread, especially `MAX30102_IR`, `MAX30102_RED`, `AS7341_630nm`, and `AS7341_680nm`, indicating usable variance for exploratory modeling.

At same time, small cohort size means even visually consistent trends may be sensitive to single-point influence. Interpretation must therefore prioritize directionality and relative usefulness of features rather than precise effect magnitude.

## Correlation Analysis

### Correlation of Selected Features with `Actual_Hgb`

| Feature | Correlation with `Actual_Hgb` | Analytical Reading |
|--------|-------------------------------:|--------------------|
| `MAX30102_IR` | `-0.501` | Strongest observable linear association in current notebook; higher IR readings correspond to lower hemoglobin in this sample. |
| `MAX30102_RED` | `-0.411` | Moderate negative association; likely useful but weaker than IR channel. |
| `RED_IR_DIFF` | `0.365` | Moderate positive association; engineered difference retains some discriminative value. |
| `AS7341_680nm` | `-0.326` | Weak-to-moderate negative association. |
| `AS7341_630nm` | `-0.319` | Weak-to-moderate negative association. |

### Additional Context

- `Actual_RBC` correlates positively with `Actual_Hgb` at `0.367`, which is directionally plausible from a physiological perspective.
- Most engineered ratio variables show weak associations with hemoglobin in this sample.
- No single feature demonstrates a sufficiently strong standalone linear relationship to justify single-variable clinical estimation.

## Figure-Based Findings

### Figure 1. `RED_IR_DIFF` vs `Actual_Hgb`

This regression plot indicates a mild positive trend. Less negative `RED_IR_DIFF` values are associated with somewhat higher hemoglobin readings; however, dispersion remains broad, suggesting limited standalone predictive reliability.

![RED_IR_DIFF vs Hgb](../figures/RED_IR_DIFF%20vs%20Hgb%20Analysis.png)

### Figure 2. `MAX30102_RED` vs `Actual_Hgb`

This plot shows a moderate inverse trend. As red-channel intensity increases, hemoglobin tends to decrease within the observed sample. Relationship is visually clearer than most AS7341 wavelength plots, though still not tight enough to imply strong univariate predictability.

![MAX30102_RED vs Hgb](../figures/MAX30102_RED%20vs%20Hgb%20Analysis.png)

### Figure 3. `MAX30102_IR` vs `Actual_Hgb`

This is most informative single-feature plot in notebook. Negative slope is visibly consistent with correlation ranking and suggests that IR response may carry strongest usable hemoglobin signal among tested variables.

![MAX30102_IR vs Hgb](../figures/MAX30102_IR%20vs%20Hgb%20Analysis.png)

### Figure 4. `AS7341_630nm` vs `Actual_Hgb`

The 630nm channel displays a weak-to-moderate negative trend, but scatter remains considerable. Signal may contribute value in multivariate models even if independent explanatory power is limited.

![630nm vs Hgb](../figures/630nm%20vs%20Hgb%20Analysis.png)

### Figure 5. `AS7341_680nm` vs `Actual_Hgb`

The 680nm channel follows a similar pattern to 630nm, with slight inverse association and substantial spread around fitted line. This suggests partial signal relevance but limited standalone robustness.

![680nm vs Hgb](../figures/680nm%20vs%20Hgb%20Analysis.png)

### Figure 6. Global Correlation Structure

Heatmap confirms that hemoglobin relationships across candidate features are mostly weak to moderate. It also shows that several optical variables and engineered features are mutually related, which supports a multivariate modeling strategy rather than reliance on any single channel.

![Correlation heatmap](../figures/Correlation%20heatmap.png)

## Interpretation

Several conclusions emerge from current EDA:

1. `MAX30102_IR` is strongest candidate feature among variables explicitly visualized in notebook.
2. `MAX30102_RED` provides secondary but meaningful signal.
3. `RED_IR_DIFF` appears more useful than many wavelength-specific engineered ratios, at least in this cohort.
4. `AS7341_630nm` and `AS7341_680nm` contain signal, but relationship strength is insufficient for confident standalone use.
5. Overall feature behavior supports combined-feature regression or ensemble modeling rather than simple threshold-based estimation.

## Limitations

### Statistical Limitations

- Sample size of `10` is too small for stable inferential conclusions.
- Correlation estimates are highly sensitive to outliers and individual patient variation.
- Linear trend inspection alone cannot capture possible nonlinear optical-physiological relationships.

### Experimental Limitations

- Notebook does not report confidence intervals, significance tests, or robustness diagnostics.
- EDA is based on processed dataset only; raw acquisition conditions and measurement repeatability are not examined here.
- No stratified analysis is present for age, sex, skin tone, acquisition setup, or other potential confounders.

## Recommendations for Next Phase

To move from exploratory analysis toward research-grade model development:

1. Expand cohort size substantially before making biological or clinical claims.
2. Evaluate multivariate regression models using combined raw and engineered features.
3. Use cross-validation and patient-level holdout evaluation to reduce overfitting risk.
4. Examine nonlinear models if linear relationships remain moderate.
5. Add uncertainty reporting, residual analysis, and feature importance review in subsequent experiments.

## Conclusion

Current exploratory analysis shows that non-invasive optical signals in this dataset do contain detectable association with hemoglobin, with `MAX30102_IR` emerging as strongest individual candidate among plotted variables. Even so, present evidence remains preliminary. Main value of this EDA lies in feature prioritization and model direction-setting, not in final performance claims. Future work should therefore emphasize larger-sample validation, multivariate modeling, and stronger statistical reporting.
