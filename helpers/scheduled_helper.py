import json
import os
import sys
from dataclasses import dataclass, asdict
from PyQt6.QtWidgets import QMessageBox, QApplication

if QApplication.instance() is None:
    app = QApplication([])

def show_corrupt_popup(file_name):
    msg = QMessageBox()
    msg.setWindowTitle("Corrupted themes.json detected")
    msg.setText(f"File {file_name} is corrupted!\nYou can overwrite it with default values and exit,\nor quit without changes to it, what would you want?")
    msg.setIcon(QMessageBox.Icon.Critical)
    write_defaults = msg.addButton("Write defaults and exit", QMessageBox.ButtonRole.AcceptRole)
    quit_button = msg.addButton("Quit", QMessageBox.ButtonRole.RejectRole)
    msg.exec()

    if msg.clickedButton() == write_defaults:
        return True
    return False

@dataclass
class Event:
    id: str
    type: str
    title: str
    end_time: str
    start_time: str = None
    notified: bool = False

EVENTS_FILE = 'config/events.json'

def get_events():
    if not os.path.exists(EVENTS_FILE):
        os.makedirs('config', exist_ok=True)
        with open(EVENTS_FILE, 'w') as f:
            f.write('[]')
        return []

    try:
        with open(EVENTS_FILE, 'r') as f:
            events = json.load(f)
            return events
    except json.JSONDecodeError:
        return 1
        

def add_event(event: Event):
    events = get_events()
    event_dict = asdict(event)
    events.append(event_dict)

    os.makedirs('config', exist_ok=True)
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=4)

def remove_event(event_id: str, update_events=None):
    events = get_events()
    events = [event for event in events if event['id'] != event_id]

    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=4)

    if update_events:
        update_events()

def update_events(events):
    os.makedirs('config', exist_ok=True)
    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=4)

@dataclass
class Reminder:
    id: str
    title: str
    notification_time: str = None
    notified: bool = False

REMINDERS_FILE = "config/reminders.json"

def get_reminders():
    if not os.path.exists(REMINDERS_FILE):
        os.makedirs('config', exist_ok=True)
        with open(REMINDERS_FILE, 'w') as f:
            f.write('[]')
        return []

    try:
        with open(REMINDERS_FILE, 'r') as f:
            reminders = json.load(f)
            return reminders
    except json.JSONDecodeError:
        return 1

def add_reminder(reminder: Reminder):
    reminders = get_reminders()
    reminder_dict = asdict(reminder)
    reminders.append(reminder_dict)

    os.makedirs('config', exist_ok=True)
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)

def remove_reminder(reminder_id: str, update_reminders=None):
    reminders = get_reminders()
    reminders = [reminder for reminder in reminders if reminder['id'] != reminder_id]

    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)

    if update_reminders:
        update_reminders()

def update_reminders(reminders):
    os.makedirs('config', exist_ok=True)
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)