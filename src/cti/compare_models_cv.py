import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"


def compare_models_with_cv():
    """Compare models using stratified 5-fold cross-validation."""

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    logistic_model = Pipeline([
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                random_state=42,
                max_iter=1000,
            ),
        ),
    ])

    random_forest_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )

    models = {
        "Logistic Regression": logistic_model,
        "Random Forest": random_forest_model,
    }

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

    print("=== 5-Fold Cross-Validation Model Comparison ===")

    for name, model in models.items():

        results = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
        )

        print(f"\n{name}")

        for metric in scoring:
            scores = results[f"test_{metric}"]

            print(
                f"{metric.upper():<10} "
                f"Mean: {scores.mean():.4f} "
                f"Std: {scores.std():.4f}"
            )


if __name__ == "__main__":
    compare_models_with_cv()