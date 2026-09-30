import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"


def train_model():
    """Train and evaluate a logistic regression model."""

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

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("=== Dataset Split ===")
    print(f"Training samples: {len(X_train):,}")
    print(f"Testing samples:  {len(X_test):,}")

    print("\n=== Model Evaluation ===")
    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print(f"ROC-AUC:  {roc_auc_score(y_test, probabilities):.4f}")

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Benign", "Phishing"],
            zero_division=0,
        )
    )

    classifier = model.named_steps["classifier"]

    feature_importance = pd.DataFrame({
        "feature": X.columns,
        "coefficient": classifier.coef_[0],
    })

    feature_importance["absolute_coefficient"] = (
        feature_importance["coefficient"].abs()
    )

    feature_importance = feature_importance.sort_values(
        "absolute_coefficient",
        ascending=False,
    )

    print("\n=== Feature Importance ===")
    print(
        feature_importance[
            ["feature", "coefficient"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    train_model()