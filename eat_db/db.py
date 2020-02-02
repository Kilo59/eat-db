"""
eat_db.api.db.py
~~~~~~~~~~~~~~~~
"""
# stdlib
import logging

LOGGER = logging.getLogger(name="db")

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
