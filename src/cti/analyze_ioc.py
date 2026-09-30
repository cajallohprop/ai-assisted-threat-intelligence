from src.cti.ioc_enrichment import enrich_ioc
from src.cti.risk_scoring import calculate_risk_score


def analyze_ioc(indicator: str) -> dict:
    """Combine IOC enrichment and risk scoring into one analyst view."""

    enrichment = enrich_ioc(indicator)
    risk = calculate_risk_score(indicator)

    if not enrichment["found"]:
        return {
            "indicator": indicator,
            "status": "No intelligence found",
            "risk_level": risk["risk_level"],
            "risk_score": risk["risk_score"],
        }

    return {
        "indicator": enrichment["indicator"],
        "indicator_type": enrichment["indicator_type"],
        "threat_category": enrichment["threat_category"],
        "source": enrichment["source"],
        "confidence": enrichment["confidence"],
        "first_seen": enrichment["first_seen"],
        "last_seen": enrichment["last_seen"],
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "status": "Intelligence found",
    }


if __name__ == "__main__":
    test_indicator = "secure-login-example.com"

    result = analyze_ioc(test_indicator)

    print("=== CTI Analyst IOC Summary ===")

    for key, value in result.items():
        print(f"{key}: {value}")