"""
eat_db.models.py
~~~~~~~~~~~~~~~~
"""
import datetime as dt
# stdlib
import enum
from typing import List

import pydantic

DB = {}
EXPIRE_DEFAULT = dt.timedelta(weeks=8)


class Tags(str, enum.Enum):
    leftovers = "leftovers"


class Food(pydantic.BaseModel):
    name: str
    storage_date: dt.datetime = dt.datetime.now()
    # TODO: use Tags to determine expire date if none provided.
    expire_date: dt.datetime = storage_date + EXPIRE_DEFAULT
    tags: List[Tags] = []


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
        if v in DB:
            raise ValueError(f"name must be unique, {v} already exists.")
