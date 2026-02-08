import os
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox

from helpers.corruption_helper import check_for_corruption
from helpers.event_timer import event_timer
from helpers.reminder_timer import reminder_timer
from helpers.settings_helper import get_settings
from helpers.theme_helper import get_themes
from helpers.tray_helper import tray_helper
from styled_functions.styled_functions import Button, Label, LineEdit, MainWindow, TableWidget, Widget, StackedWidget, ComboBox, DateTimeEdit
from widgets.events_widget import events_widget
from widgets.reminder_widget import reminder_widget
from widgets.settings_widget import settings_widget
from widgets.stats_widget import stats_widget
from widgets.timer_widget import timer_widget

app = QApplication(sys.argv)

#check for corruption
corrupted = check_for_corruption()
if corrupted:
    app.exit(0)
    sys.exit(0)

theme_data = get_themes()
settings_data = get_settings()

current_theme_name = settings_data["theme"]
theme = theme_data[current_theme_name]

window = MainWindow(theme['main_backgrounds'])
central = Widget(theme['main_backgrounds'])
window.setCentralWidget(central)

def setTooltipStyle():
    app.instance().setStyleSheet(f"""
        QToolTip {{
            background-color: {theme['main_backgrounds']['tooltip_background']};
            color: {theme['text']['text_tooltip']};
            border: 1px solid {theme['accent']['accent_primary']};
        }}
    """)

setTooltipStyle()

tray = tray_helper(app, window)

sound_file_path = os.path.join(os.path.dirname(__file__), "assets", "sounds", "error.wav")

event_timer_object = event_timer(theme, window, settings_data, tray, 5000)
event_timer_object.start()
reminder_timer_object = reminder_timer(theme, window, settings_data, tray, 5000)
reminder_timer_object.start()

def refresh_settings():
    global settings_data, theme
    new_settings_data = get_settings()
    
    if settings_data['theme'] != new_settings_data['theme']:
        theme = theme_data[new_settings_data['theme']]

        setTooltipStyle()

        window.update_theme(theme['main_backgrounds'])
        event_timer_object.update_theme(theme)
        reminder_timer_object.update_theme(theme)

        for widget in window.findChildren(QWidget):
            if hasattr(widget, "update_theme"):
                if isinstance(widget, Button):
                    widget.update_theme(theme['button'], theme['text']['text_disabled'])
                elif isinstance(widget, Label):
                    widget.update_theme(theme['text'])
                elif isinstance(widget, LineEdit):
                    widget.update_theme(theme['input'], theme['highlight'], theme['text']['text_disabled'])
                elif isinstance(widget, MainWindow):
                    widget.update_theme(theme['main_backgrounds'])
                elif isinstance(widget, TableWidget):
                    widget.update_theme(theme['table'], theme['extra'], theme['text']['text_disabled'])
                elif isinstance(widget, Widget):
                    widget.update_theme(theme['main_backgrounds'])
                elif isinstance(widget, StackedWidget):
                    widget.update_theme(theme['main_backgrounds'])
                elif isinstance(widget, ComboBox):
                    widget.update_theme(theme['combo-box'], theme['text']['text_disabled'])
                elif isinstance(widget, DateTimeEdit):
                    widget.update_theme(theme)
    event_timer_object.update_when_to_notify(new_settings_data)
    reminder_timer_object.update_when_to_notify(new_settings_data)
    settings_data = new_settings_data
    

main_layout = QHBoxLayout()
central.setLayout(main_layout)

tool_selector = Widget(theme['main_backgrounds'])
tool_selector_layout = QVBoxLayout()
tool_selector.setLayout(tool_selector_layout)
pomodoro_timer_button = Button("Pomodoro Timer", theme['button'], theme['text']['text_disabled'])
events_button = Button("Events", theme['button'], theme['text']['text_disabled'])
reminders_button = Button("Reminders", theme['button'], theme['text']['text_disabled'])
settings_button = Button("Settings", theme['button'], theme['text']['text_disabled'])
stats_button = Button("Stats", theme['button'], theme['text']['text_disabled'])
quit_button = Button("Quit app", theme['button'], theme['text']['text_disabled'])

tool_widget = StackedWidget(theme['main_backgrounds'])
tool_widget.addWidget(timer_widget(theme, tray, stats_widget))
tool_widget.addWidget(events_widget(theme, tray))
tool_widget.addWidget(reminder_widget(theme, tray))
tool_widget.addWidget(settings_widget(theme, settings_data, refresh_settings, tray))
tool_widget.addWidget(stats_widget(theme))

sound_effect = QSoundEffect()
sound_effect.setSource(QUrl.fromLocalFile(sound_file_path))
sound_effect.setVolume(0.5)

def showQuitPopup():
    msg = QMessageBox(window)
    msg.setWindowTitle("Quit confirmation")
    msg.setText("This will quit the app completely, if you want to minimize it to tray use X button. You sure you want to quit?")
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
    confirm_button = msg.button(QMessageBox.StandardButton.Yes)
    cancel_button = msg.button(QMessageBox.StandardButton.Cancel)
    msg.setIcon(QMessageBox.Icon.Information)

    msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {theme['main_backgrounds']['popup_background']};
            color: {theme['text']['text_primary']}
            border: 1px solid {theme['accent']['info']}
        }}
    """
    )
    #styled buttons raise error >:(
    confirm_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {theme['button']['button_background']};
            color: {theme['button']['button_text']};
        }}
        QPushButton:hover {{
            background-color: {theme['button']['button_hover']};
        }}
        QPushButton:pressed {{
            background-color: {theme['button']['button_pressed']};
        }}
        QPushButton:disabled {{
            background-color: {theme['button']['button_disabled']};
            color: {theme['text']['text_disabled']};
        }}
    """
    )
    cancel_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {theme['button']['button_background']};
            color: {theme['button']['button_text']};
        }}
        QPushButton:hover {{
            background-color: {theme['button']['button_hover']};
        }}
        QPushButton:pressed {{
            background-color: {theme['button']['button_pressed']};
        }}
        QPushButton:disabled {{
            background-color: {theme['button']['button_disabled']};
            color: {theme['text']['text_disabled']};
        }}
    """
    )

    msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
    msg.setWindowModality(Qt.WindowModality.ApplicationModal)

    sound_effect.play()
    reply = msg.exec()
    if reply == QMessageBox.StandardButton.Yes:
        app.exit()
        sys.exit(1)

main_layout.addWidget(tool_selector)
main_layout.addWidget(tool_widget)
tool_selector_layout.addWidget(pomodoro_timer_button)
tool_selector_layout.addWidget(events_button)
tool_selector_layout.addWidget(reminders_button)
tool_selector_layout.addWidget(settings_button)
tool_selector_layout.addWidget(stats_button)
tool_selector_layout.addWidget(quit_button)
pomodoro_timer_button.clicked.connect(lambda: tool_widget.setCurrentIndex(0))
events_button.clicked.connect(lambda: tool_widget.setCurrentIndex(1))
reminders_button.clicked.connect(lambda: tool_widget.setCurrentIndex(2))
settings_button.clicked.connect(lambda: tool_widget.setCurrentIndex(3))
stats_button.clicked.connect(lambda: tool_widget.setCurrentIndex(4))
quit_button.clicked.connect(showQuitPopup)





window.show()
tray.notify("spark-organizer", "Running in background")

app.exec()