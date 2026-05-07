"""
BMI Calculator
A simple program to calculate Body Mass Index based on user input.
Supports both Metric (kg/m) and Imperial (lbs/in) units.
"""

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


def main():
    """Main function for the standard-input BMI calculator."""
    print("=" * 40)
    print("Welcome to the BMI Calculator!")
    print("=" * 40)
    
    try:
        # Let user choose unit system
        print("\nSelect unit system:")
        print("1. Metric (kg and meters)")
        print("2. Imperial (lbs and inches)")
        
        unit_choice = input("\nEnter 1 or 2: ").strip()
        
        if unit_choice == "1":
            unit_system = "metric"
            weight_unit = "kilograms (kg)"
            height_unit = "meters (m) or centimeters (cm)"
            print("\nYou selected Metric units.")
        elif unit_choice == "2":
            unit_system = "imperial"
            weight_unit = "pounds (lbs)"
            height_unit = "inches (in)"
            print("\nYou selected Imperial units.")
        else:
            print("Invalid choice. Defaulting to Metric.")
            unit_system = "metric"
            weight_unit = "kilograms (kg)"
            height_unit = "meters (m) or centimeters (cm)"
        
        # Get user input
        weight = float(input(f"Enter your weight in {weight_unit}: "))
        height = float(input(f"Enter your height in {height_unit}: "))
        
        bmi, category = evaluate_bmi(weight, height, unit_system)
        
        # Display results
        print("\n" + "=" * 40)
        print(f"Your BMI: {bmi}")
        print(f"Category: {category}")
        print("=" * 40)
        
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
