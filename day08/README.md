# Day 08 - BMI Web App (FastAPI)

This day reuses the BMI business logic and exposes it via a FastAPI web app.

## Install

From the repo root:

```bash
python -m pip install -r day08/requirements.txt
```

## Run

```bash
uvicorn day08.app:app --reload --port 8000
```

Open http://127.0.0.1:8000 for the BMI calculator site.

API docs are available at http://127.0.0.1:8000/docs.

## Example request (API)

```bash
curl -X POST http://127.0.0.1:8000/bmi \
  -H "Content-Type: application/json" \
  -d '{"weight": 68, "height": 1.75, "unit_system": "metric"}'
```

## Tests

```bash
python -m unittest day08/test_bmi_service.py
python -m unittest day08/test_web_app.py
```

## Development
Used GitHub Copilot in VSCode. Original prompt:
> Create a web application for my BMI calculator project (located in day03). Use the fastAPI web framework. Use my original business logic code to calculate BMI.

the results was an API web server (didn't server HTML). My next prompt was:
> the web app should be a site - not only and API endpoint