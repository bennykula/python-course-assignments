# BMI Calculator

A simple Python program that calculates your Body Mass Index (BMI) based on user input.

## What is BMI?

Body Mass Index (BMI) is a measure of body fat based on height and weight. The formula is:

```
BMI = weight (kg) / height (m)²
```

## Features

- Accepts weight in kilograms and height in meters from the user
- Calculates BMI automatically
- Categorizes BMI into: Underweight, Normal weight, Overweight, or Obese
- Input validation to ensure positive numbers
- Error handling for invalid inputs

## BMI Categories

| BMI Range | Category |
|-----------|----------|
| < 18.5 | Underweight |
| 18.5 - 24.9 | Normal weight |
| 25.0 - 29.9 | Overweight |
| ≥ 30.0 | Obese |

## How to Run

Run the program from your terminal:

```bash
python day02.py
```

## Example Usage

```
========================================
Welcome to the BMI Calculator!
========================================
Enter your weight in kilograms (kg): 70
Enter your height in meters (m): 1.75

========================================
Your BMI: 22.86
Category: Normal weight
========================================
```

## Requirements

- Python 3.x

## Notes

- Enter height in **meters** (e.g., 1.75 for 5'9")
- Enter weight in **kilograms** (e.g., 70 for ~154 lbs)
- The program will validate that inputs are positive numbers

## Development
used github copilot in vscode. prompt: "write a simple python program to calculate bmi. accept inputs from user with `input`. write a README.md to describe the program."