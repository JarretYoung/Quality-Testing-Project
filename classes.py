"""
This file is the class outlining the generic Event for the google calendar
"""
from datetime import datetime



class Event():
    def __init__(self, id, summary, location, creator, organisor, attendees, start, end) -> None:
        self.id = id        
        self.summary = summary
        self.location = location
        self.creator = creator
        self.organiser = organisor
        self.attendees = []
        for attendee in attendees:
            self.attendees.append(attendee)
        self.start = start
        self.end = end

    def add_id(self, id):
        self.id = id
    
    def add_creator(self, creator):
        self.creator = creator

    def add_organiser(self, organiser):
        self.organiser = organiser

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



