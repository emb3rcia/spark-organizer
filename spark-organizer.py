from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from styled_functions.styled_functions import Button, Label, LineEdit, MainWindow, TableWidget, Widget, StackedWidget, ComboBox, DateTimeEdit
import sys
from helpers.theme_helper import get_themes, overwrite_themes
from helpers.scheduled_helper import get_events, get_reminders, update_events, update_reminders
from helpers.settings_helper import get_settings, overwrite_settings
from widgets.settings_widget import settings_widget
from widgets.timer_widget import timer_widget
from widgets.events_widget import events_widget
from helpers.tray_helper import tray_helper
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt, QUrl
from helpers.event_timer import event_timer

app = QApplication(sys.argv)

def show_corrupt_popup(file_name):
    msg = QMessageBox()
    msg.setWindowTitle("Corrupted file")
    msg.setText(f"{file_name} is corrupted!\nOverwrite with defaults or quit?")
    write_defaults = msg.addButton("Write defaults", QMessageBox.ButtonRole.AcceptRole)
    quit_btn = msg.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
    msg.exec()
    return msg.clickedButton() == write_defaults

def show_error_overwriting(file_name):
    msg = QMessageBox()
    msg.setWindowTitle("Error overwriting corrupted file")
    msg.setText(f"{file_name} is still corrupted!\nReport this on GitHub to program's creator")
    okay = msg.addButton("Okay", QMessageBox.ButtonRole.AcceptRole)
    msg.exec()
    return msg.clickedButton() == okay

#check for corruption
settings_data = get_settings()
theme_data = get_themes()
events = get_events()
reminders = get_reminders()

if theme_data == 1:
    if show_corrupt_popup("config/themes.json"):
        overwrite_themes()
        theme_data = get_themes()
        if theme_data == 1:
            if show_error_overwriting("config/themes.json"):
                app.exit()
            else:
                app.exit()
    else:
        app.exit()
if settings_data == 1:
    if show_corrupt_popup("config/settings.json"):
        overwrite_settings()
        settings_data = get_settings()
        if settings_data == 1:
            if show_error_overwriting("config/settings.json"):
                app.exit()
            else:
                app.exit()
    else:
        app.exit()
if events == 1:
    if show_corrupt_popup("config/events.json"):
        update_events([])
        events = get_events()
        if events == 1:
            if show_error_overwriting("config/events.json"):
                app.exit()
            else:
                app.exit()
    else:
        app.exit()
if reminders == 1:
    if show_corrupt_popup("config/reminders.json"):
        update_reminders([])
        reminders = get_reminders()
        if reminders == 1:
            if show_error_overwriting("config/reminders.json"):
                app.exit()
            else:
                app.exit()
    else:
        app.exit()


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

eventTimer = event_timer(theme, window, settings_data, 5000)
eventTimer.start()

def refresh_settings():
    global settings_data, theme
    new_settings_data = get_settings()
    
    if settings_data['theme'] != new_settings_data['theme']:
        theme = theme_data[new_settings_data['theme']]

        setTooltipStyle()

        window.update_theme(theme['main_backgrounds'])
        eventTimer.update_theme(theme)

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
    eventTimer.update_when_to_notify(new_settings_data)
    settings_data = new_settings_data
    

main_layout = QHBoxLayout()
central.setLayout(main_layout)

tool_selector = Widget(theme['main_backgrounds'])
tool_selector_layout = QVBoxLayout()
tool_selector.setLayout(tool_selector_layout)
pomodoro_timer_button = Button("Pomodoro Timer", theme['button'], theme['text']['text_disabled'])
events_button = Button("Events", theme['button'], theme['text']['text_disabled'])
settings_button = Button("Settings", theme['button'], theme['text']['text_disabled'])
quit_button = Button("Quit app", theme['button'], theme['text']['text_disabled'])

tool_widget = StackedWidget(theme['main_backgrounds'])
tool_widget.addWidget(timer_widget(theme, tray))
tool_widget.addWidget(events_widget(theme, tray))
tool_widget.addWidget(settings_widget(theme, settings_data, refresh_settings)) 

sound_effect = QSoundEffect()
sound_effect.setSource(QUrl.fromLocalFile("assets/sounds/ding.wav"))
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
        QApplication.quit()

main_layout.addWidget(tool_selector)
main_layout.addWidget(tool_widget)
tool_selector_layout.addWidget(pomodoro_timer_button)
tool_selector_layout.addWidget(events_button)
tool_selector_layout.addWidget(settings_button)
tool_selector_layout.addWidget(quit_button)
pomodoro_timer_button.clicked.connect(lambda: tool_widget.setCurrentIndex(0))
events_button.clicked.connect(lambda: tool_widget.setCurrentIndex(1))
settings_button.clicked.connect(lambda: tool_widget.setCurrentIndex(2))
quit_button.clicked.connect(showQuitPopup)





window.show()
tray.notify("spark-organizer", "Running in background")

app.exec()