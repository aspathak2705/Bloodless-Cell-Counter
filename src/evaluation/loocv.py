from pathlib import Path
import sys

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import LeaveOneOut
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.data_loader import (
    load_dataset,
    prepare_features,
)

df = load_dataset("data/processed/patient_level_dataset.csv")
x, y = prepare_features(df)

print("X.shape:", x.shape)
print("X.columns.tolist():", x.columns.tolist())


def evaluate_model(model, X, y):
    loo = LeaveOneOut()

    y_true = []
    y_pred = []

    for i, (train_idx, test_idx) in enumerate(loo.split(X)):
        X_train = X.iloc[train_idx]
        X_test = X.iloc[test_idx]

        y_train = y.iloc[train_idx]
        y_test = y.iloc[test_idx]

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        model.fit(X_train, y_train)
        prediction = model.predict(X_test)

        y_true.append(y_test.values[0])
        y_pred.append(prediction[0])

        if i < 5:
            print(
                f"True: {y_test.values[0]:.2f}",
                f"Pred: {prediction[0]:.2f}",
            )

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2,
    }


def evaluate_mean_baseline(y):
    y_true = y.to_numpy()
    y_pred = np.full(
        shape=y_true.shape,
        fill_value=y.mean(),
        dtype=float,
    )

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2,
    }


linear_results = evaluate_model(LinearRegression(), x, y)
baseline_results = evaluate_mean_baseline(y)

print("Linear Regression:", linear_results)
print("Mean Baseline:", baseline_results)
