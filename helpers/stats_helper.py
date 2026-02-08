import json
import os

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

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
stats_file = os.path.join(config_path, "stats.json")

def get_stats():
    if os.path.isfile(stats_file):
        try:
            with open(stats_file, "r") as f:
                stats_data = json.load(f)
        except json.JSONDecodeError:
            return 1
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

def overwrite_stats():
    stats_data = default_stats
    tmp_file = stats_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(stats_data, f, indent=4)
    os.replace(tmp_file, stats_file)