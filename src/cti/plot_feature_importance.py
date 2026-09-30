from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"
OUTPUT_PATH = Path("reports/logistic_feature_coefficients.png")


def plot_feature_importance():
    """Create a bar chart of Logistic Regression feature coefficients."""

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["label"])
    y = df["label"]

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

    model.fit(X, y)

    classifier = model.named_steps["classifier"]

    feature_analysis = pd.DataFrame({
        "feature": X.columns,
        "coefficient": classifier.coef_[0],
    })

    feature_analysis = feature_analysis.sort_values(
        "coefficient"
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))

    plt.barh(
        feature_analysis["feature"],
        feature_analysis["coefficient"],
    )

    plt.axvline(0, linewidth=1)

    plt.xlabel("Logistic Regression Coefficient")
    plt.ylabel("Feature")
    plt.title("URL Feature Associations in Logistic Regression")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print(f"Feature importance plot saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    plot_feature_importance()