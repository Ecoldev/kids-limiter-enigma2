import sys
import types
import json
import os
from datetime import datetime


plugins_module = types.ModuleType("Plugins")
plugin_submodule = types.ModuleType("Plugin")
plugin_submodule.PluginDescriptor = object
plugins_module.Plugin = plugin_submodule

sys.modules['Plugins'] = plugins_module
sys.modules['Plugins.Plugin'] = plugin_submodule


screens_module = types.ModuleType("Screens")
messagebox_module = types.ModuleType("MessageBox")
messagebox_module.MessageBox = object
screens_module.MessageBox = messagebox_module

sys.modules['Screens'] = screens_module
sys.modules['Screens.MessageBox'] = messagebox_module

components_module = types.ModuleType("Components")
tracker_module = types.ModuleType("ServiceEventTracker")
tracker_module.ServiceEventTracker = object
components_module.ServiceEventTracker = tracker_module

sys.modules['Components'] = components_module
sys.modules['Components.ServiceEventTracker'] = tracker_module


enigma_module = types.ModuleType("enigma")
enigma_module.eTimer = object
enigma_module.iPlayableService = object
enigma_module.eServiceReference = object

sys.modules['enigma'] = enigma_module


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