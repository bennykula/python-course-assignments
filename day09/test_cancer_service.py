"""Tests for the Day 9 breast-cancer service."""
from day09.iris_service import load_data, train_model


def test_train_on_breast_cancer():
    X, y = load_data()
    model, acc, _ = train_model(X, y, test_size=0.25, random_state=0)
    # Breast cancer dataset is also easy; expect good accuracy from logistic.
    assert acc >= 0.85
