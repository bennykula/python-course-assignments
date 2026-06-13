"""Business logic for Day 9: load data, train a model, make predictions.

This version uses sklearn's `load_breast_cancer` dataset instead of Iris so
the assignment is different from the in-class Iris example.
"""
from typing import Optional, Tuple

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def load_data(path: Optional[str] = None) -> Tuple[pd.DataFrame, pd.Series]:
    """Load dataset.

    If `path` is provided, expects a CSV with the target in a column named
    `target` or `diagnosis`, or as the last column. Otherwise loads
    sklearn's breast cancer dataset.
    """
    if path:
        df = pd.read_csv(path)
        # common target column names
        if "diagnosis" in df.columns:
            X = df.drop(columns=["diagnosis"]).copy()
            y = df["diagnosis"].copy()
        elif "target" in df.columns:
            X = df.drop(columns=["target"]).copy()
            y = df["target"].copy()
        else:
            X = df.iloc[:, :-1].copy()
            y = df.iloc[:, -1].copy()
        return X, y

    data = load_breast_cancer(as_frame=True)
    df = data.frame
    feature_cols = data.feature_names
    X = df[feature_cols]
    y = df["target"]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series, test_size: float = 0.2, random_state: int = 42):
    """Train a simple LogisticRegression pipeline and return model and accuracy.

    Returns (model, accuracy, (X_test, y_test)).
    """
    stratify = y if len(set(y)) > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=stratify
    )
    model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=500))
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return model, acc, (X_test, y_test)


def predict(model, X: pd.DataFrame):
    """Return predictions for X using the provided model."""
    return model.predict(X)
