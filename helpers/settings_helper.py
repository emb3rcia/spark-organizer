#imports built in
import json
import os

#imports helpers
from helpers.theme_helper import default_themes, get_themes, add_theme

#define default settings
default_settings = {
    "theme": "dark",
    "minutes_reminders": 0,
    "minutes_events": 5
}

#define config file path
config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")

#values instead of "magical numbers"
CORRUPTED = 1
THEMES_CORRUPTED = 2

def get_settings():
    # if file exists, try to read it, if error, return CORRUPTED, if file doesn't exist, create one and write default themes
    if os.path.isfile(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings_data = json.load(f)
        except json.JSONDecodeError:
            return CORRUPTED
    else:
        settings_data = default_settings

    # if currently set theme is inaccessible e.g. due to name change, check if it is one of the default ones, if yes, add it to themes.json again, if not, set to dark, if dark is inaccessible, add it to themes.json, adding is handled without truncating the file
    all_themes = get_themes()
    # if themes are corrupted, return THEMES_CORRUPTED aka 2 so corruption_helper.py can react correctly
    if all_themes == CORRUPTED:
        return THEMES_CORRUPTED
    else:
        current_theme = settings_data.get("theme", "dark")
        if current_theme not in all_themes.keys():
            if current_theme in default_themes.keys():
                data = default_themes.get(current_theme)
                add_theme(data)
                settings_data["theme"] = current_theme
            else:
                if "dark" in all_themes.keys():
                    settings_data["theme"] = "dark"
                else:
                    data = default_themes.get('dark')
                    add_theme(data)
                    settings_data["theme"] = "dark"

    tmp_file = settings_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(settings_data, f, indent=4)
    os.replace(tmp_file, settings_file)

    return settings_data

#overwrite settings, used by corruption_helper.py
def overwrite_settings():
    tmp_file = settings_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(default_settings, f, indent=4)
    os.replace(tmp_file, settings_file)