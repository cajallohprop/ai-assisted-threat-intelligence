# AI-Assisted Threat Intelligence

**Machine learning-assisted cyber threat intelligence analysis**

## Overview

This project explores how machine learning can support cyber threat intelligence (CTI) analysts by automatically identifying potentially malicious URLs.

The project was developed from a practical CTI perspective, where analysts must process large volumes of indicators and distinguish potentially harmful infrastructure from legitimate resources.

The current implementation focuses on URL-based phishing detection using machine-learning classification.

## Objectives

* Extract meaningful structural features from URLs.
* Build a reproducible machine-learning pipeline for phishing detection.
* Evaluate a baseline classification model on unseen data.
* Examine which URL characteristics influence model predictions.
* Explore how AI-assisted analysis could support CTI workflows.

## Dataset

The project uses the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository.

The dataset contains **235,795 URL records** with a range of URL and webpage-related features.

For this project, the original labels are mapped to:

* `0` — Benign / legitimate
* `1` — Phishing

The raw dataset is intentionally kept locally and is excluded from Git using `.gitignore`.

## Approach

The current pipeline uses a compact set of URL structural features:

* URL length
* Hostname length
* Path length
* Number of dots
* Number of hyphens
* Number of slashes in the URL path
* Number of question marks
* Number of equals signs
* Number of `@` symbols
* HTTPS usage
* IP-address-based hostname detection

The baseline model uses:

**StandardScaler → Logistic Regression**

The dataset is divided into:

* **80% training data**
* **20% testing data**

A stratified split with a fixed random seed is used to maintain reproducibility.

## Results

Evaluation was performed on a held-out test set using an 80/20 stratified split.

| Metric   | Result |
| -------- | -----: |
| Accuracy | 99.23% |
| ROC-AUC  | 0.9946 |

### Confusion Matrix

```text
                 Predicted
              Benign  Phishing

Actual Benign  26953      17
Actual Phishing 344   19845
```

### 5-Fold Cross-Validation

To assess the stability of the baseline model, stratified 5-fold cross-validation was performed on the full processed dataset.

| Metric    |   Mean | Std. Dev. |
| --------- | -----: | --------: |
| Accuracy  | 0.9926 |    0.0005 |
| Precision | 0.9992 |    0.0002 |
| Recall    | 0.9834 |    0.0010 |
| F1-score  | 0.9912 |    0.0006 |
| ROC-AUC   | 0.9950 |    0.0003 |

The relatively small standard deviations indicate consistent performance across the five validation folds on this dataset. However, cross-validation does not eliminate the possibility of dataset-specific patterns or distribution differences in real-world phishing campaigns.

### Model Comparison

The baseline Logistic Regression model was compared with a Random Forest classifier using **5-fold stratified cross-validation** on the full processed dataset.

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9926 | 0.9992 | 0.9834 | 0.9912 | 0.9950 |
| Random Forest | 0.9948 | 0.9987 | 0.9890 | 0.9939 | 0.9970 |

The Random Forest produced higher mean accuracy, recall, F1-score and ROC-AUC in this cross-validation experiment, while Logistic Regression produced slightly higher mean precision.

The results are specific to the PhiUSIIL dataset, the selected URL features and the evaluation methodology used in this project. They do not establish that either model will perform better against real-world or previously unseen phishing campaigns.

The standard deviations across the five folds were small for both models, indicating relatively consistent performance across the validation folds on this dataset.

### Feature Analysis

To improve model interpretability, the project analyzes the coefficients learned by the Logistic Regression model after training on the full processed dataset.

For standardized features, a **positive coefficient** indicates an association with the model's phishing class (`1`), while a **negative coefficient** indicates an association with the benign class (`0`). The magnitude of the coefficient reflects the feature's relative contribution to the model's decision within this feature set.

The strongest coefficient associations were:

| Feature              | Coefficient | Direction           |
| -------------------- | ----------: | ------------------- |
| `num_slashes`        |    +11.8692 | Phishing-associated |
| `uses_https`         |     −6.2004 | Benign-associated   |
| `num_hyphens`        |     +1.5105 | Phishing-associated |
| `hostname_length`    |     +1.2427 | Phishing-associated |
| `path_length`        |     +0.7111 | Phishing-associated |
| `num_question_marks` |     +0.6726 | Phishing-associated |
| `url_length`         |     +0.5017 | Phishing-associated |
| `num_at_symbols`     |     +0.2836 | Phishing-associated |

These coefficients describe associations learned from the PhiUSIIL dataset and should not be interpreted as causal relationships or universal indicators of phishing. For example, HTTPS is widely used by legitimate websites as well as malicious websites, so the negative `uses_https` coefficient reflects a dataset-specific model pattern rather than a security rule.

The project also generates a visualization of the learned coefficients:

`reports/logistic_feature_coefficients.png`

This provides a simple way for analysts to inspect which URL characteristics have the strongest influence on the baseline model.

## CTI IOC Analysis

The project also includes a lightweight IOC analysis workflow designed from a CTI analyst perspective.

The workflow accepts IP addresses, domains and URLs and performs:

1. **IOC enrichment** — retrieves the indicator type, source, confidence, timestamps and threat category from the sample CTI dataset.
2. **Risk scoring** — calculates an explainable risk score using the intelligence confidence and threat category.
3. **Analyst summary** — combines enrichment and risk information into a single analyst-readable result.
4. **Batch analysis** — processes multiple IOCs from a CSV file and produces a structured analysis table.

Example workflow:

```text
IOC
 ↓
IOC Enrichment
 ↓
Confidence + Threat Category
 ↓
Risk Scoring
 ↓
Analyst Summary
```

## Limitations

This is an initial baseline rather than a production phishing-detection system.

Current limitations include:

* The feature set is intentionally small.
* The model uses only URL structural characteristics.
* The primary test-set evaluation uses a single train/test split, supplemented by 5-fold cross-validation.
* Dataset-specific patterns may influence performance.
* High benchmark performance does not guarantee real-world generalization.
* Some feature definitions require further refinement; for example, URL path structure can capture patterns that may not generalize across datasets.
* The current evaluation does not include an external or temporally separated dataset.

## Future Work

Planned improvements include:

1. Refine URL feature engineering.
2. Evaluate additional tree-based and ensemble models.
3. Perform additional validation using temporally separated or external datasets.
4. Extend evaluation with threshold analysis and external validation.
5. Expand model explainability.
6. Integrate additional CTI data sources and enrichment methods.
7. Explore integration with CTI workflows and threat-intelligence platforms.
8. Investigate AI-assisted analyst workflows for resource-constrained CSIRT environments.

## Project Structure

```text
ai-assisted-threat-intelligence/
│
├── data/
│   ├── raw/              # Local datasets, excluded from Git
│   └── processed/        # Local processed datasets, excluded from Git
│
├── models/               # Saved machine-learning models
├── notebooks/            # Exploratory analysis
├── reports/              # Analysis and experiment reports
│
├── src/
│   └── cti/
│       ├── __init__.py
│       ├── features.py
│       ├── prepare_data.py
│       ├── model.py
│       ├── evaluate.py
│       ├── download_data.py
│       ├── prepare_real_data.py
│       ├── train_real_model.py
│       ├── cross_validate.py
│       └── compare_models.py
│
├── tests/                # Project tests
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Research Direction

This project is part of a broader exploration of **AI-assisted cyber threat intelligence**.

The long-term goal is to investigate how machine learning can help CTI analysts process large volumes of threat data, identify patterns, correlate indicators and prioritize potentially significant threats while keeping human analysts involved in the decision-making process.

The project is particularly relevant to environments where cybersecurity teams operate with limited resources and need to maximize the value of available threat intelligence.

## Dataset Reference

Prasad, A., & Chandra, S. (2023). *PhiUSIIL: A diverse security profile empowered phishing URL detection framework based on similarity index and incremental learning*. Computers & Security, 103545.
