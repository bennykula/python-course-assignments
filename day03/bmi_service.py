"""Shared BMI service logic used by all interfaces."""

_LBS_PER_KG = 0.453592
_INCHES_PER_METER = 39.3701


def convert_imperial_to_metric(weight_lbs, height_in):
    """Convert imperial measurements to metric units.

    Args:
        weight_lbs (float): Weight in pounds.
        height_in (float): Height in inches.

    Returns:
        tuple[float, float]: (weight_kg, height_m)
    """
    weight_kg = weight_lbs * _LBS_PER_KG
    height_m = height_in / _INCHES_PER_METER
    return weight_kg, height_m


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


def evaluate_bmi(weight, height, imperial=False):
    """Validate input, then return BMI and category.

    Args:
        weight (float): Weight in kg (metric) or lbs (imperial).
        height (float): Height in meters (metric) or inches (imperial).
        imperial (bool): If True, treat inputs as imperial units (lbs/inches)
            and convert to metric before calculating. Defaults to False.

    Returns:
        tuple[float, str]: (bmi_value, bmi_category)

    Raises:
        ValueError: If weight/height are not positive numbers.
    """
    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive numbers.")

    if imperial:
        weight, height = convert_imperial_to_metric(weight, height)

    bmi = calculate_bmi(weight, height)
    return bmi, get_bmi_category(bmi)


__all__ = ["evaluate_bmi", "convert_imperial_to_metric"]
