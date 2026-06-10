"""JSON file persistence for LOCSAM data."""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data_store")
DATA_FILE = os.path.join(DATA_DIR, "locsam_data.json")


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return None
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def save_data(data):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
