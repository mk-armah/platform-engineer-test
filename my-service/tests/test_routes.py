from fastapi.testclient import TestClient

from my_service.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    data = response.json()
    assert "status_code" in data


def test_application_status():
    response = client.get("/api/v1/argocd/application_status")
    assert response.status_code == 200
    data = response.json()
    assert "applications" in data


def test_list_projects():
    response = client.get("/api/v1/argocd/list_projects")
    assert response.status_code == 200
    data = response.json()
    assert "projects" in data
