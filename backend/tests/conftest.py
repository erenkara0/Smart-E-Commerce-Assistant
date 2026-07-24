import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient


TEST_TEMP_DIR = tempfile.TemporaryDirectory()
TEST_DATABASE_PATH = Path(TEST_TEMP_DIR.name) / "test.db"

os.environ["APP_ENV"] = "testing"
os.environ["SQLITE_DB_PATH"] = str(TEST_DATABASE_PATH)
os.environ["CORS_ALLOWED_ORIGINS"] = '["http://testserver"]'
os.environ["CORS_ALLOW_CREDENTIALS"] = "false"

from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client