#imports pyqt
from PyQt6.QtWidgets import QMessageBox

#imports helpers
from helpers.scheduled_helper import get_events, get_reminders, update_reminders, update_events
from helpers.settings_helper import get_settings, overwrite_settings
from helpers.stats_helper import get_stats, overwrite_stats
from helpers.theme_helper import get_themes, overwrite_themes


def check_for_corruption():
    #corruption pop-up
    def show_corrupt_popup(file_name):
        msg = QMessageBox()
        msg.setWindowTitle("Corrupted file")
        msg.setText(
            f"{file_name} is corrupted!\nOverwrite with defaults or quit?\nWARNING: It WILL delete saved themes or current stats, settings, event or reminders. (depending which file is corrupted)")
        write_defaults = msg.addButton("Write defaults", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        return msg.clickedButton() == write_defaults

    #error overwriting pop-up
    def show_error_overwriting(file_name):
        msg = QMessageBox()
        msg.setWindowTitle("Error overwriting corrupted file")
        msg.setText(f"{file_name} is still corrupted!\nReport this on GitHub to program's creator")
        msg.addButton("Okay", QMessageBox.ButtonRole.AcceptRole)
        msg.exec()

    #check for corruption
    settings_data = get_settings()
    theme_data = get_themes()
    events = get_events()
    reminders = get_reminders()
    stats = get_stats()

    #values instead of "magic numbers"
    CORRUPTED_VALUE = 1
    THEMES_CORRUPTED_VALUE = 2

    #corruption logic
    themes_overwritten = False
    corrupted = False
    
    if theme_data == CORRUPTED_VALUE:
        if show_corrupt_popup("config/themes.json"):
            overwrite_themes()
            themes_overwritten = True
            theme_data = get_themes()
            if theme_data == CORRUPTED_VALUE:
                show_error_overwriting("config/themes.json")
                corrupted = True
        else:
            corrupted = True
    if settings_data == CORRUPTED_VALUE:
        if show_corrupt_popup("config/settings.json"):
            overwrite_settings()
            settings_data = get_settings()
            if settings_data == CORRUPTED_VALUE:
                show_error_overwriting("config/settings.json")
                corrupted = True
        else:
            corrupted = True
    elif settings_data == THEMES_CORRUPTED_VALUE:
        if show_corrupt_popup("config/themes.json"):
            overwrite_settings()
            if not themes_overwritten:
                overwrite_themes()
            settings_data = get_settings()
            if settings_data == CORRUPTED_VALUE:
                if show_corrupt_popup("config/settings.json"):
                    overwrite_settings()
                    settings_data = get_settings()
                    if settings_data == CORRUPTED_VALUE:
                        show_error_overwriting("config/settings.json")
                        corrupted = True
                else:
                    corrupted = True
            if settings_data == THEMES_CORRUPTED_VALUE:
                show_error_overwriting("config/themes.json")
                corrupted = True
        else:
            corrupted = True
    if events == CORRUPTED_VALUE:
        if show_corrupt_popup("config/events.json"):
            update_events([])
            events = get_events()
            if events == CORRUPTED_VALUE:
                show_error_overwriting("config/events.json")
                corrupted = True
        else:
            corrupted = True
    if reminders == CORRUPTED_VALUE:
        if show_corrupt_popup("config/reminders.json"):
            update_reminders([])
            reminders = get_reminders()
            print(reminders)
            if reminders == CORRUPTED_VALUE:
                show_error_overwriting("config/reminders.json")
                corrupted = True
        else:
            corrupted = True
    if stats == CORRUPTED_VALUE:
        if show_corrupt_popup("config/stats.json"):
            overwrite_stats()
            stats = get_stats()
            print(stats)
            if stats == CORRUPTED_VALUE:
                show_error_overwriting("config/stats.json")
                corrupted = True
        else:
            corrupted = True

    return corrupted