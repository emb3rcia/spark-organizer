#imports built-in
import os

#imports pyqt
from PyQt6.QtCore import QObject, QTimer, QDateTime, QTimeZone, QUrl, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QMainWindow, QMessageBox

#imports helpers
from helpers.scheduled_helper import get_reminders, update_reminders

#define sound_effect_file path
sound_effect_file = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ding.wav")

class reminder_timer(QObject):
    def __init__(self, theme_data, window: QMainWindow, settings_data, tray, interval_ms=5000):
        super().__init__(None)
        #self definitions
        self.window = window
        self.tray = tray
        self.settings_data = settings_data
        self.theme_data = theme_data

        #initiate popup instance and set its style
        self.msg = QMessageBox(self.window)
        self.setPopupStyleEvent(self.theme_data)

        #define sound effect
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_effect_file))
        self.sound_effect.setVolume(0.5)

        #define timer
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self.check_reminders)

    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()
    
    def update_theme(self, theme_data):
        self.theme_data = theme_data

    def setPopupStyleReminder(self, theme_data):
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

    def sendPopup(self, title, text):
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        self.sound_effect.play()
        self.msg.exec()

    def check_reminders(self):
        now = QDateTime.currentDateTime(QTimeZone.systemTimeZone())
        offset_secs = self.settings_data['minutes_reminders'] * 60
        reminders = get_reminders()
        changed = False
        for r in reminders:
            if not r['notified']:
                notification_date = QDateTime.fromString(r['notification_time'], Qt.DateFormat.ISODate)
                notify_date = notification_date.addSecs(-offset_secs)
                if notify_date <= now and r['notified'] == False:
                    self.tray.notify(r['title'], f"Reminder: {r['title']}")
                    r['notified'] = True
                    changed = True
                    self.sendPopup(r['title'], f"Reminder: {r['title']}")
        if changed:
            update_reminders(reminders)
    
    def update_when_to_notify(self, settings_data):
        self.settings_data = settings_data