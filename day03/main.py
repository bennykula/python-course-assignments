"""
BMI Calculator
A simple program to calculate Body Mass Index based on user input.
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
        # Get user input
        weight = float(input("Enter your weight in kilograms (kg): "))
        height = float(input("Enter your height in meters (m): "))
        
        bmi, category = evaluate_bmi(weight, height)
        
        # Display results
        print("\n" + "=" * 40)
        print(f"Your BMI: {bmi}")
        print(f"Category: {category}")
        print("=" * 40)
        
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
