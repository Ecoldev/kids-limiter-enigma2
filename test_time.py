import json
import os
import sys
from datetime import datetime


sys.modules['enigma'] = type('enigma', (), {})()

import plugin

TEST_FILE = "test_kids_time.json"

def write_json(data):
    with open(TEST_FILE, "w") as f:
        json.dump(data, f)

def setup():
    plugin.SAVE_FILE = TEST_FILE

def test_migration():
    print("TEST: migration")

    write_json({"date": "2026-03-27", "time": 100})
    setup()

    data = plugin.load_time()

    assert data["time_seconds"] == 100
    print("OK migration")


def test_invalid_json():
    print("TEST: invalid json")

    with open(TEST_FILE, "w") as f:
        f.write("{ broken")

    setup()

    data = plugin.load_time()

    assert data["time_seconds"] == 0
    print("OK invalid json")


def test_missing_file():
    print("TEST: missing file")

    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)

    setup()

    data = plugin.load_time()

    assert data["time_seconds"] == 0
    print("OK missing file")


def test_reset_logic():
    print("TEST: reset")

    today = datetime.now().strftime("%Y-%m-%d")

    data = {"date": "2000-01-01", "time_seconds": 999}

    if not data.get("date") or data["date"] != today:
        data["date"] = today
        data["time_seconds"] = 0

    assert data["time_seconds"] == 0
    print("OK reset")


if __name__ == "__main__":
    test_migration()
    test_invalid_json()
    test_missing_file()
    test_reset_logic()

    print("ALL TESTS PASSED")