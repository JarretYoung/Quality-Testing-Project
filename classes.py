"""
This file is the class outlining the generic Event for the google calendar
"""

class Event():
    def __init__(self, summary, location, attendees, start, end) -> None:
        self.id = None
        self.summary = summary
        self.location = location
        self.attendees = []
        for attendee in attendees:
            self.attendees.append(attendee)
        self.start = start
        self.end = end

    def add_id(self, id):
        self.id = id

    def get_JSON_format(self):
        json = {
        'summary': '{name}'.format(name=self.summary),
        'location': '{location}'.format(location=self.location),
        'description': '',
        'start': {
            'dateTime': '{time}'.format(time=self.start),
            'timeZone': 'Asia/Singapore',
        },
        'end': {
            'dateTime': '{time}'.format(time=self.end),
            'timeZone': 'Asia/Singapore',
        },
        'attendees': self.attendees,
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }
        return json

class Attendee():
    def __init__(self, email) -> None:
        self.email = email

class Date():
    def __init__(self, dateTime, timeZone) -> None:
        self.dateTime = dateTime
        self.timeZone = timeZone
