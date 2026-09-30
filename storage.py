
#storage.py - Module for data persistence and file handling.


import json
import os

DATA_FILE = "theatre_data.json"

DEFAULT_MOVIES = {
    "1": {
        "title": "MARVEL: IRON MAN",
        "genre": "Sci-Fi/Action",
        "duration": "2h 6m",
        "price": 300.00,
        "rows": 6,
        "cols": 7,
        "booked_seats": ["A1", "A2", "C4"]
    },
    "2": {
        "title": "FORD V FERRARI",
        "genre": "Sport/Action",
        "duration": "2h 32m",
        "price": 290.00,
        "rows": 8,
        "cols": 5,
        "booked_seats": ["E1", "E2", "E3"]
    },
    "3": {
        "title": "MISSION IMPOSSIBLE",
        "genre": "Action/Thriller",
        "duration": "1h 50m",
        "price": 250.00,
        "rows": 4,
        "cols": 7,
        "booked_seats": ["C1", "C4", "C7"]
    },
    "4": {
        "title": "THE PURSUIT OF HAPPYNESS",
        "genre": "Melodrama/Drama",
        "duration": "1h 57m",
        "price": 225.00,
        "rows": 7,
        "cols": 6,
        "booked_seats": ["B3", "D5"]
    }
}


def load_data():
    """Load movie and booking records from the JSON file."""
    if not os.path.exists(DATA_FILE):
        data = {
            "movies": DEFAULT_MOVIES,
            "bookings": {}
        }
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[!] Error loading data file. Resetting to defaults.")
        data = {"movies": DEFAULT_MOVIES, "bookings": {}}
        save_data(data)
        return data


def save_data(data):
    """Save the updated movie and booking data to the JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)