import json
import os
import sys
from PyQt6.QtWidgets import QMessageBox, QApplication
from helpers.theme_helper import listThemes, default_themes, initializeThemes
from helpers.scheduled_helper import EVENTS_FILE, REMINDERS_FILE

default_settings = {
    "theme": "dark",
    "minutes": 5
}

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")

def show_corrupt_popup(file_name):
    msg = QMessageBox()
    msg.setWindowTitle("Corrupted themes.json detected")
    msg.setText(f"File {file_name} is corrupted!\nYou can overwrite it with default values and exit,\nor quit without changes to it, what would you want?")
    msg.setIcon(QMessageBox.Icon.Critical)
    write_defaults = msg.addButton("Write defaults and exit", QMessageBox.ButtonRole.AcceptRole)
    quit_button = msg.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
    msg.exec()
    if msg.clickedButton() == write_defaults:
        return True
    return False


def get_settings():
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings_data = json.load(f)
        except json.JSONDecodeError:
            return 1
    else:
        settings_data = default_settings.copy()

    all_themes = listThemes()
    current_theme = settings_data.get("theme", "dark")
    if current_theme not in all_themes:
        if current_theme in default_themes:
            settings_data["theme"] = current_theme
        else:
            settings_data["theme"] = "dark"
            initializeThemes()

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