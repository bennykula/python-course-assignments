"""Tkinter GUI BMI calculator wrapper."""

import tkinter as tk
from tkinter import ttk

try:
    from day03.bmi_service import evaluate_bmi
except ModuleNotFoundError:
    from bmi_service import evaluate_bmi


def calculate_and_display(weight_var, height_var, result_var, imperial_var):
    """Read user input from widgets, calculate BMI, and display results."""
    try:
        weight = float(weight_var.get())
        height = float(height_var.get())
        imperial = imperial_var.get()
        bmi, category = evaluate_bmi(weight, height, imperial=imperial)
        result_var.set(f"BMI: {bmi} | Category: {category}")
    except ValueError as error:
        result_var.set(f"Error: {error}")


def update_labels(imperial_var, weight_label, height_label):
    """Update weight/height label text based on the selected unit system."""
    if imperial_var.get():
        weight_label.config(text="Weight (lbs):")
        height_label.config(text="Height (in):")
    else:
        weight_label.config(text="Weight (kg):")
        height_label.config(text="Height (m):")


def main():
    """Build and run the Tkinter BMI calculator UI."""
    root = tk.Tk()
    root.title("BMI Calculator")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=16)
    frame.grid(row=0, column=0, sticky="nsew")

    imperial_var = tk.BooleanVar(value=False)
    weight_var = tk.StringVar()
    height_var = tk.StringVar()
    result_var = tk.StringVar(value="Enter values and click Calculate")

    # Unit system toggle
    unit_frame = ttk.LabelFrame(frame, text="Unit System", padding=6)
    unit_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    ttk.Radiobutton(
        unit_frame, text="Metric (kg / m)", variable=imperial_var, value=False,
        command=lambda: update_labels(imperial_var, weight_label, height_label),
    ).grid(row=0, column=0, padx=(0, 16))
    ttk.Radiobutton(
        unit_frame, text="Imperial (lbs / in)", variable=imperial_var, value=True,
        command=lambda: update_labels(imperial_var, weight_label, height_label),
    ).grid(row=0, column=1)

    weight_label = ttk.Label(frame, text="Weight (kg):")
    weight_label.grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
    ttk.Entry(frame, textvariable=weight_var, width=20).grid(row=1, column=1, pady=(0, 8))

    height_label = ttk.Label(frame, text="Height (m):")
    height_label.grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(0, 8))
    ttk.Entry(frame, textvariable=height_var, width=20).grid(row=2, column=1, pady=(0, 8))

    ttk.Button(
        frame,
        text="Calculate",
        command=lambda: calculate_and_display(weight_var, height_var, result_var, imperial_var),
    ).grid(row=3, column=0, columnspan=2, pady=(4, 8))

    ttk.Label(frame, textvariable=result_var).grid(row=4, column=0, columnspan=2, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    main()
