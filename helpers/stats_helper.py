#imports built-in
import json
import os

#define default stats
default_stats = {
    "work_started_count":0,
    "work_completed_count":0,
    "break_started_count":0,
    "break_completed_count":0,
    "longer_break_started_count":0,
    "longer_break_completed_count":0,
    "cycles_started_count":0,
    "cycles_completed_count":0
}

#define config file path
config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
stats_file = os.path.join(config_path, "stats.json")

#values instead of "magic numbers"
CORRUPTED = 1

def get_stats():
    # if file exists, try to read it, if error, return CORRUPTED, if file doesn't exist, create one and write default themes
    if os.path.isfile(stats_file):
        try:
            with open(stats_file, "r") as f:
                stats_data = json.load(f)
        except json.JSONDecodeError:
            return CORRUPTED
    else:
        stats_data = default_stats
        tmp_file = stats_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(stats_data, f, indent=4)
        os.replace(tmp_file, stats_file)

    return stats_data

def add_one_to_stat(stat):
    stats_data = get_stats()
    stats_data[stat] += 1
    tmp_file = stats_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(stats_data, f, indent=4)
    os.replace(tmp_file, stats_file)

#overwrite stats, used by corruption_helper.py
def overwrite_stats():
    stats_data = default_stats
    tmp_file = stats_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(stats_data, f, indent=4)
    os.replace(tmp_file, stats_file)