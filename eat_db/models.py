"""
eat_db.models.py
~~~~~~~~~~~~~~~~
"""
# stdlib
import datetime as dt
import enum
from typing import List, Set

import pydantic

DB = {}
EXPIRE_DEFAULT = dt.timedelta(weeks=4)


class Labels(str, enum.Enum):
    leftovers = "leftovers"
    food = "food"
    drink = "drink"


class Food(pydantic.BaseModel):
    name: str
    storage_date: dt.date = dt.date.today()
    # TODO: use Labels to determine expire date if none provided.
    expire_date: dt.date = storage_date + EXPIRE_DEFAULT
    labels: Set[Labels] = set()

    class Config:
        use_enum_values = True
        anystr_strip_whitespace = True


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
