"""Command-line argument BMI calculator wrapper."""

import sys

try:
    from day03.bmi_service import evaluate_bmi, CM_TO_M_CONVERSION_THRESHOLD
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi, CM_TO_M_CONVERSION_THRESHOLD


def main():
    """Run BMI calculation using sys.argv input."""
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python day03/cli_argv.py <weight> <height> [unit_system]")
        print("  unit_system: 'metric' (default, kg/m) or 'imperial' (lbs/in)")
        print(f"  Note: For metric units, height can be in meters or centimeters (>{CM_TO_M_CONVERSION_THRESHOLD} cm auto-converts)")
        return

    try:
        weight = float(sys.argv[1])
        height = float(sys.argv[2])
        
        # Get unit system (default to metric)
        unit_system = sys.argv[3].lower() if len(sys.argv) == 4 else "metric"
        
        if unit_system not in ("metric", "imperial"):
            print("Error: unit_system must be 'metric' or 'imperial'")
            return
        
        bmi, category = evaluate_bmi(weight, height, unit_system)

        print(f"BMI: {bmi}")
        print(f"Category: {category}")
        print(f"Unit System: {unit_system}")
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
