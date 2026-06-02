"""Shared BMI service logic used by all interfaces."""

CM_TO_M_CONVERSION_THRESHOLD = 50


def calculate_bmi(weight, height, unit_system="metric"):
    """Calculate BMI given weight and height.

    Args:
        weight: Weight value (kg for metric, lbs for imperial)
        height: Height value (meters for metric, inches for imperial).
                If height > 50 with metric units, assumes cm and converts to meters.
        unit_system: "metric" (default) or "imperial"

    Returns:
        float: BMI value rounded to 2 decimal places
    """
    if unit_system == "metric" and height > CM_TO_M_CONVERSION_THRESHOLD:
        height = height / 100

    if unit_system == "imperial":
        bmi = (weight / (height ** 2)) * 703
    else:
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


def evaluate_bmi(weight, height, unit_system="metric"):
    """Validate input, then return BMI and category.

    Returns:
        tuple[float, str]: (bmi_value, bmi_category)

    Raises:
        ValueError: If weight/height are not positive numbers or invalid unit system.
    """
    if unit_system not in ("metric", "imperial"):
        raise ValueError("unit_system must be 'metric' or 'imperial'")

    if weight <= 0 or height <= 0:
        raise ValueError("Weight and height must be positive numbers.")

    bmi = calculate_bmi(weight, height, unit_system)
    return bmi, get_bmi_category(bmi)


__all__ = ["evaluate_bmi", "calculate_bmi", "get_bmi_category"]
