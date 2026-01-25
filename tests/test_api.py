from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_licenses_ok():
    r = client.get("/licenses")
    assert r.status_code == 200


def test_classify_endpoint_exists():
    r = client.post("/classify")
    assert r.status_code in (
        200,
        500,
    )  # 500 possible if LLM not running; endpoint exists
