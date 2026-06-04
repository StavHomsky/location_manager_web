import json
import os

FILE_PATH = "data/locations.json"


def load_locations():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_locations(locations):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as f:
        json.dump(locations, f, indent=4)


def get_next_id(locations):
    if not locations:
        return 1
    return max(l["id"] for l in locations) + 1