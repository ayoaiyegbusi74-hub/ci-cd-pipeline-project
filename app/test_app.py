import pytest
from app import app, calculate_bmi, bmi_category


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# --- unit tests for pure functions ---

def test_calculate_bmi_normal():
    assert calculate_bmi(70, 1.75) == 22.86


def test_calculate_bmi_zero_weight_raises():
    with pytest.raises(ValueError):
        calculate_bmi(0, 1.75)


def test_calculate_bmi_negative_height_raises():
    with pytest.raises(ValueError):
        calculate_bmi(70, -1.75)


@pytest.mark.parametrize(
    "bmi_value,expected",
    [
        (17.0, "Underweight"),
        (22.0, "Normal weight"),
        (27.0, "Overweight"),
        (32.0, "Obesity"),
    ],
)
def test_bmi_category(bmi_value, expected):
    assert bmi_category(bmi_value) == expected


# --- integration tests for HTTP endpoints ---

def test_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_bmi_endpoint_success(client):
    resp = client.post("/bmi", json={"weight_kg": 70, "height_m": 1.75})
    assert resp.status_code == 200
    body = resp.get_json()
    assert body["bmi"] == 22.86
    assert body["category"] == "Normal weight"


def test_bmi_endpoint_missing_fields(client):
    resp = client.post("/bmi", json={"weight_kg": 70})
    assert resp.status_code == 400


def test_bmi_endpoint_invalid_values(client):
    resp = client.post("/bmi", json={"weight_kg": -5, "height_m": 1.75})
    assert resp.status_code == 400
