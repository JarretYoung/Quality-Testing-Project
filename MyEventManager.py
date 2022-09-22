# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.
# can send calendar event invitation to a student using the student.monash.edu email.
# The app doesn't support sending events to non student or private emails such as outlook, gmail etc
# students must have their own api key
# no test cases for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
from tracemalloc import start
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from classes import *

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])

def check_event_input(event: Event, summary, location, attendees, start_date, end_date):
    valid = True
    if summary == "" or summary == None:
        raise ValueError('Event must have a name')
    if location == "" or location == None:
        raise ValueError('Event must have location')
    # Add check for online location
    # Add check for physical location
    if len(attendees) == 0:
        raise ValueError('Event must have at least one attendee')
    # Add check for attendee email presence (maybe)?
    if start_date == "" or start_date == None:
        raise ValueError('Event must have a start date')
    # Add check for time format
    if end_date == "" or end_date == None:
        raise ValueError('Event must have an end date')
    # Add check for time format



    if event.summary == "":
        valid = False
    if event.location == "":
        valid = False
    if len(event.attendees) == 0:
        valid = False
    if event.start == "":
        valid = False
    return valid


def start_new_event():
    organiser_status = None
    while organiser_status == None:
        organiser_confirmation = input("Are you the organiser? Y/N")
        if organiser_confirmation.upper() == 'Y':
            organiser_status = True
        elif organiser_confirmation.upper() == 'N':
            organiser_status = False

    
    summary = input("Insert Event Name")

    location = input("Insert location of event")

    list_of_attendees = []
    number_of_attendees = input("Please enter the number of attendees")
    for i in range(number_of_attendees):
        email = input("Input attendee " + str(i) + "'s email" )
        attendee = Attendee(email)
        list_of_attendees.append(attendee)

    start_date = input("Insert a start date")
    start = '{date}T09:00:00-07:00'.format(date=start_date)

    end_date = input("Insert a end date")
    end = '{date}T17:00:00-07:00'.format(time=end_date)

    check_event_input(summary, location, list_of_attendees, start_date, end_date)

    event = Event(summary, location, list_of_attendees, start, end)


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()