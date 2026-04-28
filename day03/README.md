# Day 03 - BMI Calculator (3 Interfaces)

This folder contains one shared BMI logic module and three different user interfaces.

## Structure

- `bmi_service.py`: Shared library module.
- `main.py`: Standard input version using `input()`.
- `cli_argv.py`: Command-line argument version using `sys.argv`.
- `gui_tkinter.py`: GUI version using Tkinter.
- `test_bmi_service.py`: Unit tests for shared BMI logic.

## Shared Module

The shared module exposes one public function:

- `evaluate_bmi(weight, height)`

It does all of the following:

- Validates positive input values.
- Calculates BMI.
- Determines BMI category.
- Returns `(bmi, category)`.

## Run Each Interface

From the repository root:

1. Standard input

```bash
python day03/main.py
```

2. Command line arguments

```bash
python day03/cli_argv.py 70 1.75
```

3. Tkinter GUI

```bash
python day03/gui_tkinter.py
```

## Run Tests

```bash
python -m unittest day03/test_bmi_service.py
```

## Development
used github copilot in vscode. prompt:

>> - move `calculate_bmi`, `get_bmi` into a new module (use it in this file). wrap them in one function that the module exports.
>> 
>> - Create 3 versions of the program for 3 different ways to interact with the users. Each one uses the shared library.
>> 
>> 1. uses standard input (the input function)
>> 2. uses the command line (the sys.argv list)
>> 3. uses GUI. use tkinter.
>> 
>> Create a test file with a number of test-cases for the module (not the interface wrappers).
>> document the code in a README.md file.
