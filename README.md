\# AI-Assisted Threat Intelligence



\*\*Machine learning-assisted cyber threat intelligence analysis\*\*



\## Overview



This project explores how machine learning can support cyber threat intelligence (CTI) analysts by automatically identifying potentially malicious URLs.



The project was developed from a practical CTI perspective, where analysts must process large volumes of indicators and distinguish potentially harmful infrastructure from legitimate resources.



The current implementation focuses on URL-based phishing detection using machine-learning classification.



\## Objectives



\* Extract meaningful structural features from URLs.

\* Build a reproducible machine-learning pipeline for phishing detection.

\* Evaluate a baseline classification model on unseen data.

\* Examine which URL characteristics influence model predictions.

\* Explore how AI-assisted analysis could support CTI workflows.



\## Dataset



The project uses the \*\*PhiUSIIL Phishing URL Dataset\*\* from the UCI Machine Learning Repository.



The dataset contains \*\*235,795 URL records\*\* with a range of URL and webpage-related features.



For this project, the original labels are mapped to:



\* `0` — Benign / legitimate

\* `1` — Phishing



The raw dataset is intentionally kept locally and is excluded from Git using `.gitignore`.



\## Approach



The current pipeline uses a compact set of URL structural features:



\* URL length

\* Hostname length

\* Path length

\* Number of dots

\* Number of hyphens

\* Number of slashes

\* Number of question marks

\* Number of equals signs

\* Number of `@` symbols

\* HTTPS usage

\* IP-address-based hostname detection



The baseline model uses:



\*\*StandardScaler → Logistic Regression\*\*



The dataset is divided into:



\* \*\*80% training data\*\*

\* \*\*20% testing data\*\*



A stratified split with a fixed random seed is used to maintain reproducibility.



\## Results



Evaluation was performed on the held-out test set.



| Metric   | Result |

| -------- | -----: |

| Accuracy | 99.23% |

| ROC-AUC  | 0.9947 |



\### Confusion Matrix



```text

&#x20;                Predicted

&#x20;             Benign  Phishing

Actual Benign  26953      17

Actual Phishing 344   19845

```



The model achieved high performance on this dataset, but these results should \*\*not\*\* be interpreted as evidence that the model will achieve the same performance against real-world or previously unseen phishing campaigns.



\## Feature Analysis



The logistic regression coefficients provide an initial view of which features are associated with the model's predictions.



The strongest coefficients in the current experiment include:



\* Number of URL slashes

\* HTTPS usage

\* Number of hyphens

\* Hostname length

\* Path length



These coefficients represent statistical associations learned by the model. They should not be interpreted as evidence that a particular URL characteristic directly causes a URL to be malicious.



\## Limitations



This is an initial baseline rather than a production phishing-detection system.



Current limitations include:



\* The feature set is intentionally small.

\* The model uses only URL structural characteristics.

\* The evaluation uses a single train/test split.

\* Dataset-specific patterns may influence performance.

\* High benchmark performance does not guarantee real-world generalization.

\* Some feature definitions require further refinement; for example, URL slash counts can capture normal URL formatting.



\## Future Work



Planned improvements include:



1\. Refine URL feature engineering.

2\. Compare Logistic Regression with tree-based models.

3\. Perform cross-validation and additional validation experiments.

4\. Add precision, recall, F1-score and ROC curves.

5\. Add model explainability.

6\. Develop IOC enrichment and correlation capabilities.

7\. Explore integration with CTI workflows and threat-intelligence platforms.

8\. Investigate AI-assisted analyst workflows for resource-constrained CSIRT environments.



\## Project Structure



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

│       ├── features.py

│       ├── prepare\_data.py

│       ├── model.py

│       ├── evaluate.py

│       ├── download\_data.py

│       ├── prepare\_real\_data.py

│       └── train\_real\_model.py

│

├── tests/                # Project tests

│

├── .gitignore

├── requirements.txt

└── README.md

```



\## Research Direction



This project is part of a broader exploration of \*\*AI-assisted cyber threat intelligence\*\*.



The long-term goal is to investigate how machine learning can help CTI analysts process large volumes of threat data, identify patterns, correlate indicators and prioritize potentially significant threats while keeping human analysts involved in the decision-making process.



The project is particularl



