"""
eat_db.api.app.py
~~~~~~~~~~~~~~~~~
fastapi app module.
"""
import enum

import fastapi

app = fastapi.FastAPI()


class Bins(str, enum.Enum):
    fridge = "fridge"
    freezer = "freezer"
    extra_freezer = "extra-freezer"


db = {
    Bins.fridge: ["spam", "bacon", "eggs", "steak"],
    Bins.freezer: ["steak", "ice-cream", "peas"],
}


@app.get("/")
async def root():
    return {"message": {k: len(v) for (k, v) in db.items()}}


@app.get("/bin/{name}")
async def check_bin(name: Bins = Bins.fridge, skip: int = 0, limit: int = 10):
    """Check bins for contents."""
    bin_contents = db.get(name, [])[skip:limit]
    return bin_contents
