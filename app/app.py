"""
Simple BMI Calculator API.

Endpoints:
  GET  /health         -> liveness/readiness check (used by container healthcheck)
  POST /bmi            -> body: {"weight_kg": float, "height_m": float}
                           returns: {"bmi": float, "category": str}
"""

from flask import Flask, request, jsonify

app = Flask(__name__)


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if weight_kg <= 0:
        raise ValueError("weight_kg must be greater than 0")
    if height_m <= 0:
        raise ValueError("height_m must be greater than 0")
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.post("/bmi")
def bmi():
    data = request.get_json(silent=True) or {}

    try:
        weight_kg = float(data["weight_kg"])
        height_m = float(data["height_m"])
    except (KeyError, TypeError, ValueError):
        return jsonify(error="weight_kg and height_m are required numeric fields"), 400

    try:
        result = calculate_bmi(weight_kg, height_m)
    except ValueError as exc:
        return jsonify(error=str(exc)), 400

    return jsonify(bmi=result, category=bmi_category(result)), 200


if __name__ == "__main__":
    # nosec B104 - binding to all interfaces is required for Docker port mapping to work
    app.run(host="0.0.0.0", port=8080)  # nosec B104
