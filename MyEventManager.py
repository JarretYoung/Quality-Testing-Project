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


# Code adapted from https://developers.google.gtcom/calendar/quickstart/python
from __future__ import print_function
from aifc import Error
import datetime
from fileinput import filename
from importlib.resources import path
import pickle
import os.path
from traceback import print_tb
from tracemalloc import start
from xml.dom import ValidationErr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from classes import *
from datetime import *
import datetime
import re
import json
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


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


def get_upcoming_events(api, starting_time):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    # if (number_of_events <= 0):
    #     raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax='2050-01-01T07:35:12.084923Z',
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    # events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax = '2050-01-01T07:35:12.084923Z',
    #                                   maxResults=number_of_events, singleEvents=True,
    #                                   orderBy='startTime').execute()
    return events_result.get('items', [])


def get_all_events(api):
    """
    Returns all the events 
    """

    events_result = api.events().list(calendarId='primary', timeMin='2010-01-01T07:35:12.084923Z',
                                      timeMax='2050-01-01T07:35:12.084923Z', singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def check_email_validity(email, attendee_number):
    """
    This code was copied from geeksforgeeks

    @author:    @ankthon
    @from:      https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    """
    # Make a regular expression
    # for validating an Email
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Define a function for
    # for validating an Email

    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        pass
    else:
        raise ValueError("Attendee {number}'s email is invalid".format(
            number=attendee_number + 1))


def check_event_input(summary, location, creator, organizer, attendees, start_date, end_date):
    valid = True
    # Checking for Event name
    if summary == "" or summary == None:
        raise ValueError('Event must have a name')

    # Checking for Event location
    if location == "" or location == None:
        raise ValueError('Event must have location (Online or Physical)')
    # Check if location is online and if it is valid
    check_location_is_online = (location[0:4] == "http")
    # Check if location is physical and if it is valid
    location_in_list_form = location.split(" ")
    check_location_is_physical = True
    try:
        temp = location_in_list_form[-2]
    except IndexError:
        check_location_is_physical = False
    else:
        # 4 <= len(postal_code) <= 5
        if (len(location_in_list_form[-1]) < 4) or (len(location_in_list_form[-1]) > 5):
            check_location_is_physical = False
        if (len(location_in_list_form[-2]) < 2) or (
                len(location_in_list_form[-2]) > 3):  # 2 <= len(state_abbreviation) <= 3
            check_location_is_physical = False
    # Final check to see if location is valid
    if (check_location_is_online == False) and (check_location_is_physical == False):
        raise ValueError(
            'Physical Event location must follow Australian or American format; Online Events must have a join link')

    # Check for Event Attendees
    if len(attendees) == 0:
        raise ValueError('Event must have at least one attendee')
    for i in range(len(attendees)):
        check_email_validity(attendees[i]['email'], i)

        # Checking for Event time
    if start_date == "" or start_date == None:
        raise ValueError('Event must have a start date')
    # Add check for time format
    MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    try:
        # Checking for yyyy-mm-dd format
        datetime.datetime.strptime(start_date, '%Y-%M-%d')
    except ValueError:
        date_as_list = start_date.split("-")
        try:
            # Checking if overall formatting is correct ex: using '/' instead of '-' to separate the date
            temp = date_as_list[-2]
        except IndexError:
            raise ValueError(
                "Start Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
        else:
            # Assuming input is following dd-MON-yy
            month = 0
            # Identifying which month was inputted based on the MONTHS list above
            for i in range(len(MONTHS)):
                if date_as_list[1] == MONTHS[i]:
                    month = i + 1
            # If month was not identified, assume that input was of wrong format; else reconstruct date
            if month == 0:
                raise ValueError(
                    "Start Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
            else:
                start_date = '{day}-{MONTH}-{year}'.format(
                    day=date_as_list[0], MONTH=month, year=date_as_list[2])
            # Test if date is of acceptable format using datetime package
            try:
                datetime.datetime.strptime(start_date, '%d-%M-%y')
            except ValueError:
                raise ValueError(
                    "Start Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")

    if end_date == "" or end_date == None:
        raise ValueError('Event must have an end date')
    # Add check for time format
    MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    try:
        # Checking for yyyy-mm-dd format
        datetime.datetime.strptime(end_date, '%Y-%M-%d')
    except ValueError:
        date_as_list = end_date.split("-")
        try:
            # Checking if overall formatting is correct ex: using '/' instead of '-' to separate the date
            temp = date_as_list[-2]
        except IndexError:
            raise ValueError(
                "End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
        else:
            # Assuming input is following dd-MON-yy
            month = 0
            # Identifying which month was inputted based on the MONTHS list above
            for i in range(len(MONTHS)):
                if date_as_list[1] == MONTHS[i]:
                    month = i + 1
            # If month was not identified, assume that input was of wrong format; else reconstruct date
            if month == 0:
                raise ValueError(
                    "End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
            else:
                end_date = '{day}-{MONTH}-{year}'.format(
                    day=date_as_list[0], MONTH=month, year=date_as_list[2])
            # Test if date is of acceptable format using datetime package
            try:
                datetime.datetime.strptime(end_date, '%d-%M-%y')
            except ValueError:
                raise ValueError(
                    "End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")


def start_new_event(api, summary, location, list_of_attendees, start_date, end_date):

    check_event_input(summary, location, list_of_attendees,
                      start_date, end_date)

    MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
              'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    try:
        # Checking for yyyy-mm-dd format
        datetime.datetime.strptime(start_date, '%Y-%M-%d')
    except ValueError:
        date_as_list = start_date.split("-")
        # Assuming input is following dd-MON-yy
        month = 0
        # Identifying which month was inputted based on the MONTHS list above
        for i in range(len(MONTHS)):
            if date_as_list[1] == MONTHS[i]:
                month = i+1
        # Reconstruct date
        start_date = '20{year}-{MONTH}-{day}'.format(
            day=date_as_list[0], MONTH=month, year=date_as_list[2])
    finally:
        start = '{date}T09:00:00-07:00'.format(date=start_date)

    try:
        # Checking for yyyy-mm-dd format
        datetime.datetime.strptime(end_date, '%Y-%M-%d')
    except ValueError:
        date_as_list = end_date.split("-")
        # Assuming input is following dd-MON-yy
        month = 0
        # Identifying which month was inputted based on the MONTHS list above
        for i in range(len(MONTHS)):
            if date_as_list[1] == MONTHS[i]:
                month = i+1
        # Reconstruct date
        end_date = '20{year}-{MONTH}-{day}'.format(
            day=date_as_list[0], MONTH=month, year=date_as_list[2])
    finally:
        end = '{date}T17:00:00-07:00'.format(date=end_date)

    event = Event(None, summary, location, None,
                  None, list_of_attendees, start, end)

    event_output = api.events().insert(calendarId='primary',
                                       body=event.get_JSON_format()).execute()

    if event_output['id'] != None:
        event.add_id(event_output['id'])
        event.add_creator(event_output['creator'])
        event.add_organiser(event_output['organizer'])

    return event


def delete_existing_event(api, event_id, event_date, current_date):
    # Check if < current date ; if not then abort
    if event_date >= current_date:
        raise ValueError('You can only delete past events')

    # delete using api
    api.events().delete(calendarId='primary', eventId=event_id).execute()


def addAttendee(api, eventId, newAttendeeEmail):
    try:
        event = api.events().get(calendarId='primary', eventId=eventId).execute()

        eventLaterThan2050 = isEventLaterThan2050(event)
        if eventLaterThan2050:
            raise Exception("Can't edit event that is later than 2050")

        attendees = event['attendees']
        initialAttendeeAmount = len(attendees)

        if initialAttendeeAmount == 20:
            raise Exception("Event has reached a maximum of 20 attendees")

        attendees.append({"email": newAttendeeEmail})
        updatedEvent = api.events().patch(calendarId='primary', eventId=eventId, body={"attendees": attendees},
                                          sendUpdates="all").execute()

        if (len(updatedEvent['attendees']) == initialAttendeeAmount):
            print(f'{newAttendeeEmail} is already an attendee in this event')
        else:
            print(
                f'{newAttendeeEmail} was added to event {eventId} on {updatedEvent["updated"]}.')

        return updatedEvent['attendees']
    except Exception as e:
        print(e)
        print(
            f'{newAttendeeEmail} was not added successfully to event {eventId} as attendee.')
        return False


def removeAttendee(api, eventId, attendeeEmail):
    try:
        event = api.events().get(calendarId='primary', eventId=eventId).execute()

        eventLaterThan2050 = isEventLaterThan2050(event)
        if eventLaterThan2050:
            raise Exception("Can't edit event that is later than 2050")

        attendees = event['attendees']
        initialAttendeeAmount = len(attendees)
        # get attendees that are not attendeeEmail
        attendees = list(
            filter(lambda attendee: attendee['email'] != attendeeEmail, attendees))
        updatedEvent = api.events().patch(calendarId='primary', eventId=eventId, body={
            "attendees": attendees}, sendUpdates="all").execute()  # update event with new attendee list

        if len(attendees) == (initialAttendeeAmount-1):
            print(
                f'{attendeeEmail} was removed from event {eventId} on {updatedEvent["updated"]}.')
        else:
            print(f'{attendeeEmail} is not an attendee in this event.')
        return updatedEvent['attendees']
    except Exception as e:
        print(e)
        print(
            f'{attendeeEmail} was not removed successfully from event {eventId} as attendee')
        return False


def isEventLaterThan2050(event):
    # Directly obtain first 4 characters of date to get year
    startYear, endYear = int(event['start']['dateTime'][:4]), int(
        event['end']['dateTime'][:4])
    if startYear > 2050 or endYear > 2050:
        return True
    return False


def importEventFromJSON(api, eventJSON):
    '''
    Loads a JSON file in valid format and adds as event
    '''
    try:
        f = open(eventJSON)
        event = json.load(f)
        event = api.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: %s' % (event.get("htmlLink")))
        return True

    except FileNotFoundError as e:
        print(e)
        return "File not found"

    except json.JSONDecodeError as e:
        print(e)
        return "Incorrect JSON file format"

    except Exception as e:
        print(e)
        return "Event was not created successfully"
    
def exportEventToJson(api,eventId,exportDestination=None):
    '''
    Exports an event into JSON file. 
    '''    
    try:
        event = api.events().get(calendarId='primary', eventId=eventId).execute()
        fileName = '_'.join(event['summary'].split()) + ".json"

        if not exportDestination:
            path = fileName
        else:
            exportDestination = exportDestination.split("/")
            exportDestination.append(fileName)
            path = os.path.join(*exportDestination)

        with open(path,"w") as outfile:
            json.dump(event,outfile,indent=4)
        print(f"Event JSON file created at {path}")
        return path
    
    except FileNotFoundError:
        print("Directory not found")
        return False
        


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # events = get_upcoming_events(api, time_now, 10)
    events = get_all_events(api)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    temp = start_new_event(api)
    print(temp)


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
