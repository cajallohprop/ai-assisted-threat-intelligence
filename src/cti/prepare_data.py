import pandas as pd

from src.cti.features import extract_url_features


def load_and_prepare_data(file_path: str) -> tuple[pd.DataFrame, pd.Series]:
    """Load URL data and convert URLs into machine-learning features."""

    df = pd.read_csv(file_path)

    feature_rows = [
        extract_url_features(url)
        for url in df["url"]
    ]

    X = pd.DataFrame(feature_rows)
    y = df["label"]

    return X, y


if __name__ == "__main__":
    X, y = load_and_prepare_data("data/sample_urls.csv")

    print("Features:")
    print(X)

    print("\nLabels:")
    print(y)