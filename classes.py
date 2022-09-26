"""
This file is the class outlining the generic Event for the google calendar
"""
from datetime import datetime



class Event():
    def __init__(self, id, summary, location, creator, organisor, attendees, start, end) -> None:
        self.id = id                            # To access .id
        self.summary = summary                  # To access .summary
        self.location = location                # To access .location
        self.creator = creator                  # To access .creator['email']
        self.organiser = organisor              # To access .organiser['email']
        self.attendees = []                     # To access .attendees[index]['email']
        for attendee in attendees:
            self.attendees.append(attendee)
        self.start = start                      # To access .start['dateTime']
        self.end = end                          # To access .end['dateTime']

    def add_id(self, id):
        self.id = id
    
    def add_creator(self, creator):
        self.creator = creator

    def add_organiser(self, organiser):
        self.organiser = organiser

    def add_start(self, start):
        self.start = start
    
    def add_end(self, end):
        self.end = end

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

class Attendee:
	def __init__(self,email,isOwner=False):
		self.email = email
		self.isOwner = isOwner

