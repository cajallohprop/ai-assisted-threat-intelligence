from pathlib import Path

from ucimlrepo import fetch_ucirepo


OUTPUT_PATH = Path("data/raw/phiusiil.csv")


def download_dataset() -> None:
    """Download the PhiUSIIL phishing URL dataset from UCI."""

    dataset = fetch_ucirepo(id=967)

    df = dataset.data.features.copy()
    df["label"] = dataset.data.targets["label"]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved dataset to: {OUTPUT_PATH}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns):,}")


if __name__ == "__main__":
    download_dataset()