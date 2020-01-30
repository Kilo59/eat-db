"""
eat_db.api.app.py
~~~~~~~~~~~~~~~~~
fastapi app module.
"""
import enum
import logging

import fastapi
import pydantic

LOGGER = logging.getLogger("api")
LOGGER.setLevel(logging.DEBUG)

DEMO_NOSQL_DB = {
    "fridge": [
        "spam",
        "bacon",
        "eggs",
        "steak",
        "chinese",
        "pizza",
        "mexican",
        "cheese",
        "hotdogs",
        "hamburgers",
        "yogurt",
    ],
    "freezer": ["steak", "ice-cream", "peas", "pizza", "fries"],
}


def get_db(**kwargs):
    LOGGER.debug(f"get_db() kwargs:{kwargs}")
    return DEMO_NOSQL_DB


class BinTypes(str, enum.Enum):
    fridge = "fridge"
    freezer = "freezer"
    pantry = "pantry"
    extra_freezer = "extra-freezer"


class Bin(pydantic.BaseModel):
    name: str
    bin_type: BinTypes
    description: str = None

    @pydantic.validator("name")
    def unique_name(cls, v):
        if v in get_db():
            raise ValueError(f"name must be unique, {v} already exists.")


app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": {k: len(v) for (k, v) in get_db().items()}}


@app.get("/status/liveness")
async def liveness():
    """Check if the service is running"""
    return {"message": "ok"}


@app.get("/bin/{name}")
async def check_bin(name: BinTypes = BinTypes.fridge, skip: int = 0, limit: int = 10):
    """Check bins for contents."""
    bin_contents = get_db().get(name, [])[skip:limit]
    return bin_contents


@app.post("/bin/")
async def create_bin(bin_obj: Bin):
    LOGGER.debug(bin_obj)
    if not bin_obj.name:
        LOGGER.warning(f"name not provided: {bin_obj.name}")
        raise fastapi.HTTPException(400)
    get_db()[bin_obj.name] = []
    return bin_obj
