"""Tkinter GUI BMI calculator wrapper."""

import tkinter as tk
from tkinter import ttk

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


def calculate_and_display(weight_var, height_var, result_var):
    """Read user input from widgets, calculate BMI, and display results."""
    try:
        weight = float(weight_var.get())
        height = float(height_var.get())
        bmi, category = evaluate_bmi(weight, height)
        result_var.set(f"BMI: {bmi} | Category: {category}")
    except ValueError as error:
        result_var.set(f"Error: {error}")


def main():
    """Build and run the Tkinter BMI calculator UI."""
    root = tk.Tk()
    root.title("BMI Calculator")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")

    weight_var = tk.StringVar()
    height_var = tk.StringVar()
    result_var = tk.StringVar(value="Enter values and click Calculate")

    ttk.Label(frame, text="Weight (kg):").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
    ttk.Entry(frame, textvariable=weight_var, width=20).grid(row=0, column=1, pady=(0, 8))

    ttk.Label(frame, text="Height (m):").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
    ttk.Entry(frame, textvariable=height_var, width=20).grid(row=1, column=1, pady=(0, 8))

    ttk.Button(
        frame,
        text="Calculate",
        command=lambda: calculate_and_display(weight_var, height_var, result_var),
    ).grid(row=2, column=0, columnspan=2, pady=(4, 8))

    ttk.Label(frame, textvariable=result_var).grid(row=3, column=0, columnspan=2, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    main()
