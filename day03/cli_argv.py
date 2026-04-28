"""Command-line argument BMI calculator wrapper."""

import sys

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


def main():
    """Run BMI calculation using sys.argv input."""
    if len(sys.argv) != 3:
        print("Usage: python day03/cli_argv.py <weight_kg> <height_m>")
        return

    try:
        weight = float(sys.argv[1])
        height = float(sys.argv[2])
        bmi, category = evaluate_bmi(weight, height)

        print(f"BMI: {bmi}")
        print(f"Category: {category}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
