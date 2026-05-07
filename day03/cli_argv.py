"""Command-line argument BMI calculator wrapper."""

import sys

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


def main():
    """Run BMI calculation using sys.argv input.

    Usage (metric):   python day03/cli_argv.py <weight_kg> <height_m>
    Usage (imperial): python day03/cli_argv.py --imperial <weight_lbs> <height_in>
    """
    args = sys.argv[1:]
    imperial = "--imperial" in args
    if imperial:
        args = [a for a in args if a != "--imperial"]

    if len(args) != 2:
        print("Usage (metric):   python day03/cli_argv.py <weight_kg> <height_m>")
        print("Usage (imperial): python day03/cli_argv.py --imperial <weight_lbs> <height_in>")
        return

    try:
        weight = float(args[0])
        height = float(args[1])
        bmi, category = evaluate_bmi(weight, height, imperial=imperial)

        unit_label = "lbs/in (imperial)" if imperial else "kg/m (metric)"
        print(f"Units: {unit_label}")
        print(f"BMI: {bmi}")
        print(f"Category: {category}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
