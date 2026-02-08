import uuid

from PyQt6.QtCore import QDateTime, QTimeZone, Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem, \
    QMessageBox

from helpers.scheduled_helper import get_reminders, add_reminder, remove_reminder, Reminder
from styled_functions.styled_functions import Widget, Label, Button, LineEdit, DateTimeEdit, TableWidget


class reminder_widget(QWidget):
    def __init__(self, theme_data, tray):
        super().__init__()
        self.tray = tray
        self.theme_data = theme_data
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile("assets/sounds/error.wav"))
        self.sound_effect.setVolume(0.5)
        interact_widget = Widget(self.theme_data['main_backgrounds'])
        interact_layout = QHBoxLayout()
        self.reminders_display_widget = TableWidget(self.theme_data['table'], self.theme_data['text']['text_disabled'], self.theme_data['extra'])
        self.reminders_display_widget.setColumnCount(3)
        self.reminders_display_widget.setHorizontalHeaderLabels(["Reminder title", "Notification date", "Delete event"])
        self.reminders_display_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.reminders_display_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.reminders_display_widget.horizontalHeader().setStretchLastSection(False)
        reminders_control_widget = Widget(self.theme_data['main_backgrounds'])
        reminders_control_layout = QFormLayout()
        reminders_control_widget.setLayout(reminders_control_layout)
        control_title_label = Label("Reminder title:", self.theme_data['text'], 1)
        self.control_title_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        reminders_control_layout.addRow(control_title_label, self.control_title_lineedit)
        notification_date_label = Label("Select reminder date and time:", self.theme_data['text'], 1)
        self.notification_date = DateTimeEdit(self.theme_data)
        self.notification_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        reminders_control_layout.addRow(notification_date_label, self.notification_date)
        add_reminder_button = Button("Add reminder", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        add_reminder_button.clicked.connect(self.add_reminder_function)
        reminders_control_layout.addRow(add_reminder_button)

        interact_widget.setLayout(interact_layout)
        interact_layout.addWidget(self.reminders_display_widget)
        interact_layout.addWidget(reminders_control_widget)

        main_layout.addWidget(interact_widget)

        self.update_reminders()

    def reset_fields(self):
        self.notification_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.control_title_lineedit.setText("")
    
    def showPopup(self, title, text):
        msg = QMessageBox(self)
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

    def add_reminder_function(self):
        if self.notification_date.dateTime() > QDateTime.currentDateTime(QTimeZone.systemTimeZone()):
            reminder = Reminder(
                id=str(uuid.uuid4()),
                notification_time=self.notification_date.dateTime().toString(Qt.DateFormat.ISODate),
                title=self.control_title_lineedit.text()
            )
        elif not self.control_title_lineedit.text().strip():
            self.showPopup("Incorrect settings", "Title cannot be empty!")
            return
        else:
            self.showPopup("Incorrect settings", "Notification date can't be set to before now!")
            return
        self.reset_fields()
        add_reminder(reminder)
        self.update_reminders()

    def update_reminders(self):
        self.reminders_display_widget.setRowCount(0)

        self.reminders = get_reminders()
        for reminder in self.reminders:
            row = self.reminders_display_widget.rowCount()
            self.reminders_display_widget.insertRow(row)

            self.reminders_display_widget.setItem(row, 0, QTableWidgetItem(reminder['title']))
            self.reminders_display_widget.setItem(row, 1, QTableWidgetItem(str(reminder['notification_time'].replace("T", " ") if reminder['notification_time'] else "")))

            delete_button = Button("Delete", self.theme_data['button'], self.theme_data['text']['text_disabled'])
            
            rid = reminder['id']
            delete_button.clicked.connect(lambda checked=False, rid=rid: remove_reminder(rid, self.update_reminders))

            self.reminders_display_widget.setCellWidget(row, 2, delete_button)
