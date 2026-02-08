
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout

from helpers.stats_helper import get_stats
from styled_functions.styled_functions import ComboBox, Widget, Label, LineEdit, Button

class stats_widget(QWidget):
    def __init__(self, theme_data):
        super().__init__()
        self.theme_data = theme_data

        main_layout = QFormLayout()
        self.setLayout(main_layout)

        work_sessions_started_label = Label("Work sessions started:", self.theme_data['text'], 1)
        work_sessions_complete_label = Label("Completed work sessions:", self.theme_data['text'], 1)
        break_sessions_started_label = Label("Break sessions started:", self.theme_data['text'], 1)
        break_sessions_complete_label = Label("Break sessions completed:", self.theme_data['text'], 1)
        longer_break_sessions_started_label = Label("Longer sessions started:", self.theme_data['text'], 1)
        longer_break_sessions_complete_label = Label("Longer break sessions completed:", self.theme_data['text'], 1)
        cycles_started_label = Label("Cycles started:", self.theme_data['text'], 1)
        cycles_complete_label = Label("Cycles completed:", self.theme_data['text'], 1)

        self.work_sessions_started_stat = Label("1", self.theme_data['text'], 1)
        self.work_sessions_complete_stat = Label("1", self.theme_data['text'], 1)
        self.break_sessions_started_stat = Label("1", self.theme_data['text'], 1)
        self.break_sessions_complete_stat = Label("1", self.theme_data['text'], 1)
        self.longer_break_sessions_started_stat = Label("1", self.theme_data['text'], 1)
        self.longer_break_sessions_complete_stat = Label("1", self.theme_data['text'], 1)
        self.cycles_started_stat = Label("1", self.theme_data['text'], 1)
        self.cycles_complete_stat = Label("1", self.theme_data['text'], 1)
        self.update_stats()

        main_layout.addRow(work_sessions_started_label, self.work_sessions_started_stat)
        main_layout.addRow(work_sessions_complete_label, self.work_sessions_complete_stat)
        main_layout.addRow(break_sessions_started_label, self.break_sessions_started_stat)
        main_layout.addRow(break_sessions_complete_label, self.break_sessions_complete_stat)
        main_layout.addRow(longer_break_sessions_started_label, self.longer_break_sessions_started_stat)
        main_layout.addRow(longer_break_sessions_complete_label, self.longer_break_sessions_complete_stat)
        main_layout.addRow(cycles_started_label, self.cycles_started_stat)
        main_layout.addRow(cycles_complete_label, self.cycles_complete_stat)

    def update_stats(self):
        stats = get_stats()
        self.work_sessions_started_stat.setText(str(stats['work_started_count']))
        self.work_sessions_complete_stat.setText(str(stats['work_completed_count']))
        self.break_sessions_started_stat.setText(str(stats['break_started_count']))
        self.break_sessions_complete_stat.setText(str(stats['break_completed_count']))
        self.longer_break_sessions_started_stat.setText(str(stats['longer_break_started_count']))
        self.longer_break_sessions_complete_stat.setText(str(stats['longer_break_completed_count']))
        self.cycles_started_stat.setText(str(stats['cycles_started_count']))
        self.cycles_complete_stat.setText(str(stats['cycles_completed_count']))