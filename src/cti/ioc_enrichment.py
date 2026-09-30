import pandas as pd


DATA_PATH = "data/sample/sample_iocs.csv"


def load_ioc_data(file_path: str = DATA_PATH) -> pd.DataFrame:
    """Load the sample CTI indicator dataset."""

    return pd.read_csv(file_path)


def enrich_ioc(indicator: str, file_path: str = DATA_PATH) -> dict:
    """Search the CTI dataset and return intelligence for an IOC."""

    df = load_ioc_data(file_path)

    matches = df[
        df["indicator"].str.lower() == indicator.lower()
    ]

    if matches.empty:
        return {
            "indicator": indicator,
            "found": False,
            "message": "No matching intelligence found.",
        }

    record = matches.iloc[0]

    return {
        "indicator": record["indicator"],
        "indicator_type": record["indicator_type"],
        "source": record["source"],
        "confidence": int(record["confidence"]),
        "first_seen": record["first_seen"],
        "last_seen": record["last_seen"],
        "threat_category": record["threat_category"],
        "found": True,
    }


if __name__ == "__main__":
    test_indicator = "secure-login-example.com"

    result = enrich_ioc(test_indicator)

    print("=== IOC Enrichment ===")

    for key, value in result.items():
        print(f"{key}: {value}")