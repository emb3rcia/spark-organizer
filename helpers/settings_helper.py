import json
import os
from helpers.theme_helper import list_themes, default_themes

default_settings = {
    "theme": "dark",
    "minutes_reminders": 0,
    "minutes_events": 5
}

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")

def get_settings():
    if os.path.isfile(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings_data = json.load(f)
        except json.JSONDecodeError:
            return 1
    else:
        settings_data = default_settings

    all_themes = list_themes()
    if all_themes == 1:
        return 2
    else:
        current_theme = settings_data.get("theme", "dark")
        if current_theme not in all_themes:
            if current_theme in default_themes:
                settings_data["theme"] = current_theme
            else:
                settings_data["theme"] = "dark"

    tmp_file = settings_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(settings_data, f, indent=4)
    os.replace(tmp_file, settings_file)

    return settings_data

def overwrite_settings():
    tmp_file = settings_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(default_settings, f, indent=4)
    os.replace(tmp_file, settings_file)