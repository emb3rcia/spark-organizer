import json
import os
from dataclasses import dataclass, asdict


@dataclass
class Event:
    id: str
    type: str
    title: str
    end_time: str
    start_time: str = None
    notified: bool = False

config_path = os.path.join(os.path.dirname(__file__), "..", "config")
os.makedirs(config_path, exist_ok=True)
EVENTS_FILE = os.path.join(config_path, "events.json")
REMINDERS_FILE = os.path.join(config_path, "reminders.json")

def get_events():
    if not os.path.isfile(EVENTS_FILE):
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

def remove_event(event_id: str):
    events = get_events()
    events = [event for event in events if event['id'] != event_id]

    with open(EVENTS_FILE, 'w') as f:
        json.dump(events, f, indent=4)

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

def get_reminders():
    if not os.path.isfile(REMINDERS_FILE):
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

def remove_reminder(reminder_id):
    reminders = get_reminders()
    reminders = [reminder for reminder in reminders if reminder['id'] != reminder_id]

    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)

def update_reminders(reminders):
    os.makedirs('config', exist_ok=True)
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=4)