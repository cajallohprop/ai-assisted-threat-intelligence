import pandas as pd


DATA_PATH = "data/sample/sample_iocs.csv"


def calculate_risk_score(indicator: str, file_path: str = DATA_PATH) -> dict:
    """Calculate an explainable risk score for an IOC."""

    df = pd.read_csv(file_path)

    matches = df[
        df["indicator"].str.lower() == indicator.lower()
    ]

    if matches.empty:
        return {
            "indicator": indicator,
            "found": False,
            "risk_score": 0,
            "risk_level": "Unknown",
        }

    record = matches.iloc[0]

    confidence = int(record["confidence"])
    category = str(record["threat_category"]).lower()

    score = confidence

    if category in {"credential theft", "malware delivery"}:
        score += 5
    elif category == "command and control":
        score += 3

    score = min(score, 100)

    if score >= 90:
        risk_level = "High"
    elif score >= 70:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    return {
        "indicator": record["indicator"],
        "threat_category": record["threat_category"],
        "confidence": confidence,
        "risk_score": score,
        "risk_level": risk_level,
        "found": True,
    }


if __name__ == "__main__":
    test_indicator = "secure-login-example.com"

    result = calculate_risk_score(test_indicator)

    print("=== IOC Risk Assessment ===")

    for key, value in result.items():
        print(f"{key}: {value}")