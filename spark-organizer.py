from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox
from styled_functions.styled_functions import Button, Label, LineEdit, MainWindow, TableWidget, Widget, StackedWidget, ComboBox
import sys
from helpers.theme_helper import initializeThemes
from helpers.settings_helper import initializeSettings
from widgets.settings_widget import settings_widget
from widgets.timer_widget import timer_widget
from helpers.tray_helper import tray_helper
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import Qt, QUrl

theme_data = initializeThemes()

settings_data = initializeSettings()

current_theme_name = settings_data["theme"]
theme = theme_data[current_theme_name]

app = QApplication(sys.argv)
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

def refresh_theme(theme_name):
    theme = theme_data[theme_name]

    setTooltipStyle()

    window.update_theme(theme['main_backgrounds'])

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

main_layout = QHBoxLayout()
central.setLayout(main_layout)

tool_selector = Widget(theme['main_backgrounds'])
tool_selector_layout = QVBoxLayout()
tool_selector.setLayout(tool_selector_layout)
pomodoro_timer_button = Button("Pomodoro Timer", theme['button'], theme['text']['text_disabled'])
settings_button = Button("Settings", theme['button'], theme['text']['text_disabled'])
quit_button = Button("Quit app", theme['button'], theme['text']['text_disabled'])

tool_widget = StackedWidget(theme['main_backgrounds'])
tool_widget.addWidget(timer_widget(theme, tray))
tool_widget.addWidget(settings_widget(theme, settings_data, refresh_theme)) 

def setToolToTimer():
    tool_widget.setCurrentIndex(0)

def setToolToSettings():
    tool_widget.setCurrentIndex(1)

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
tool_selector_layout.addWidget(settings_button)
tool_selector_layout.addWidget(quit_button)
pomodoro_timer_button.clicked.connect(setToolToTimer)
settings_button.clicked.connect(setToolToSettings)
quit_button.clicked.connect(showQuitPopup)




window.show()
tray.notify("spark-organizer", "Running in background")

app.exec()