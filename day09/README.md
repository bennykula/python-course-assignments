# Day 9 — Simple breast-cancer prediction

This assignment implements a small machine-learning example using the
`breast_cancer` dataset from `scikit-learn`.

Files:

- `iris_service.py`: business logic (data loading, training, prediction). Uses
	`load_breast_cancer` by default.
- `cli_argv.py`, `main.py`: simple CLI wrapper to run training and print accuracy.
- `requirements.txt`: dependencies.
- `test_iris_service.py`: unit tests.

Run locally:

```bash
python3 -m venv day09/.venv
source day09/.venv/bin/activate
pip install -r day09/requirements.txt
python -m day09.cli_argv
```

If you want to use your own CSV, pass its path as the first argument. The CSV
may contain a `diagnosis` or `target` column for the target, or the target can
be the last column.

Prompts I used with ChatGPT/Copilot while developing:

1. "Create a small Python module that loads a scikit-learn classification dataset and trains a scikit-learn logistic regression pipeline. Include functions for loading data, training returning accuracy, and predicting."
2. "Add a simple CLI wrapper that accepts an optional CSV path and prints test accuracy."
