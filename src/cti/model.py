import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.cti.features import extract_url_features
from src.cti.prepare_data import load_and_prepare_data


def train_model(file_path: str) -> Pipeline:
    """Train a logistic regression model for URL classification."""

    X, y = load_and_prepare_data(file_path)

    model = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", LogisticRegression(random_state=42)),
    ])

    model.fit(X, y)

    return model


def predict_url(model: Pipeline, url: str) -> dict:
    """Classify a URL and return the prediction with confidence."""

    features = extract_url_features(url)

    X = pd.DataFrame([features])

    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]

    return {
        "url": url,
        "prediction": int(prediction),
        "confidence": float(max(probability)),
    }


if __name__ == "__main__":
    model = train_model("data/sample_urls.csv")

    test_urls = [
        "https://www.example.com",
        "http://192.168.1.10/login",
    ]

    for url in test_urls:
        result = predict_url(model, url)
        print(result)