"""Unit tests for the BMI FastAPI web app."""

import unittest

from fastapi.testclient import TestClient

from day08.app import app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("BMI Calculator", response.text)
        self.assertIn("<form", response.text)
        self.assertIn("name=\"weight\"", response.text)
        self.assertIn("name=\"height\"", response.text)

    def test_result_page_metric(self):
        response = self.client.get("/result?weight=68&height=1.75&unit_system=metric")
        self.assertEqual(response.status_code, 200)
        self.assertIn("BMI: 22.2", response.text)
        self.assertIn("Normal weight", response.text)

    def test_result_page_error(self):
        response = self.client.get("/result?weight=0&height=1.75&unit_system=metric")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Weight and height must be positive numbers.", response.text)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_bmi_metric(self):
        response = self.client.post("/bmi", json={"weight": 68, "height": 1.75})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["bmi"], 22.2)
        self.assertEqual(data["category"], "Normal weight")
        self.assertEqual(data["unit_system"], "metric")

    def test_bmi_metric_cm(self):
        response = self.client.post("/bmi", json={"weight": 68, "height": 175})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["bmi"], 22.2)
        self.assertEqual(data["category"], "Normal weight")
        self.assertEqual(data["unit_system"], "metric")

    def test_bmi_imperial(self):
        response = self.client.post(
            "/bmi", json={"weight": 150, "height": 69, "unit_system": "imperial"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["bmi"], 22.15)
        self.assertEqual(data["category"], "Normal weight")
        self.assertEqual(data["unit_system"], "imperial")

    def test_invalid_unit_system(self):
        response = self.client.post(
            "/bmi", json={"weight": 70, "height": 1.75, "unit_system": "invalid"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "unit_system must be 'metric' or 'imperial'"
        )

    def test_non_positive_values(self):
        response = self.client.post("/bmi", json={"weight": 0, "height": 1.75})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "Weight and height must be positive numbers."
        )


if __name__ == "__main__":
    unittest.main()
