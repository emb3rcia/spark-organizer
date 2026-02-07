#reused from my spark-builder project

import json
import os
from helpers.theme_helper import listThemes, default_themes

default_settings = {
    "theme": "dark"
}

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)  # create folder if it doesn't exist
settings_file = os.path.join(config_path, "settings.json")


def initializeSettings():
    if os.path.exists(settings_file):
        with open(settings_file, "r") as f:
            try:
                settings_data = json.load(f)
            except json.JSONDecodeError:
                settings_data = default_settings.copy()
    else:
        settings_data = default_settings.copy()

    from helpers.theme_helper import listThemes

    all_themes = listThemes()
    current_theme = settings_data.get("theme", "dark")

    if current_theme not in all_themes:
        if current_theme in default_themes:
            settings_data["theme"] = current_theme
        else:
            if "dark" in all_themes:
                settings_data["theme"] = "dark"
            else:
                settings_data["theme"] = "dark"

    tmp_file = settings_file + ".tmp"
    with open(tmp_file, "w") as f:
        json.dump(settings_data, f, indent=4)
    os.replace(tmp_file, settings_file)

    return settings_data