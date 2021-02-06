"""
eat_db.database
~~~~~~~~~~~~~~~
"""
import logging

# project
from eat_db.database import mongo

__all__ = ["get_db", "load_dummy_data", "mongo"]

LOGGER = logging.getLogger(name="db")
LOGGER.setLevel(logging.DEBUG)

DEMO_NOSQL_DB = {
    "fridge": [],
    "freezer": [],
    "items": [],
}


def get_db(**kwargs):
    LOGGER.debug(f"get_db() kwargs:{kwargs}")
    return DEMO_NOSQL_DB


def load_dummy_data(model):
    DEMO_NOSQL_DB["items"] = [
        model(name=name, tags={"food"})
        for name in [
            "spam",
            "bacon",
            "eggs",
            "steak",
            "cheese",
            "hotdogs",
            "hamburgers",
            "yogurt",
        ]
    ]


def get_by_label(collection: str, label: str):
    collection_contents = DEMO_NOSQL_DB[collection]
    matching_items = [food for food in collection_contents if label in food.labels]
    LOGGER.debug(f"Matches: {len(matching_items)}")
    return matching_items
