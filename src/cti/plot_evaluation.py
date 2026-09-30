from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    PrecisionRecallDisplay,
    RocCurveDisplay,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"
OUTPUT_DIR = Path("reports")


def plot_evaluation_curves():
    """Train the baseline model and generate ROC and PR curves."""

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
        ("scaler", StandardScaler()),
        (
            "classifier",
            LogisticRegression(
                random_state=42,
                max_iter=1000,
            ),
        ),
    ])

    model.fit(X_train, y_train)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ROC Curve
    RocCurveDisplay.from_estimator(
        model,
        X_test,
        y_test,
    )

    plt.title("ROC Curve - Logistic Regression")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "roc_curve.png",
        dpi=300,
    )
    plt.close()

    # Precision-Recall Curve
    PrecisionRecallDisplay.from_estimator(
        model,
        X_test,
        y_test,
    )

    plt.title("Precision-Recall Curve - Logistic Regression")
    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / "precision_recall_curve.png",
        dpi=300,
    )
    plt.close()

    print("Evaluation plots saved:")
    print(OUTPUT_DIR / "roc_curve.png")
    print(OUTPUT_DIR / "precision_recall_curve.png")


if __name__ == "__main__":
    plot_evaluation_curves()