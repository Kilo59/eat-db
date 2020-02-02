"""
eat_db.api.db.py
~~~~~~~~~~~~~~~~
"""
# stdlib
import logging

LOGGER = logging.getLogger(name="db")

DEMO_NOSQL_DB = {
    "fridge": [],
    "freezer": [],
}


def get_db(**kwargs):
    LOGGER.debug(f"get_db() kwargs:{kwargs}")
    return DEMO_NOSQL_DB


def load_dummy_data(model):
    DEMO_NOSQL_DB["fridge"] = [
        model(name=name, tags={"fridge"})
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
