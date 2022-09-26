from multiprocessing.sharedctypes import Value
import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
# Add other imports here if needed
import datetime
import importlib.util
import os.path
import sys
from contextlib import contextmanager
from io import StringIO
from application import Application
from classes import Event

@contextmanager
def automatedInputOutput(inputList=[]):
    newIn, newOut = StringIO("\n".join(inputList)), StringIO()
    oldIn, oldOut = sys.stdin, sys.stdout
    try:
        sys.stdin, sys.stdout = newIn, newOut
        yield sys.stdin, sys.stdout
    finally:
        sys.stdin, sys.stdout = oldIn, oldOut



test_event_1 = {
    'kind': 'calendar#event',
    'etag': '"3327475922566000"',
    'id': '7k6giqb8k7ck6po83pbof50sij',
    'summary': 'FIT2107 Assignment Test Valid',
    'description': 'This is a test',
    'location': '123 Fake St. Clayton VIC 3400',
    'creator': {
        'email': 'bcho0029@student.monash.edu',
        'self': True
    },
    'organizer': {
        'email': 'bcho0029@student.monash.edu',
        'self': True
    },
    'start': {
        'dateTime': '2023-09-14T09:00:00-07:00',
        'timeZone': 'Asia/Singapore'
    },
    'end': {
        'dateTime': '2023-09-15T17:00:00-07:00',
        'timeZone': 'Asia/Singapore'
    },
    'attendees': [
        {
            'email': 'gyon0004@student.monash.edu',
            'organizer': True,
            'self': True,
            'responseStatus': 'accepted'
        }
    ],
        'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

# user_input = ["5", "5", "1", "bcho0029@student.monash.edu", "add", "1", "bishan.choo04@gmail",'e']
# Simulating user input
user_input = ["9", "1", "e"]

with automatedInputOutput(user_input) as (inGen, outGen):
    mock_api = MagicMock()
    mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
    time_now = '2022-09-24T03:29:17.380207Z'
    running_application = Application(mock_api, time_now)
    running_application.on_start()

# print(len(running_application.event_list[0].attendees))
print(running_application.event_list[0].reminders)