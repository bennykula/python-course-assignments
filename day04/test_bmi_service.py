"""Unit tests for the shared BMI service module."""

import unittest

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


class TestBmiService(unittest.TestCase):
    """Test cases for BMI calculation and categorization logic."""

    # Metric tests (original tests)
    def test_underweight_case(self):
        bmi, category = evaluate_bmi(50, 1.8)
        self.assertEqual(bmi, 15.43)
        self.assertEqual(category, "Underweight")

    def test_normal_weight_lower_boundary(self):
        bmi, category = evaluate_bmi(59.94, 1.8)
        self.assertEqual(bmi, 18.5)
        self.assertEqual(category, "Normal weight")

    def test_normal_weight_case(self):
        bmi, category = evaluate_bmi(68, 1.75)
        self.assertEqual(bmi, 22.2)
        self.assertEqual(category, "Normal weight")

    def test_overweight_boundary(self):
        bmi, category = evaluate_bmi(81, 1.8)
        self.assertEqual(bmi, 25.0)
        self.assertEqual(category, "Overweight")

    def test_obese_boundary(self):
        bmi, category = evaluate_bmi(97.2, 1.8)
        self.assertEqual(bmi, 30.0)
        self.assertEqual(category, "Obese")

    def test_zero_values_raise_value_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(0, 1.75)

        with self.assertRaises(ValueError):
            evaluate_bmi(70, 0)

    def test_negative_values_raise_value_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(-70, 1.75)

        with self.assertRaises(ValueError):
            evaluate_bmi(70, -1.75)

    # Centimeter conversion tests (Issue #1)
    def test_cm_to_meters_auto_conversion(self):
        # 175 cm should be auto-converted to 1.75 m
        bmi, category = evaluate_bmi(68, 175, "metric")
        self.assertEqual(bmi, 22.2)
        self.assertEqual(category, "Normal weight")

    def test_cm_conversion_underweight(self):
        bmi, category = evaluate_bmi(50, 180, "metric")
        self.assertEqual(bmi, 15.43)
        self.assertEqual(category, "Underweight")

    # Imperial unit tests (Issue #2)
    def test_imperial_underweight(self):
        # 110 lbs, 5'11" (71 inches)
        bmi, category = evaluate_bmi(110, 71, "imperial")
        self.assertEqual(bmi, 15.34)
        self.assertEqual(category, "Underweight")

    def test_imperial_normal_weight(self):
        # 150 lbs, 5'9" (69 inches)
        bmi, category = evaluate_bmi(150, 69, "imperial")
        self.assertEqual(bmi, 22.15)
        self.assertEqual(category, "Normal weight")

    def test_imperial_overweight(self):
        # 180 lbs, 5'9" (69 inches)
        bmi, category = evaluate_bmi(180, 69, "imperial")
        self.assertEqual(bmi, 26.58)
        self.assertEqual(category, "Overweight")

    def test_imperial_obese(self):
        # 250 lbs, 5'9" (69 inches)
        bmi, category = evaluate_bmi(250, 69, "imperial")
        self.assertEqual(bmi, 36.91)
        self.assertEqual(category, "Obese")

    # Invalid unit system test
    def test_invalid_unit_system_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(70, 1.75, "invalid_unit")

    def test_zero_values_imperial_raise_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(0, 70, "imperial")

        with self.assertRaises(ValueError):
            evaluate_bmi(150, 0, "imperial")


if __name__ == "__main__":
    unittest.main()
