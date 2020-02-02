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
from eat_db import Food, Labels, db, __version__

TEST_LOGGER = logging.getLogger("tests")
TEST_LOGGER.setLevel(logging.DEBUG)


@pytest.fixture
def api_client():
    """Return a starlette TestClient for the `app`."""
    client = TestClient(eat_db.api.main.APP)
    return client


@pytest.fixture
def test_db():
    test_db = db.get_db()
    db.load_dummy_data(Food)
    initial_fridge_size = len(test_db["fridge"])
    yield test_db
    db.load_dummy_data(Food)
    assert len(test_db["fridge"]) == initial_fridge_size


def test_version():
    assert __version__ == "0.0.1"


def test_liveness(api_client):
    response = api_client.get("/status/liveness")
    TEST_LOGGER.info(f"liveness: {response}")
    assert response.status_code == 200


@pytest.mark.parametrize(
    "json_test_params,",
    [
        pytest.param(
            {"labels": {"leftovers"}},
            marks=pytest.mark.xfail(
                reason="Incoming request must be valid json. Python sets are not.",
                strict=True,
            ),
        ),
        {"labels": ["leftovers"]},
        {"labels": ["leftovers", "drink"]},
    ],
)
def test_add_food(request, api_client, test_db, json_test_params):
    fridge_inital = len(test_db["fridge"])
    json_body = {"name": request.node.name}
    json_body.update(json_test_params)
    print(f"\trequest json:\n{pf(json_body)}")

    response = api_client.put("/fridge", json=json_body)
    print(f"{response}\n{response.content}")
    assert response.status_code == 200
    assert len(test_db["fridge"]) == fridge_inital + 1


@pytest.mark.parametrize("model,as_dict", [(Food, {"name": "hot dog"})])
def test_models(model, as_dict):
    print(f"input dict:\n{pf(as_dict, depth=1, width=40)}")
    validated_data = model.parse_obj(as_dict)
    print(
        f"output dict:\n{pf(validated_data.dict(exclude_none=True),depth=1, width=40)}"
    )
    print(f"json:\n{pf(validated_data.json(exclude_none=True), depth=1, width=40)}")
