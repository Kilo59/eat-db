"""
eat_db.api.main.py
~~~~~~~~~~~~~~~~~
fastapi APP module.
"""
# stdlib
import logging
from pprint import pformat as pf
from typing import List, Union

import fastapi

# project
import eat_db.database
from eat_db.models import Item

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.DEBUG)


eat_db.database.load_dummy_data(Item)
DB = eat_db.database.get_db()
APP = fastapi.FastAPI()


@APP.get("/")
async def root():
    return {"message": {k: len(v) for (k, v) in DB.items()}}


@APP.get("/status/liveness")
async def liveness():
    """Check if the service is running"""
    return {"message": "ok"}


@APP.get(
    "/items",
    response_model=Union[List[str], List[Item]],
    response_model_exclude_none=True,
)
def all_items(label: str = None, skip: int = 0, limit: int = 10, details: bool = False):
    """Check the fridge for contents."""
    if not label:
        items = DB.get("items", [])[skip:limit]
    else:
        items = eat_db.db.get_by_label("items", label)[skip:limit]
    if details:
        return [item.dict(exclude={}) for item in items]
    return [item.name for item in items]


APP.add_event_handler("shutdown", eat_db.database.mongo.close_connection())
