"""Pytest fixtures."""
import shutil
import uuid
from pathlib import Path

import pytest

from api.user_api import UserAPI
from models.user import UserData
from utils.assertions import AssertionHelper


ALLURE_DIR = Path(__file__).parent.parent / "allure-results"


def pytest_sessionfinish(session, exitstatus):
    """Cleanup allure results in success."""
    if exitstatus == 0 and ALLURE_DIR.exists():
        shutil.rmtree(ALLURE_DIR)


@pytest.fixture
def check():
    return AssertionHelper()


@pytest.fixture
def api_client():
    return UserAPI()


@pytest.fixture
def user_data():
    return UserData.generate()


@pytest.fixture
def created_user(api_client, user_data):
    """Create user and return (client, data) tuple."""
    resp = api_client.create_user(user_data)
    assert resp.status_code == 200, f"Setup failed: {resp.text}"
    return api_client, user_data


@pytest.fixture
def updated_user_data():
    return UserData.generate(prefix="updated")


@pytest.fixture
def unique_email():
    return f"test_{uuid.uuid4().hex[:8]}@test.com"


@pytest.fixture
def unique_login():
    return f"user_{uuid.uuid4().hex[:8]}"
