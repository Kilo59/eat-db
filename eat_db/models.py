"""
eat_db.models.py
~~~~~~~~~~~~~~~~
"""
# stdlib
import datetime as dt
from typing import List, Set

from pydantic import BaseModel, Field, PositiveInt

DB = {}
EXPIRE_DEFAULT = dt.timedelta(weeks=4)


class Item(BaseModel):
    name: str
    qty: PositiveInt = Field(default=1, title="Quantity")
    description: str = None
    storage_date: dt.date = None
    expire_date: dt.date = None
    labels: Set[str] = Field(default_factory=set, max_items=15)
    notes: List[str] = Field(default_factory=list, max_items=100)


if __name__ == "__main__":
    pass
