import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"


def run_cross_validation():
    """Evaluate the logistic regression model using 5-fold stratified CV."""

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    model = Pipeline([
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "classifier",
            LogisticRegression(
                random_state=42,
                max_iter=1000,
            ),
        ),
    ])

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    scoring = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]

    results = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
    )

    print("=== 5-Fold Stratified Cross-Validation ===")

    for metric in scoring:
        scores = results[f"test_{metric}"]

        print(
            f"{metric.upper():<10} "
            f"Mean: {scores.mean():.4f} "
            f"Std: {scores.std():.4f}"
        )


if __name__ == "__main__":
    run_cross_validation()