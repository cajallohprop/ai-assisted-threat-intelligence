from urllib.parse import urlparse


def extract_url_features(url: str) -> dict:
    """Extract basic features from a URL for threat classification."""

    parsed = urlparse(url)

    return {
        "url_length": len(url),
        "hostname_length": len(parsed.hostname or ""),
        "path_length": len(parsed.path),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_slashes": url.count("/"),
        "num_question_marks": url.count("?"),
        "num_equals": url.count("="),
        "num_at_symbols": url.count("@"),
        "uses_https": int(parsed.scheme.lower() == "https"),
        "has_ip_address": int(
            parsed.hostname is not None
            and all(part.isdigit() for part in parsed.hostname.split("."))
            and len(parsed.hostname.split(".")) == 4
        ),
    }