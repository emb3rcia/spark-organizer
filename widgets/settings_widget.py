#reused from my spark-builder project

from PyQt6.QtWidgets import QComboBox, QWidget, QVBoxLayout, QFormLayout
from styled_functions.styled_functions import ComboBox, Widget, Label
from helpers.theme_helper import listThemes
import os
import json

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
settings_file = os.path.join(config_path, "settings.json")


class settings_widget(QWidget):
    def __init__(self, theme_data, settings_data, on_theme_change):
        super().__init__()
        self.on_theme_change = on_theme_change  # store the callback

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        interact_widget = Widget(theme_data['main_backgrounds'])
        interact_layout = QFormLayout()
        interact_widget.setLayout(interact_layout)
        main_layout.addWidget(interact_widget)

        themes_box = ComboBox(theme_data['combo-box'], theme_data['text']['text_disabled'])
        themes_label = Label("Theme:", theme_data['text'], 1)
        interact_layout.addRow(themes_label, themes_box)

        themes = listThemes()
        themes_box.addItems(themes)
        index = themes.index(settings_data['theme'])
        themes_box.setCurrentIndex(index)

        themes_box.currentTextChanged.connect(lambda text: self.change_theme(text, settings_data))


    def change_theme(self, current_index_text, settings_data):
        settings_data['theme'] = current_index_text
        tmp_file = settings_file + ".tmp"
        with open(tmp_file, "w") as f:
            json.dump(settings_data, f, indent=4)
        os.replace(tmp_file, settings_file)

        self.on_theme_change(current_index_text)