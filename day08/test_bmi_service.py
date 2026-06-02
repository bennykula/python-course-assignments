"""Unit tests for the shared BMI service module."""

import unittest

from day08.bmi_service import evaluate_bmi


class TestBmiService(unittest.TestCase):
    """Test cases for BMI calculation and categorization logic."""

    def test_underweight_case(self):
        bmi, category = evaluate_bmi(50, 1.8)
        self.assertEqual(bmi, 15.43)
        self.assertEqual(category, "Underweight")

    def test_normal_weight_case(self):
        bmi, category = evaluate_bmi(68, 1.75)
        self.assertEqual(bmi, 22.2)
        self.assertEqual(category, "Normal weight")

    def test_overweight_boundary(self):
        bmi, category = evaluate_bmi(81, 1.8)
        self.assertEqual(bmi, 25.0)
        self.assertEqual(category, "Overweight")

    def test_cm_to_meters_auto_conversion(self):
        bmi, category = evaluate_bmi(68, 175, "metric")
        self.assertEqual(bmi, 22.2)
        self.assertEqual(category, "Normal weight")

    def test_imperial_normal_weight(self):
        bmi, category = evaluate_bmi(150, 69, "imperial")
        self.assertEqual(bmi, 22.15)
        self.assertEqual(category, "Normal weight")

    def test_imperial_overweight(self):
        bmi, category = evaluate_bmi(180, 69, "imperial")
        self.assertEqual(bmi, 26.58)
        self.assertEqual(category, "Overweight")

    def test_invalid_unit_system_raises_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(70, 1.75, "invalid_unit")

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


if __name__ == "__main__":
    unittest.main()
