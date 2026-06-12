import pandas as pd


def load_dataset(path):
    return pd.read_csv(path)


def prepare_features(df):

    groups = df["Patient Name"]

    X = df.drop(
        columns=[
            "Patient Name",
            "Actual_Hgb",
            "Actual_RBC"
        ]
    )

    y = df["Actual_Hgb"]

    return X, y, groups


if __name__ == "__main__":

    df = load_dataset(
        "data/raw/Final Dataset.xlsx - Sheet1.csv"
    )

    X, y, groups = prepare_features(df)

    print("X Shape:", X.shape)
    print("y Shape:", y.shape)
    print("Patients:", groups.nunique())