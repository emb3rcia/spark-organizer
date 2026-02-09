#reused and changed from my spark-builder project

#imports built-in
import json
import os

#imports pyqt
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIntValidator, QColor
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QMessageBox

#imports helper
from helpers.theme_helper import get_themes

#imports styled_functions
from styled_functions.styled_functions import ComboBox, Widget, Label, Button, LineEdit

#define file paths
config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")

sound_effect_file = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "error.wav")


class settings_widget(QWidget):
    def __init__(self, theme_data, settings_data, on_settings_save, tray, window):
        super().__init__()
        #define pyqt6 required values
        self.theme_data = theme_data
        self.on_settings_save = on_settings_save
        self.settings_data = settings_data
        self.tray = tray
        self.window = window
        self.msg = QMessageBox(self.window)
        self.setPopupStyleEventsSettings(self.theme_data)

        #define sound effect
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_effect_file))
        self.sound_effect.setVolume(0.5)

        #define main layouts and widgets
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        interact_widget = Widget(self.theme_data['main_backgrounds'])
        interact_layout = QFormLayout()
        interact_widget.setLayout(interact_layout)
        main_layout.addWidget(interact_widget)

        #define themes combobox
        self.themes_box = ComboBox(self.theme_data['combo-box'], self.theme_data['text']['text_disabled'])
        themes_label = Label("Theme:", self.theme_data['text'], 1)

        #add items to themes combobox
        themes = get_themes()
        self.themes_box.addItems(list(themes.keys()))
        index = list(themes.keys()).index(settings_data.get('theme', 'dark'))
        self.themes_box.setCurrentIndex(index)

        #define validator
        validator = QIntValidator(0, 9999)

        #define when to notify events row
        self.when_to_notify_events = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.when_to_notify_events.setPlaceholderText("For notification on set time write 0")
        self.when_to_notify_events.setValidator(validator)
        self.when_to_notify_events.setText(str(settings_data['minutes_events'] if settings_data['minutes_events'] else 5))
        when_to_notify_events_label = Label("How many minutes before events should you be notified:", theme_data['text'], 1)

        # define when to notify reminders row
        self.when_to_notify_reminders = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.when_to_notify_reminders.setPlaceholderText("For notification on set time write 0")
        self.when_to_notify_reminders.setValidator(validator)
        self.when_to_notify_reminders.setText(str(settings_data['minutes_reminders'] if settings_data['minutes_reminders'] else 3))
        when_to_notify_reminders_label = Label("How many minutes before reminders should you be notified:", theme_data['text'], 1)

        #define save settings button
        save_settings_button = Button("Save settings", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        save_settings_button.clicked.connect(self.change_settings)

        #add rows
        interact_layout.addRow(themes_label, self.themes_box)
        interact_layout.addRow(when_to_notify_events_label, self.when_to_notify_events)
        interact_layout.addRow(when_to_notify_reminders_label, self.when_to_notify_reminders)
        interact_layout.addRow("", save_settings_button)

    def setPopupStyleEventsSettings(self, theme_data):
        self.theme_data = theme_data
        self.msg.setIcon(QMessageBox.Icon.Information)

        palette = self.msg.palette()
        palette.setColor(self.msg.backgroundRole(), QColor(self.theme_data['main_backgrounds']['popup_background']))
        palette.setColor(self.msg.foregroundRole(), QColor(self.theme_data['text']['text_primary']))
        self.msg.setPalette(palette)

        self.msg.setStyleSheet(f"""
                    QMessageBox {{
                        border: 1px solid {self.theme_data['accent']['info']};
                    }}
                    QMessageBox QPushButton {{
                        background-color: {self.theme_data['button']['button_background']};
                        color: {self.theme_data['button']['button_text']};
                        border: 1px solid {self.theme_data['button']['button_border']};
                        border-radius: 6px;
                    }}
                    QMessageBox QPushButton:hover {{
                        background-color: {self.theme_data['button']['button_hover']};
                    }}
                    QMessageBox QPushButton:pressed {{
                        background-color: {self.theme_data['button']['button_pressed']};
                    }}
                    QMessageBox QPushButton:disabled {{
                        background-color: {self.theme_data['button']['button_disabled']};
                        color: {self.theme_data['text']['text_disabled']};
                    }}
                """)

        self.msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.msg.setWindowModality(Qt.WindowModality.ApplicationModal)

    def showPopup(self, title, text):
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        self.sound_effect.play()
        self.msg.exec()

    def change_settings(self):
        if not self.when_to_notify_reminders.text().isdigit() or int(self.when_to_notify_reminders.text()) < 0:
            self.showPopup("Invalid settings", "You must select at least one minute before reminders\nor select 0 for notification on set date")
            return
        elif not self.when_to_notify_events.text().isdigit() or int(self.when_to_notify_events.text()) < 0:
            self.showPopup("Invalid settings","You must select at least one minute before events\nor deadlines or select 0 for notification on set date")
            return
        else:
            self.settings_data['theme'] = self.themes_box.currentText()
            text = self.when_to_notify_events.text().strip()
            if text.isdigit():
                self.settings_data['minutes_events'] = int(text)
            text = self.when_to_notify_reminders.text().strip()
            if text.isdigit():
                self.settings_data['minutes_reminders'] = int(text)
            tmp_file = settings_file + ".tmp"
            with open(tmp_file, "w") as f:
                json.dump(self.settings_data, f, indent=4)
            os.replace(tmp_file, settings_file)

            self.on_settings_save()
            self.tray.notify("Settings", "Updated settings!")
    
