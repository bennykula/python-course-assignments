"""FastAPI web app for BMI calculation."""

import html

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from day08.bmi_service import evaluate_bmi

app = FastAPI(title="BMI Calculator")


class BmiRequest(BaseModel):
    weight: float
    height: float
    unit_system: str = "metric"


class BmiResponse(BaseModel):
    bmi: float
    category: str
    unit_system: str


def render_page(content):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>BMI Calculator</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 0; background: #f6f7fb; color: #1b1b1b; }}
    .wrap {{ max-width: 720px; margin: 40px auto; padding: 24px; }}
    .card {{ background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 10px 30px rgba(10, 20, 30, 0.08); }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    p {{ margin: 0 0 16px; color: #4b5563; }}
    form {{ display: grid; gap: 12px; }}
    label {{ font-size: 14px; font-weight: 600; }}
    input, select {{ padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 8px; font-size: 14px; }}
    button {{ padding: 12px 16px; border: 0; border-radius: 8px; background: #2563eb; color: #fff; font-weight: 600; cursor: pointer; }}
    button:hover {{ background: #1d4ed8; }}
    .alert {{ padding: 12px; border-radius: 8px; margin-bottom: 12px; }}
    .alert.error {{ background: #fee2e2; color: #991b1b; }}
    .alert.ok {{ background: #dcfce7; color: #166534; }}
    .hint {{ font-size: 13px; color: #6b7280; }}
    .footer {{ margin-top: 16px; font-size: 13px; color: #6b7280; }}
    a {{ color: #2563eb; text-decoration: none; }}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="card">
      {content}
    </div>
  </div>
</body>
</html>"""


def render_form(weight="", height="", unit_system="metric", error=None, result=None):
    safe_weight = html.escape(str(weight)) if weight != "" else ""
    safe_height = html.escape(str(height)) if height != "" else ""
    safe_unit = unit_system if unit_system in ("metric", "imperial") else "metric"

    error_html = (
        f"<div class=\"alert error\">{html.escape(error)}</div>" if error else ""
    )
    result_html = (
        f"<div class=\"alert ok\">{html.escape(result)}</div>" if result else ""
    )

    content = f"""
<h1>BMI Calculator</h1>
<p>Enter your weight and height to calculate BMI.</p>
{error_html}
{result_html}
<form action="/result" method="get">
  <div>
    <label for="weight">Weight</label>
    <input id="weight" name="weight" type="number" step="any" value="{safe_weight}" placeholder="e.g. 68" required>
  </div>
  <div>
    <label for="height">Height</label>
    <input id="height" name="height" type="number" step="any" value="{safe_height}" placeholder="e.g. 1.75 or 175" required>
  </div>
  <div>
    <label for="unit_system">Unit System</label>
    <select id="unit_system" name="unit_system">
      <option value="metric" {'selected' if safe_unit == 'metric' else ''}>Metric (kg, m/cm)</option>
      <option value="imperial" {'selected' if safe_unit == 'imperial' else ''}>Imperial (lb, in)</option>
    </select>
  </div>
  <button type="submit">Calculate BMI</button>
</form>
<p class="hint">Metric expects kg and m (or cm). Imperial expects lb and inches.</p>
<div class="footer">API docs: <a href="/docs">/docs</a></div>
"""
    return render_page(content)


@app.get("/", response_class=HTMLResponse)
def index():
    return HTMLResponse(render_form())


@app.get("/result", response_class=HTMLResponse)
def result(weight: float, height: float, unit_system: str = "metric"):
    try:
        bmi, category = evaluate_bmi(weight, height, unit_system)
    except ValueError as exc:
        return HTMLResponse(
            render_form(weight, height, unit_system, error=str(exc)), status_code=400
        )

    message = f"BMI: {bmi} ({category})"
    return HTMLResponse(
        render_form(weight, height, unit_system, result=message), status_code=200
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/bmi", response_model=BmiResponse)
def calculate_bmi_endpoint(payload: BmiRequest):
    try:
        bmi, category = evaluate_bmi(payload.weight, payload.height, payload.unit_system)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"bmi": bmi, "category": category, "unit_system": payload.unit_system}
