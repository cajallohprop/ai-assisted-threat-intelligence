from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from src.cti.model import train_model
from src.cti.prepare_data import load_and_prepare_data


def evaluate_model(file_path: str) -> None:
    """Evaluate the model on the supplied dataset.

    Note:
        This is a pipeline sanity check on the training data,
        not a measure of real-world model generalization.
    """

    X, y = load_and_prepare_data(file_path)

    model = train_model(file_path)

    predictions = model.predict(X)

    accuracy = accuracy_score(y, predictions)
    matrix = confusion_matrix(y, predictions)

    print("=== Model Evaluation ===")
    print(f"Accuracy: {accuracy:.4f}")

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nClassification Report:")
    print(classification_report(
        y,
        predictions,
        target_names=["Benign", "Suspicious"],
        zero_division=0,
    ))


if __name__ == "__main__":
    evaluate_model("data/sample_urls.csv")