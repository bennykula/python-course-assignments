"""Unit tests for the shared BMI service module."""

import unittest

try:
    from day03.bmi_service import evaluate_bmi, convert_imperial_to_metric
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi, convert_imperial_to_metric


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


class TestImperialSupport(unittest.TestCase):
    """Test cases for imperial unit conversion and evaluation."""

    def test_convert_imperial_to_metric_weight(self):
        weight_kg, _ = convert_imperial_to_metric(154, 70)
        self.assertAlmostEqual(weight_kg, 69.85, places=2)

    def test_convert_imperial_to_metric_height(self):
        _, height_m = convert_imperial_to_metric(154, 70)
        self.assertAlmostEqual(height_m, 1.778, places=3)

    def test_evaluate_bmi_imperial_normal_weight(self):
        # 154 lbs, 70 in → ~69.85 kg, ~1.778 m → BMI ~22.09 (Normal weight)
        bmi, category = evaluate_bmi(154, 70, imperial=True)
        self.assertEqual(category, "Normal weight")
        self.assertAlmostEqual(bmi, 22.09, places=1)

    def test_evaluate_bmi_imperial_equals_metric(self):
        # 70 kg, 1.75 m in metric should give same BMI as 154.32 lbs, 68.9 in
        weight_lbs = 70 / 0.453592
        height_in = 1.75 * 39.3701
        bmi_imperial, category_imperial = evaluate_bmi(weight_lbs, height_in, imperial=True)
        bmi_metric, category_metric = evaluate_bmi(70, 1.75)
        self.assertEqual(bmi_imperial, bmi_metric)
        self.assertEqual(category_imperial, category_metric)

    def test_evaluate_bmi_imperial_underweight(self):
        # 100 lbs, 70 in → ~45.36 kg, ~1.778 m → BMI ~14.34 (Underweight)
        bmi, category = evaluate_bmi(100, 70, imperial=True)
        self.assertEqual(category, "Underweight")

    def test_evaluate_bmi_imperial_obese(self):
        # 300 lbs, 70 in → ~136.08 kg, ~1.778 m → BMI ~43.05 (Obese)
        bmi, category = evaluate_bmi(300, 70, imperial=True)
        self.assertEqual(category, "Obese")

    def test_evaluate_bmi_imperial_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(0, 70, imperial=True)

        with self.assertRaises(ValueError):
            evaluate_bmi(154, 0, imperial=True)

    def test_evaluate_bmi_imperial_negative_raises_value_error(self):
        with self.assertRaises(ValueError):
            evaluate_bmi(-154, 70, imperial=True)

        with self.assertRaises(ValueError):
            evaluate_bmi(154, -70, imperial=True)


if __name__ == "__main__":
    unittest.main()
