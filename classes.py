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

    def get_JSON_format(self):
        json = {
        'summary': '{location}'.format(time=self.location),
        'location': '{location}'.format(location=self.location),
        'description': '',
        'start': {
            'dateTime': '{time}'.format(time=self.start),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '{time}'.format(time=self.end),
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
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
