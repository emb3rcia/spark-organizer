import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QSystemTrayIcon

icon_file = os.path.join(os.path.dirname(__file__), "..", "assets", "svg", "icon.svg")
class tray_helper:
    def __init__(self, app, main_window):
        self.app = app
        self.main_window = main_window

        self.tray = QSystemTrayIcon(QIcon(icon_file), app)

        self.tray.toolTip("spark-organizer")
        self.tray.activated.connect(self.show_window)
        self.tray.show()

    def show_window(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.main_window.show()
            self.main_window.raise_()
            self.main_window.activateWindow()

    def notify(self, title, message):
        self.tray.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )