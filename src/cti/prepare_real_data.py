from pathlib import Path

import pandas as pd

from src.cti.features import extract_url_features


INPUT_PATH = Path("data/raw/phiusiil.csv")
OUTPUT_PATH = Path("data/processed/phiusiil_features.csv")


def prepare_dataset() -> None:
    """Convert raw URLs into our custom ML features."""

    df = pd.read_csv(INPUT_PATH)

    feature_rows = [
        extract_url_features(url)
        for url in df["URL"]
    ]

    X = pd.DataFrame(feature_rows)

    # UCI PhiUSIIL labels:
    # 0 = phishing
    # 1 = legitimate
    y = df["label"].map({
        0: 1,  # phishing -> suspicious
        1: 0,  # legitimate -> benign
    })

    result = X.copy()
    result["label"] = y

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved processed dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(result):,}")
    print(f"Features: {len(X.columns):,}")
    print("\nLabel distribution:")
    print(result["label"].value_counts())


if __name__ == "__main__":
    prepare_dataset()