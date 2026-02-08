from PyQt6.QtWidgets import QComboBox, QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem, QMessageBox
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QDateTime, QTimeZone, Qt, QUrl
from styled_functions.styled_functions import ComboBox, Widget, Label, Button, LineEdit, DateTimeEdit, TableWidget
from helpers.scheduled_helper import get_events, add_event, remove_event, Event
import uuid

class events_widget(QWidget):
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
        self.events_display_widget = TableWidget(self.theme_data['table'], self.theme_data['text']['text_disabled'], self.theme_data['extra'])
        self.events_display_widget.setColumnCount(5)
        self.events_display_widget.setHorizontalHeaderLabels(["Event type", "Event title", "Start date", "End date", "Delete event"])
        self.events_display_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.events_display_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.events_display_widget.horizontalHeader().setStretchLastSection(False)
        events_control_widget = Widget(self.theme_data['main_backgrounds'])
        events_control_layout = QFormLayout()
        events_control_widget.setLayout(events_control_layout)
        control_title_label = Label("Event title:", self.theme_data['text'], 1)
        self.control_title_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        events_control_layout.addRow(control_title_label, self.control_title_lineedit)
        control_type_label = Label("Event type:", self.theme_data['text'], 1)
        self.control_type_combobox = ComboBox(self.theme_data['combo-box'], self.theme_data['text']['text_disabled'])
        self.control_type_combobox.addItems(("deadline", "event"))
        self.control_type_combobox.setCurrentIndex(0)
        self.control_type_combobox.currentIndexChanged.connect(self.should_have_startdate)
        events_control_layout.addRow(control_type_label, self.control_type_combobox)
        start_date_label = Label("Select start date and time:", self.theme_data['text'], 1)
        self.start_date = DateTimeEdit(self.theme_data)
        self.start_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.should_have_startdate()
        end_date_label = Label("Select end date and time:", self.theme_data['text'], 1)
        self.end_date = DateTimeEdit(self.theme_data)
        self.end_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        events_control_layout.addRow(start_date_label, self.start_date)
        events_control_layout.addRow(end_date_label, self.end_date)
        add_event_button = Button("Add event", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        add_event_button.clicked.connect(self.add_event_function)
        events_control_layout.addRow(add_event_button)

        interact_widget.setLayout(interact_layout)
        interact_layout.addWidget(self.events_display_widget)
        interact_layout.addWidget(events_control_widget)

        main_layout.addWidget(interact_widget)

        self.update_events()

    def should_have_startdate(self):
        if self.control_type_combobox.currentIndex() == 0:
            self.start_date.setDisabled(True)
        else:
            self.start_date.setDisabled(False)
    
    def reset_fields(self):
        self.start_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.end_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.control_type_combobox.setCurrentIndex(0)
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

    def add_event_function(self):
        if self.control_type_combobox.currentText() == "event":
            if self.end_date.dateTime() < self.start_date.dateTime():
                self.showPopup("Incorrect settings", "Start date can't be set to before end date")
                return
            elif self.end_date.dateTime() < QDateTime.currentDateTime(QTimeZone.systemTimeZone()):
                self.showPopup("Incorrect settings", "End date can't be set to before now!")
                return
            else:
                event = Event(
                    id=str(uuid.uuid4()),
                    type=self.control_type_combobox.currentText(),
                    start_time=self.start_date.dateTime().toString(Qt.DateFormat.ISODate),
                    end_time=self.end_date.dateTime().toString(Qt.DateFormat.ISODate),
                    title=self.control_title_lineedit.text()
                )
        else:
            if self.end_date.dateTime() > QDateTime.currentDateTime(QTimeZone.systemTimeZone()):
                event = Event(
                    id=str(uuid.uuid4()),
                    type=self.control_type_combobox.currentText(),
                    start_time=None,
                    end_time=self.end_date.dateTime().toString(Qt.DateFormat.ISODate),
                    title=self.control_title_lineedit.text()
                )
            else:
                self.showPopup("Incorrect settings", "End date can't be set to before now!")
                return
        self.reset_fields()
        add_event(event)
        self.update_events()

    def update_events(self):
        self.events_display_widget.setRowCount(0)

        self.events = get_events()
        for event in self.events:
            row = self.events_display_widget.rowCount()
            self.events_display_widget.insertRow(row)

            self.events_display_widget.setItem(row, 0, QTableWidgetItem(event['type']))
            self.events_display_widget.setItem(row, 1, QTableWidgetItem(event['title']))
            self.events_display_widget.setItem(row, 2, QTableWidgetItem(str(event['start_time']).replace("T", " ") or ""))
            self.events_display_widget.setItem(row, 3, QTableWidgetItem((event['end_time']).replace("T", " ")))

            delete_button = Button("Delete", self.theme_data['button'], self.theme_data['text']['text_disabled'])
            
            eid = event['id']
            delete_button.clicked.connect(lambda checked=False, eid=eid: remove_event(eid, self.update_events))

            self.events_display_widget.setCellWidget(row, 4, delete_button)
