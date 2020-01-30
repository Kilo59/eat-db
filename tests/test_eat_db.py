"""
tests.test_eat_db.py
~~~~~~~~~~~~~~~~~~~~
High level basic project tests.
"""
import logging

import pytest
from starlette.testclient import TestClient

import eat_db.api.main
from eat_db import __version__

TEST_LOGGER = logging.getLogger("tests")
TEST_LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def api_client():
    """Return a starlette TestClient for the `app`."""
    client = TestClient(eat_db.api.main.app)
    return client


def test_version():
    assert __version__ == "0.0.1"


def test_liveness(api_client):
    response = api_client.get("/status/liveness")
    TEST_LOGGER.info(f"liveness: {response}")
    assert response.status_code == 200
