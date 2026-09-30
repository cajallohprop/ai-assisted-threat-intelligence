import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


DATA_PATH = "data/processed/phiusiil_features.csv"


def analyze_logistic_coefficients():
    """Analyze Logistic Regression coefficients for URL features."""

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

    feature_analysis["absolute_coefficient"] = (
        feature_analysis["coefficient"].abs()
    )

    feature_analysis["direction"] = feature_analysis[
        "coefficient"
    ].apply(
        lambda value: "phishing-associated"
        if value > 0
        else "benign-associated"
    )

    feature_analysis = feature_analysis.sort_values(
        "absolute_coefficient",
        ascending=False,
    )

    print("=== Logistic Regression Feature Analysis ===")
    print()

    print(
        feature_analysis[
            ["feature", "coefficient", "direction"]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    analyze_logistic_coefficients()