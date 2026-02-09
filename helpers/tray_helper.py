#imports built-in
import os

#imports pyqt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon

#define path
icon_file = os.path.join(os.path.dirname(__file__), "..", "assets", "svg", "icon.svg")

class tray_helper:
    def __init__(self, app, main_window):
        #define pyqt6 required values
        self.app = app
        self.main_window = main_window

        #set tray icon
        self.tray = QSystemTrayIcon(QIcon(icon_file), app)

        #set tooltip
        self.tray.setToolTip("spark-organizer")

        #connect function and show in tray
        self.tray.activated.connect(self.show_window)
        self.tray.show()

    #show window when clicked
    def show_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    #notify function
    def notify(self, title, message):
        self.tray.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )