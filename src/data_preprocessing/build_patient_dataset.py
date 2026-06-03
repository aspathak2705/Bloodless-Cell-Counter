import numpy as np
import pandas as pd


SPECTRAL_COLUMNS = [
    "AS7341_415nm",
    "AS7341_445nm",
    "AS7341_480nm",
    "AS7341_515nm",
    "AS7341_555nm",
    "AS7341_590nm",
    "AS7341_630nm",
    "AS7341_680nm",
]


def load_dataset(path):
    return pd.read_csv(path)


def normalize_patient_names(df):
    df = df.copy()
    df["Patient Name"] = (
        df["Patient Name"]
        .replace("", np.nan)
        .ffill()
        .astype(str)
        .str.strip()
    )
    return df


def dataset_summary(df):
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Patients: {df['Patient Name'].nunique()}")


def calculate_ppg_features(group):
    red = group["MAX30102_RED"]
    ir = group["MAX30102_IR"]

    ac_red = red.max() - red.min()
    ac_ir = ir.max() - ir.min()
    dc_red = red.mean()
    dc_ir = ir.mean()

    red_component = ac_red / dc_red if dc_red else np.nan
    ir_component = ac_ir / dc_ir if dc_ir else np.nan

    if ir_component == 0 or pd.isna(ir_component):
        r_ratio = np.nan
    else:
        r_ratio = red_component / ir_component

    return pd.Series(
        {
            "AC_RED": ac_red,
            "AC_IR": ac_ir,
            "DC_RED": dc_red,
            "DC_IR": dc_ir,
            "R_ratio": r_ratio,
        }
    )


def calculate_spectral_features(group):
    features = {}

    for column in SPECTRAL_COLUMNS:
        features[f"{column}_mean"] = group[column].mean()
        features[f"{column}_std"] = group[column].std(ddof=0)

    return pd.Series(features)


def build_patient_dataset_v2(df):
    grouped = df.groupby("Patient Name", sort=False)

    ppg_features = grouped.apply(
        calculate_ppg_features, include_groups=False
    ).reset_index()

    spectral_features = grouped.apply(
        calculate_spectral_features, include_groups=False
    ).reset_index()

    targets = grouped.agg(
        Actual_Hgb=("Actual Hgb", "first"),
        Actual_RBC=("Original RBC Count", "first"),
    ).reset_index()

    patient_df = ppg_features.merge(
        spectral_features,
        on="Patient Name",
        how="inner",
    ).merge(
        targets,
        on="Patient Name",
        how="inner",
    )

    return patient_df


def main():
    df = load_dataset("data/raw/Final Dataset.xlsx - Sheet1.csv")
    df = normalize_patient_names(df)

    dataset_summary(df)

    patient_df = build_patient_dataset_v2(df)

    patient_df.to_csv(
        "data/processed/patient_level_dataset.csv",
        index=False,
    )

    print(patient_df.shape)
    print(patient_df.columns.tolist())


if __name__ == "__main__":
    main()
