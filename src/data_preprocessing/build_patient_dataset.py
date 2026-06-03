import pandas as pd


def load_dataset(path):
    return pd.read_csv(path)


def dataset_summary(df):
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Patients: {df['Patient Name'].nunique()}")


def build_patient_dataset(df):
    grouped = df.groupby("Patient Name")

    agg_dict = {
        "AS7341_415nm": "mean",
        "AS7341_445nm": "mean",
        "AS7341_480nm": "mean",
        "AS7341_515nm": "mean",
        "AS7341_555nm": "mean",
        "AS7341_590nm": "mean",
        "AS7341_630nm": "mean",
        "AS7341_680nm": "mean",
        "MAX30102_RED": "mean",
        "MAX30102_IR": "mean",
    }

    patient_df = grouped.agg(agg_dict).reset_index()

    patient_df["Actual_Hgb"] = grouped["Actual Hgb"].first().values
    patient_df["Actual_RBC"] = grouped["Original RBC Count"].first().values

    return patient_df


def create_features(df):
    df["RED_IR_RATIO"] = df["MAX30102_RED"] / df["MAX30102_IR"]
    df["RED_IR_DIFF"] = df["MAX30102_RED"] - df["MAX30102_IR"]

    df["R630_R680_RATIO"] = (
        df["AS7341_630nm"] / df["AS7341_680nm"]
    )

    df["R630_R680_DIFF"] = (
        df["AS7341_630nm"] - df["AS7341_680nm"]
    )

    df["R590_R680_RATIO"] = (
        df["AS7341_590nm"] / df["AS7341_680nm"]
    )

    df["R555_R680_RATIO"] = (
        df["AS7341_555nm"] / df["AS7341_680nm"]
    )

    df["R630_RED_RATIO"] = (
        df["AS7341_630nm"] / df["MAX30102_RED"]
    )

    df["R680_IR_RATIO"] = (
        df["AS7341_680nm"] / df["MAX30102_IR"]
    )

    return df


def main():
    df = load_dataset(
        "data/raw/Final Dataset.xlsx - Sheet1.csv"
    )

    dataset_summary(df)

    patient_df = build_patient_dataset(df)
    patient_df = create_features(patient_df)

    print(patient_df.shape)
    print(patient_df.head())

    patient_df.to_csv(
        "data/processed/patient_level_dataset.csv",
        index=False
    )


if __name__ == "__main__":
    main()