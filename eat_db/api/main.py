"""
eat_db.api.main.py
~~~~~~~~~~~~~~~~~
fastapi APP module.
"""
# stdlib
import logging
from pprint import pformat as pf

import fastapi

# project
import eat_db.db
from eat_db.models import Food, Tags

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("api")


eat_db.db.load_dummy_data(Food)
DB = eat_db.db.get_db()
APP = fastapi.FastAPI()


@APP.get("/")
async def root():
    return {"message": {k: len(v) for (k, v) in DB.items()}}


@APP.get("/status/liveness")
async def liveness():
    """Check if the service is running"""
    return {"message": "ok"}


@APP.get("/fridge")
async def check_fridge(skip: int = 0, limit: int = 10):
    """Check the fridge for contents."""
    fridge_contents = DB.get("fridge", [])[skip:limit]
    return [food.name for food in fridge_contents]


@APP.put("/fridge")
async def add_food(
    food: Food, tag: Tags = Tags.fridge,
):
    """
    Put food in the fridge.
    TODO: finalize how tags are going to be used.
    """
    LOGGER.debug(f"adding tag: {tag}")
    food.tags.add(tag.value)
    LOGGER.debug(f"food:\n{pf(food.dict(exclude_none=True))}")
    DB["fridge"].append(food)
    return {
        "message": f"{food.name} added",
        "expires": food.expire_date,
        "tags": food.tags,
    }
