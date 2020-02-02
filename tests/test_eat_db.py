"""
tests.test_eat_db.py
~~~~~~~~~~~~~~~~~~~~
High level basic project tests.
"""
# stdlib
import logging
from pprint import pformat as pf

import pytest
from starlette.testclient import TestClient

# project
import eat_db.api.main
from eat_db import Food, Tags, __version__

TEST_LOGGER = logging.getLogger("tests")
TEST_LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def api_client():
    """Return a starlette TestClient for the `app`."""
    client = TestClient(eat_db.api.main.APP)
    return client


def test_version():
    assert __version__ == "0.0.1"


def test_liveness(api_client):
    response = api_client.get("/status/liveness")
    TEST_LOGGER.info(f"liveness: {response}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "json_test_params,",
    [
        {"tags": ["leftovers"]},
        pytest.param(
            {"tags": {"leftovers"}},
            marks=pytest.mark.xfail(
                reason="Incoming request must be valid json. Python sets are not.",
                strict=True,
            ),
        ),
    ],
)
def test_add_food(request, api_client, json_test_params):
    json_body = {"name": request.node.name}
    json_body.update(json_test_params)
    print(f"\trequest json:\n{pf(json_body)}")
    response = api_client.post("/fridge", json=json_body)
    print(f"{response}\n{response.content}")
    assert response.status_code == 200


@pytest.mark.parametrize("model,as_dict", [(Food, {"name": "hot dog"})])
def test_models(model, as_dict):
    print(f"input dict:\n{pf(as_dict, depth=1, width=40)}")
    validated_data = model.parse_obj(as_dict)
    print(
        f"output dict:\n{pf(validated_data.dict(exclude_none=True),depth=1, width=40)}"
    )
    print(f"json:\n{pf(validated_data.json(exclude_none=True), depth=1, width=40)}")
