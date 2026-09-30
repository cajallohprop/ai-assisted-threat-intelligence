import pandas as pd

from src.cti.analyze_ioc import analyze_ioc


INPUT_PATH = "data/sample/sample_iocs.csv"
OUTPUT_PATH = "data/sample/ioc_analysis_results.csv"


def analyze_ioc_batch(
    input_path: str = INPUT_PATH,
    output_path: str = OUTPUT_PATH,
) -> pd.DataFrame:
    """Analyze all IOCs in a CSV file and save the results."""

    df = pd.read_csv(input_path)

    results = []

    for indicator in df["indicator"]:
        results.append(analyze_ioc(indicator))

    results_df = pd.DataFrame(results)

    results_df.to_csv(output_path, index=False)

    return results_df


if __name__ == "__main__":
    results = analyze_ioc_batch()

    print("=== Batch IOC Analysis ===")
    print()
    print(results.to_string(index=False))
    print()
    print(f"Results saved to: {OUTPUT_PATH}")