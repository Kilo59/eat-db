"""
eat_db.api.main.py
~~~~~~~~~~~~~~~~~
fastapi APP module.
"""
# stdlib
import logging

import fastapi

# project
import eat_db.db
from eat_db.models import Tags

LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.DEBUG)

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
    bin_contents = DB.get("fridge", [])[skip:limit]
    return bin_contents


@APP.post("/fridge")
async def add_food(tag: Tags = None):
    LOGGER.debug(tag)
    return {"message": "added"}
