import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"


def compare_models():
    """Compare Logistic Regression and Random Forest on the same test set."""

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

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

    print("=== Model Comparison ===")

    for name, model in models.items():
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        probabilities = model.predict_proba(X_test)[:, 1]

        print(f"\n{name}")
        print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
        print(f"F1-score: {f1_score(y_test, predictions):.4f}")
        print(f"ROC-AUC:  {roc_auc_score(y_test, probabilities):.4f}")


if __name__ == "__main__":
    compare_models()