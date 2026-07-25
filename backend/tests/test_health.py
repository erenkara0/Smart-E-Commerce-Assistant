from fastapi.testclient import TestClient


def test_health_endpoint_returns_success(
    client: TestClient,
) -> None:
    response = client.get("/health")

    assert response.status_code == 200

    response_body = response.json()

    assert response_body["success"] is True
    assert response_body["message"] == "API is healthy"
    assert response_body["data"]["status"] == "ok"