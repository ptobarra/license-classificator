"""
API integration tests for the License Classificator service.

This module provides basic smoke tests for the FastAPI endpoints to ensure
the service is operational and can handle requests. Tests verify endpoint
availability and expected response codes without requiring a running LLM.

Tests are designed to be lightweight and run in CI/CD pipelines without
external dependencies like Ollama or OpenAI.

Example:
    Run tests with pytest from the project root:

    ```bash
    pytest tests/test_api.py -v
    ```

Note:
    These tests use FastAPI's TestClient which doesn't require the server
    to be running. Database operations use the in-memory SQLite instance
    configured in [`app.db.session`](app/db/session.py).

Planned Extensions:
    - Mock LLM responses to test classification logic
    - Golden dataset accuracy benchmarks
    - Manual override workflow validation
    - Error handling coverage (invalid inputs, missing files)
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_licenses_ok():
    """
    Verify that the GET /licenses endpoint is accessible and returns successfully.

    Tests the [`list_licenses`](app/api/routes.py) endpoint to ensure it can
    retrieve license records from the database. This is a smoke test that
    validates basic API functionality.

    Expected behavior:
        - HTTP 200 status code
        - JSON array response (may be empty if no licenses ingested)

    Example:
        >>> from fastapi.testclient import TestClient
        >>> from app.main import app
        >>> client = TestClient(app)
        >>> response = client.get("/licenses")
        >>> response.status_code
        200
    """
    r = client.get("/licenses")
    assert r.status_code == 200


def test_classify_endpoint_exists():
    """
    Verify that the POST /classify endpoint exists and is reachable.

    Tests the [`classify_all`](app/api/routes.py) endpoint availability without
    requiring a running LLM service. Accepts both success (200) and server error
    (500) responses since the LLM may not be available in test environments.

    Expected behavior:
        - HTTP 200 if Ollama is running and licenses.xlsx exists
        - HTTP 500 if LLM is unavailable or file is missing
        - Endpoint is registered and routable

    Note:
        This is an existence test, not a full integration test. For production
        testing, use mocked LLM responses or ensure Ollama is running.

    Example:
        >>> response = client.post("/classify")
        >>> assert response.status_code in (200, 500)
    """
    r = client.post("/classify")
    assert r.status_code in (
        200,
        500,
    )  # 500 possible if LLM not running; endpoint exists
