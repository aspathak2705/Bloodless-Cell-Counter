import pandas as pd


def load_dataset(path):
    return pd.read_csv(path)


def prepare_features(df):
    y = df["Actual_Hgb"]

    selected_features = [
        "R_ratio",
        "DC_RED",
        "DC_IR",
        "AS7341_630nm_mean",
        "AS7341_680nm_mean",
    ]

    X = df[selected_features]

    return X, y


if __name__ == "__main__":
    df = load_dataset(
        "data/processed/patient_level_dataset.csv"
    )

    X, y = prepare_features(df)

