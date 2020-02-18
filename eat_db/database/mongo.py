"""
eat_db.database.mongo.py
~~~~~~~~~~~~~~~~~~~~~~~~
"""
import logging
import pymongo.mongo_client

LOGGER = logging.getLogger("mongo")
MONGO_GLOBALS = {}


def get_mongo_client(
    host: str = None, port: int = None, check: bool = False, **mongo_conn_kwargs
):
    client = MONGO_GLOBALS.get("client")
    if not client:
        client = pymongo.mongo_client.MongoClient(
            host=host, port=port, **mongo_conn_kwargs
        )
        LOGGER.debug("loading mongo `client` global")
        MONGO_GLOBALS["client"] = client
    if check:
        client.admin.command("ismaster")
    return client


def close_connection():
    client = MONGO_GLOBALS.get("client")
    if not client:
        LOGGER.debug("no active `client` global, no mongo connection to close")
        return False
    client.close()
    return True
