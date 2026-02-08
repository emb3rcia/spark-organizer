#reused and changed from my spark-builder project

from PyQt6.QtWidgets import QComboBox, QWidget, QVBoxLayout, QFormLayout
from PyQt6.QtGui import QIntValidator
from styled_functions.styled_functions import ComboBox, Widget, Label, Button, LineEdit
from helpers.theme_helper import list_themes
import os
import json

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")


class settings_widget(QWidget):
    def __init__(self, theme_data, settings_data, on_settings_save):
        super().__init__()
        self.theme_data = theme_data
        self.on_settings_save = on_settings_save
        self.settings_data = settings_data

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        interact_widget = Widget(self.theme_data['main_backgrounds'])
        interact_layout = QFormLayout()
        interact_widget.setLayout(interact_layout)
        main_layout.addWidget(interact_widget)

        self.themes_box = ComboBox(self.theme_data['combo-box'], self.theme_data['text']['text_disabled'])
        themes_label = Label("Theme:", self.theme_data['text'], 1)
        interact_layout.addRow(themes_label, self.themes_box)

        themes = list_themes()
        self.themes_box.addItems(themes)
        index = themes.index(settings_data['theme'])
        self.themes_box.setCurrentIndex(index)

        self.themes_box.currentTextChanged.connect(self.change_settings)

        validator = QIntValidator(0, 9999)
        self.when_to_notify = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.when_to_notify.setPlaceholderText("For notification on set time write 0")
        self.when_to_notify.setValidator(validator)
        when_to_notify_label = Label("How many minutes before should you be notified:", theme_data['text'], 1)
        interact_layout.addRow(when_to_notify_label, self.when_to_notify)
        save_settings_button = Button("Save settings", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        save_settings_button.clicked.connect(self.change_settings)
        interact_layout.addRow("", save_settings_button)


    def change_settings(self):
        self.settings_data['theme'] = self.themes_box.currentText()
        text = self.when_to_notify.text().strip()
        if text.isdigit():
            self.settings_data['minutes'] = int(text)
        tmp_file = settings_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(self.settings_data, f, indent=4)
        os.replace(tmp_file, settings_file)

        self.on_settings_save()
    
