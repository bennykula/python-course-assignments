"""Simple CLI wrapper for the Day 9 breast-cancer example."""
import sys

from day09.iris_service import load_data, train_model


def run(argv=None):
    argv = argv or sys.argv
    path = None
    if len(argv) > 1:
        path = argv[1]
    X, y = load_data(path)
    model, acc, _ = train_model(X, y)
    print(f"Model trained on breast-cancer dataset. Test accuracy: {acc:.3f}")


if __name__ == "__main__":
    run()
