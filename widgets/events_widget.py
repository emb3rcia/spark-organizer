#imports built-it
import os
import uuid

#imports pyqt
from PyQt6.QtCore import QDateTime, QTimeZone, Qt, QUrl
from PyQt6.QtGui import QColor
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem, QMessageBox

#imports helper
from helpers.scheduled_helper import get_events, add_event, remove_event, Event

#imports styled_functions
from styled_functions.styled_functions import ComboBox, Widget, Label, Button, LineEdit, DateTimeEdit, TableWidget

#define sound effect file path
sound_effect_file = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "error.wav")

class events_widget(QWidget):
    def __init__(self, theme_data, tray, window):
        super().__init__()
        #define pyqt6 required values
        self.tray = tray
        self.theme_data = theme_data
        self.window = window
        self.msg = QMessageBox(self.window)

        #define sound effect
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_effect_file))
        self.sound_effect.setVolume(0.5)

        #define main layouts and widgets
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        interact_widget = Widget(self.theme_data['main_backgrounds'])
        interact_layout = QHBoxLayout()

        #define events_display table
        self.events_display_widget = TableWidget(self.theme_data['table'], self.theme_data['text']['text_disabled'], self.theme_data['extra'])
        self.events_display_widget.setColumnCount(5)
        self.events_display_widget.setHorizontalHeaderLabels(["Event type", "Event title", "Start date", "End date", "Delete event"])
        self.events_display_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.events_display_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.events_display_widget.horizontalHeader().setStretchLastSection(False)

        #define events_control layout and widget
        events_control_widget = Widget(self.theme_data['main_backgrounds'])
        events_control_layout = QFormLayout()
        events_control_widget.setLayout(events_control_layout)

        #define title row
        control_title_label = Label("Event title:", self.theme_data['text'], 1)
        self.control_title_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])


        #define type row
        control_type_label = Label("Event type:", self.theme_data['text'], 1)
        self.control_type_combobox = ComboBox(self.theme_data['combo-box'], self.theme_data['text']['text_disabled'])
        self.control_type_combobox.addItems(("deadline", "event"))
        self.control_type_combobox.setCurrentIndex(0)
        self.control_type_combobox.currentIndexChanged.connect(self.should_have_startdate)

        #define start date row
        start_date_label = Label("Select start date and time:", self.theme_data['text'], 1)
        self.start_date = DateTimeEdit(self.theme_data)
        self.start_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.should_have_startdate()

        #define end date row
        end_date_label = Label("Select end date and time:", self.theme_data['text'], 1)
        self.end_date = DateTimeEdit(self.theme_data)
        self.end_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))

        #define add event button
        add_event_button = Button("Add event", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        add_event_button.clicked.connect(self.add_event_function)

        #add rows to layout
        events_control_layout.addRow(control_title_label, self.control_title_lineedit)
        events_control_layout.addRow(control_type_label, self.control_type_combobox)
        events_control_layout.addRow(start_date_label, self.start_date)
        events_control_layout.addRow(end_date_label, self.end_date)
        events_control_layout.addRow(add_event_button)

        #add layout and widgets to interact layout
        interact_widget.setLayout(interact_layout)
        interact_layout.addWidget(self.events_display_widget)
        interact_layout.addWidget(events_control_widget)

        #add interact_widget to main layouts
        main_layout.addWidget(interact_widget)

        #update events in taable
        self.update_events()

    def should_have_startdate(self):
        if self.control_type_combobox.currentText() != "event":
            self.start_date.setDisabled(True)
        else:
            self.start_date.setDisabled(False)
    
    def reset_fields(self):
        self.start_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.end_date.setDateTime(QDateTime.currentDateTime(QTimeZone.systemTimeZone()))
        self.control_type_combobox.setCurrentIndex(0)
        self.control_title_lineedit.setText("")

    def setPopupStyleEventsError(self, theme_data):
        self.theme_data = theme_data

        palette = self.msg.palette()
        palette.setColor(self.msg.backgroundRole(), QColor(self.theme_data['main_backgrounds']['popup_background']))
        palette.setColor(self.msg.foregroundRole(), QColor(self.theme_data['text']['text_primary']))
        self.msg.setPalette(palette)

        self.msg.setStyleSheet(f"""
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

    def showPopup(self, title, text):
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        self.msg.setIcon(QMessageBox.Icon.Critical)
        self.msg.setStyleSheet(f"""
            QMessageBox {{
                 border: 1px solid {self.theme_data['accent']['error']};
            }}
            """
            )
        self.sound_effect.play()
        self.msg.exec()

    def add_event_function(self):
        if not self.control_title_lineedit.text().strip():
            self.showPopup("Incorrect settings", "Title cannot be empty!")
            return
        if self.control_type_combobox.currentText() == "event":
            if self.end_date.dateTime() < self.start_date.dateTime():
                self.showPopup("Incorrect settings", "Start date can't be set to before end date")
                return
            elif self.end_date.dateTime() < QDateTime.currentDateTime(QTimeZone.systemTimeZone()):
                self.showPopup("Incorrect settings", "End date can't be set to before now!")
                return
            elif self.start_date.dateTime() < QDateTime.currentDateTime(QTimeZone.systemTimeZone()):
                self.showPopup("Incorrect settings", "Start date can't be set to before now!")
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
            self.events_display_widget.setItem(row, 2, QTableWidgetItem(str(event['start_time'].replace("T", " ") if event['start_time'] else "")))
            self.events_display_widget.setItem(row, 3, QTableWidgetItem((event['end_time']).replace("T", " ")))

            delete_button = Button("Delete", self.theme_data['button'], self.theme_data['text']['text_disabled'])
            
            eid = event['id']
            delete_button.clicked.connect(lambda checked=False, eid=eid: remove_event(eid, self.update_events))

            self.events_display_widget.setCellWidget(row, 4, delete_button)
