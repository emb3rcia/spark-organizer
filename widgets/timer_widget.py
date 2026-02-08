from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QMessageBox
from PyQt6.QtGui import QIntValidator

from helpers.stats_helper import add_one_to_stat
from styled_functions.styled_functions import Widget, Label, LineEdit, Button
from PyQt6.QtCore import QTimer, Qt, QUrl
from PyQt6.QtMultimedia import QSoundEffect

import os

sound_effect_file = os.path.join(os.path.dirname(__file__), "..", "assets", "sounds", "ding.wav")

NOT_STARTED = 2
RUNNING = 0
PAUSED = 1

WORK = 1
BREAK = 2
LONGER_BREAK = 3

class timer_widget(QWidget):
    def __init__(self, theme_data, tray, stats_widget):
        super().__init__()
        self.tray = tray
        self.paused = NOT_STARTED
        self.lifecycle = 0 #0 = not started
        self.work_time_seconds = None
        self.break_time_seconds = None
        self.longer_break_time_seconds = None
        self.stats_widget = stats_widget
        self.cycles = None
        self.passed_cycles = 0
        self.theme_data = theme_data
        self.sound_effect = QSoundEffect()
        self.sound_effect.setSource(QUrl.fromLocalFile(sound_effect_file))
        self.sound_effect.setVolume(0.5)

        self.timer_label = Label("00:00:00", self.theme_data['text'], 1)
        self.timer_button = Button("Start timer", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        self.timer_button.clicked.connect(self.startOrPauseTimer)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.remaining_seconds = 0
        self.updateDisplay()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        interact_widget = Widget(self.theme_data['main_backgrounds'])
        interact_layout = QFormLayout()
        interact_widget.setLayout(interact_layout)
        main_layout.addWidget(interact_widget)
        validator = QIntValidator(1, 9999)

        work_time_label = Label("Work time:", self.theme_data['text'], 1)
        self.work_time_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.work_time_lineedit.setPlaceholderText("How many minutes you want to work")
        self.work_time_lineedit.setValidator(validator)
        interact_layout.addRow(work_time_label, self.work_time_lineedit)

        break_time_label = Label("Break time:", self.theme_data['text'], 1)
        self.break_time_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.break_time_lineedit.setPlaceholderText("How many minutes should break be")
        self.break_time_lineedit.setValidator(validator)
        interact_layout.addRow(break_time_label, self.break_time_lineedit)

        longer_break_time_label = Label("Longer break time:", self.theme_data['text'], 1)
        self.longer_break_time_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.longer_break_time_lineedit.setPlaceholderText("How many minutes should longer break be")
        self.longer_break_time_lineedit.setValidator(validator)
        interact_layout.addRow(longer_break_time_label, self.longer_break_time_lineedit)

        cycles_label = Label("How many cycles before longer break:", self.theme_data['text'], 1)
        self.cycles_lineedit = LineEdit(self.theme_data['input'], self.theme_data['highlight'], self.theme_data['text']['text_disabled'])
        self.cycles_lineedit.setPlaceholderText("How many cycles should be between longer breaks")
        self.cycles_lineedit.setValidator(validator)
        phase_descriptor_label = Label("Current timer:", self.theme_data['text'], 1)
        self.phase_label = Label("Not started", self.theme_data['text'], 1)
        reset_button = Button("Reset timer", self.theme_data['button'], self.theme_data['text']['text_disabled'])
        reset_button.clicked.connect(self.resetTimers)
        interact_layout.addRow(cycles_label, self.cycles_lineedit)
        interact_layout.addRow(self.timer_label, self.timer_button)
        interact_layout.addRow(phase_descriptor_label, self.phase_label)
        interact_layout.addRow(reset_button)
    
    def disableInputs(self, boolean: bool):
        self.work_time_lineedit.setDisabled(boolean)
        self.break_time_lineedit.setDisabled(boolean)
        self.longer_break_time_lineedit.setDisabled(boolean)
        self.cycles_lineedit.setDisabled(boolean)
    
    def resetTimers(self):
        self.work_time_seconds = None
        self.break_time_seconds = None
        self.longer_break_time_seconds = None
        self.cycles = None
        self.passed_cycles = 0
        self.lifecycle = 0
        self.disableInputs(False)
        self.timer_label.setText("00:00:00")
        self.paused = NOT_STARTED
        self.phase_label.setText("Not started")
        self.timer_button.setText("Start timer")
        self.timer.stop()
        self.remaining_seconds = 0

    def startOrPauseTimer(self):
        if self.work_time_seconds is None:
            txt = self.work_time_lineedit.text().strip() or "25"
            minutes = int(txt)
            self.work_time_seconds = minutes * 60
        if self.break_time_seconds is None:
            txt = self.break_time_lineedit.text().strip() or "5"
            minutes = int(txt)
            self.break_time_seconds = minutes * 60
        if self.longer_break_time_seconds is None:
            txt = self.longer_break_time_lineedit.text().strip() or "15"
            minutes = int(txt)
            self.longer_break_time_seconds = minutes * 60
        if self.cycles is None:
            txt = self.cycles_lineedit.text().strip() or "4"
            cycles = int(txt)
            self.cycles = cycles if cycles > 0 else 4
        if self.paused == PAUSED:
            self.timer_button.setText("Pause timer")
            self.paused = RUNNING
            self.timer.start(1000)
            return
        elif self.paused == RUNNING:
            self.timer_button.setText("Resume timer")
            self.paused = PAUSED
            self.timer.stop()
            return
        elif self.paused == NOT_STARTED:
            self.timer_button.setText("Pause timer")
            self.paused = RUNNING
            self.remaining_seconds = self.work_time_seconds
            self.phase_label.setText("Work")
            self.updateDisplay()
            self.tray.notify("Started timer!", "Work time!")
            self.lifecycle = WORK
            add_one_to_stat("work_started_count")
            self.stats_widget.update_stats()
            self.timer.start(1000)
            self.disableInputs(True)
            return
    

    def showPhasePopup(self, title, text):
        self.timer.stop()

        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(QMessageBox.Icon.Information)

        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {self.theme_data['main_backgrounds']['popup_background']};
                color: {self.theme_data['text']['text_primary']};
                border: 1px solid {self.theme_data['accent']['info']};
            }}
        """
        )

        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        msg.setWindowModality(Qt.WindowModality.ApplicationModal)

        self.sound_effect.play()
        msg.exec()
        
        if self.paused == RUNNING:
            self.timer.start(1000)

    def updateDisplay(self):
        h = self.remaining_seconds // 3600
        m = (self.remaining_seconds % 3600) // 60
        s = self.remaining_seconds % 60

        self.timer_label.setText(f"{h:02}:{m:02}:{s:02}")

    def updateTimer(self):
        if self.remaining_seconds <= 0:
            self.timer.stop()
            if self.lifecycle == WORK:
                self.passed_cycles += 1
                add_one_to_stat("cycles_completed_count")
                self.stats_widget.update_stats()
                if self.passed_cycles >= self.cycles:
                    if self.longer_break_time_seconds and self.longer_break_time_seconds > 0:
                        self.remaining_seconds = self.longer_break_time_seconds
                        self.updateDisplay()
                    else:
                        self.resetTimers()
                        return
                    self.tray.notify("Work time finished!", "Longer break time!")
                    self.showPhasePopup("Longer break time!", "Wow! You finished your work cycles! Now you get longer break!")
                    self.phase_label.setText("Longer break")
                    self.passed_cycles = 0
                    add_one_to_stat("work_completed_count")
                    add_one_to_stat("longer_break_started_count")
                    self.stats_widget.update_stats()
                    self.lifecycle = LONGER_BREAK

                else:
                    if self.break_time_seconds and self.break_time_seconds > 0:
                        self.remaining_seconds = self.break_time_seconds
                        self.updateDisplay()
                    else:
                        self.resetTimers()
                        return
                    self.tray.notify("Work time finished!", "Break time!")
                    self.showPhasePopup("Break time!", "Work session finished! Now you have break!")
                    self.phase_label.setText("Break")
                    add_one_to_stat("work_completed_count")
                    add_one_to_stat("break_started_count")
                    self.stats_widget.update_stats()
                    self.lifecycle = BREAK

            elif self.lifecycle == BREAK:
                if self.work_time_seconds and self.work_time_seconds > 0:
                    self.remaining_seconds = self.work_time_seconds
                    self.updateDisplay()
                else:
                    self.resetTimers()
                    return
                self.tray.notify("Break time finished!", "Work time!")
                self.showPhasePopup("Time to work!", "Your break ended, go to work!")
                self.phase_label.setText("Work")
                add_one_to_stat("work_started_count")
                add_one_to_stat("break_completed_count")
                add_one_to_stat("cycles_started_count")
                self.stats_widget.update_stats()
                self.lifecycle = WORK
            elif self.lifecycle == LONGER_BREAK:
                if self.work_time_seconds and self.work_time_seconds > 0:
                    self.remaining_seconds = self.work_time_seconds
                    self.updateDisplay()
                else:
                    self.resetTimers()
                    return
                self.tray.notify("Longer break time finished!", "Work time!")
                self.showPhasePopup("Time to work!", "Your longer break ended, go to work!")
                self.phase_label.setText("Work")
                add_one_to_stat("work_started_count")
                add_one_to_stat("longer_break_completed_count")
                add_one_to_stat("cycles_completed_count")
                self.stats_widget.update_stats()
                self.lifecycle = WORK

            if self.remaining_seconds <= 0:
                self.resetTimers()
                return

            self.timer.start(1000)
            return

        self.remaining_seconds -= 1
        self.updateDisplay()