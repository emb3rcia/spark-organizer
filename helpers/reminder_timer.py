from PyQt6.QtCore import QObject, QTimer, QDateTime, QTimeZone, QUrl, Qt
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from helpers.scheduled_helper import get_reminders, update_reminders

class reminder_timer(QObject):
    def __init__(self, theme_data, window: QMainWindow, settings_data, interval_ms=5000):
        super().__init__(None)
        self.window = window
        self.settings_data = settings_data
        self.theme_data = theme_data
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("assets/sounds/ding.wav"))
        self.sound_effect.setVolume(0.5)
        self.timer = QTimer(self)
        self.timer.setInterval(interval_ms)
        self.timer.timeout.connect(self.check_reminders)

    def start(self):
        self.timer.start()
    
    def stop(self):
        self.timer.stop()
    
    def update_theme(self, theme_data):
        self.theme_data = theme_data

    def sendPopup(self, title, text):

        msg = QMessageBox(self.window)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Information)

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.theme_data['main_backgrounds']['popup_background']};
                color: {self.theme_data['text']['text_primary']}
                border: 1px solid {self.theme_data['accent']['info']}
            }}
        """
        )

        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        msg.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.sound_effect.play()
        msg.exec()

    def check_reminders(self):
        now = QDateTime.currentDateTime(QTimeZone.systemTimeZone())
        offset_secs = self.settings_data['minutes'] * 60
        reminders = get_reminders()
        changed = False
        for r in reminders:
            notification_date = QDateTime.fromString(r['notification_time'], Qt.DateFormat.ISODate)
            notify_date = notification_date.addSecs(-offset_secs)
            if notify_date <= now and r['notified'] == False:
                self.sendPopup(r['title'], f"Reminder: {r['title']}")
                r['notified'] = True
                changed = True
        if changed:
            update_reminders(reminders)
    
    def update_when_to_notify(self, settings_data):
        self.settings_data = settings_data