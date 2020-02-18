"""
eat_db.api.main.py
~~~~~~~~~~~~~~~~~
fastapi APP module.
"""
# stdlib
import logging
from pprint import pformat as pf
from typing import List

import fastapi

# project
import eat_db.database
from eat_db.models import Food, Labels

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.DEBUG)


eat_db.database.load_dummy_data(Food)
DB = eat_db.database.get_db()
APP = fastapi.FastAPI()


@APP.get("/")
async def root():
    return {"message": {k: len(v) for (k, v) in DB.items()}}


@APP.get("/status/liveness")
async def liveness():
    """Check if the service is running"""
    return {"message": "ok"}


@APP.get("/fridge")
async def check_fridge(
    label: Labels = None, skip: int = 0, limit: int = 10, details: bool = False
):
    """Check the fridge for contents."""
    if not label:
        fridge_contents = DB.get("fridge", [])[skip:limit]
    else:
        fridge_contents = eat_db.db.get_by_label("fridge", label)[skip:limit]
    if details:
        return [item.dict(exclude={}) for item in fridge_contents]
    return [item.name for item in fridge_contents]


@APP.put("/fridge")
async def add_food(
    food: Food, label: Labels = Labels.food,
):
    """
    Put food in the fridge.
    TODO: finalize how labels are going to be used.
    """
    labels = {Labels.food.value, label.value}
    LOGGER.debug(f"adding labels: {labels}")
    food.labels.update(labels)
    LOGGER.debug(f"food:\n{pf(food.dict(exclude_none=True))}")

    LOGGER.debug("updating DB")
    DB["fridge"].append(food)
    return {
        "message": f"{food.name} added",
        "expires": food.expire_date,
        "labels": food.labels,
    }


APP.add_event_handler("shutdown", eat_db.database.mongo.close_connection())
