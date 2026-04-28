"""Shared BMI service logic used by all interfaces."""


def calculate_bmi(weight, height):
    """Calculate BMI given weight in kg and height in meters."""
    bmi = weight / (height ** 2)
    return round(bmi, 2)


def get_bmi_category(bmi):
    """Map a BMI value to its category."""
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def evaluate_bmi(weight, height):
    """Validate input, then return BMI and category.

    Returns:
        tuple[float, str]: (bmi_value, bmi_category)

    Raises:
        ValueError: If weight/height are not positive numbers.
    """
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive numbers.")

    bmi = calculate_bmi(weight, height)
    return bmi, get_bmi_category(bmi)


__all__ = ["evaluate_bmi"]
