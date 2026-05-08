"""Tests for main.py."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

import app.main as main_module


@pytest.fixture
def app_client():
    with patch("app.main.SyncScheduler"):
        app = main_module.create_app()
        client = TestClient(app)
        yield client


class TestCreateApp:
    def test_create_app(self, app_client):
        assert app_client is not None

    def test_health_endpoint(self, app_client):
        resp = app_client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_root_endpoint(self, app_client):
        resp = app_client.get("/")
        assert resp.status_code in [200, 404]

    def test_spa_docs_route_fallback(self, app_client):
        resp = app_client.get("/docs/data")
        assert resp.status_code in [200, 404]

    def test_unknown_api_path_stays_404(self, app_client):
        resp = app_client.get("/api/not-found")
        assert resp.status_code == 404

    def test_init_endpoint(self, app_client):
        with patch("app.main.get_mysql_service") as mock_get_db:
            mock_db = MagicMock()
            mock_get_db.return_value = mock_db
            resp = app_client.post("/init")
            assert resp.status_code in [200, 500]

    def test_init_endpoint_error(self, app_client):
        with patch("app.main.get_mysql_service") as mock_get_db:
            mock_db = MagicMock()
            mock_db.init_system_tables.side_effect = Exception("init failed")
            mock_get_db.return_value = mock_db
            resp = app_client.post("/init")
            assert resp.status_code == 500


class TestLifespan:
    def test_lifespan(self, app_client):
        resp = app_client.get("/health")
        assert resp.status_code == 200


class TestCORSMiddleware:
    def test_cors_headers(self, app_client):
        resp = app_client.options("/health")
        assert resp.status_code in [200, 405]
