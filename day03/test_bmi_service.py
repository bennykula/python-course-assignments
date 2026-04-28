"""Unit tests for the shared BMI service module."""

import unittest

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


class TestBmiService(unittest.TestCase):
    """Test cases for BMI calculation and categorization logic."""

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


if __name__ == "__main__":
    unittest.main()
