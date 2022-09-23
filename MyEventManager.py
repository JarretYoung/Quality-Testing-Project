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
from datetime import *
import datetime
import re
import pickle
import classes
from classes import *
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
        raise ValueError("Attendee {number}'s email is invalid".format(number=attendee_number + 1))



def check_event_input(event: Event, summary, location, attendees, start_date, end_date):
    def check_event_input(summary, location, attendees, start_date, end_date):
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
            if (len(location_in_list_form[-1]) < 4) or (
                    len(location_in_list_form[-1]) > 5):  # 4 <= len(postal_code) <= 5
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
        MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
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
                for i in range(MONTHS):
                    if date_as_list[1] == MONTHS[i]:
                        month = i + 1
                # If month was not identified, assume that input was of wrong format; else reconstruct date
                if month == 0:
                    raise ValueError(
                        "Start Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
                else:
                    start_date = '{day}-{MONTH}-{year}'.format(day=date_as_list[0], MONTH=month, year=date_as_list[2])
                # Test if date is of acceptable format using datetime package
                try:
                    datetime.datetime.strptime(start_date, '%d-%M-%y')
                except ValueError:
                    raise ValueError(
                        "Start Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")

        if end_date == "" or end_date == None:
            raise ValueError('Event must have an end date')
        # Add check for time format
        MONTHS = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        try:
            # Checking for yyyy-mm-dd format
            datetime.datetime.strptime(end_date, '%Y-%M-%d')
        except ValueError:
            date_as_list = end_date.split("-")
            try:
                # Checking if overall formatting is correct ex: using '/' instead of '-' to separate the date
                temp = date_as_list[-2]
            except IndexError:
                raise ValueError("End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
            else:
                # Assuming input is following dd-MON-yy
                month = 0
                # Identifying which month was inputted based on the MONTHS list above
                for i in range(MONTHS):
                    if date_as_list[1] == MONTHS[i]:
                        month = i + 1
                # If month was not identified, assume that input was of wrong format; else reconstruct date
                if month == 0:
                    raise ValueError(
                        "End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")
                else:
                    end_date = '{day}-{MONTH}-{year}'.format(day=date_as_list[0], MONTH=month, year=date_as_list[2])
                # Test if date is of acceptable format using datetime package
                try:
                    datetime.datetime.strptime(end_date, '%d-%M-%y')
                except ValueError:
                    raise ValueError(
                        "End Date must follow the yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format")


def start_new_event(api):
    organiser_status = None
    while organiser_status == None:
        organiser_confirmation = input("Are you the organiser? Y/N : ")
        if organiser_confirmation.upper() == 'Y':
            organiser_status = True
        elif organiser_confirmation.upper() == 'N':
            organiser_status = False

    summary = input("Insert Event Name : ")

    location = input("Insert location of event : ")

    list_of_attendees = []
    number_of_attendees = input("Please enter the number of attendees : ")
    for i in range(int(number_of_attendees)):
        email = input("Input attendee " + str(i + 1) + "'s email : ")
        attendee = {'email': '{email_to_insert}'.format(email_to_insert=email)}
        list_of_attendees.append(attendee)

    start_date = input("Insert a start date : ")
    start = '{date}T09:00:00-07:00'.format(date=start_date)

    end_date = input("Insert a end date : ")
    end = '{date}T17:00:00-07:00'.format(date=end_date)

    check_event_input(summary, location, list_of_attendees, start_date, end_date)

    event = Event(summary, location, list_of_attendees, start, end)

    event_output = api.events().insert(calendarId='primary', body=event.get_JSON_format()).execute()

    if event_output['id'] != None:
        event.add_id(event_output['id'])

    return event_output


def organiser_info(event_id):

    event = get_calendar_api().events().get(calendarId='primary', eventId=event_id).execute()
    organiser = event['organizer']['email']
    return organiser


def check_is_organiser(user, event_id):
    # user = input("Please enter your email")
    if user == organiser_info(event_id):
        return True
    return False


def create_event():
    user = input("Please enter your email (abc@email.com) :")
    if check_is_organiser(user):
        event_body = start_new_event()
        new_event_create = get_calendar_api().events().insert(calendarId='primary', body=event_body).execute()
        return new_event_create
    else:
        print('Only organiser can create an event')


def update_event(eventId):
    user = input("Please enter your email and id (abc@email.com) :")

    if check_is_organiser(user):
        # retrieve the event from the API.
        event = get_calendar_api().events().get(calendarId='primary', eventId=eventId).execute()

        start_date = input("Insert a start date")
        check_date_start = start_date.split('-')
        if (len(check_date_start[0]) == 4 and check_date_start[0] <2050) or len(check_date_start[0]) == 2 and  check_date_start[2] < 50 :
            start = '{date}T09:00:00-07:00'.format(date=start_date)
        else:
            raise ValueError('No later than 2050')

        end_date = input("Insert a end date")
        check_date_end = end_date.split('-')
        if (len(check_date_end[0]) == 4 and check_date_end[0] < 2050) or len(check_date_end[0]) == 2 and \
                check_date_end[2] < 50:
            end = '{date}T17:00:00-07:00'.format(time=end_date)
        else:
            raise ValueError('No later than 2050')

        event['summary'] = input("Insert your event summary: ")
        event['start']['dateTime'] = start
        event['end']['dateTime'] = end

        updated_event = get_calendar_api().events().patch(calendarId='primary', eventId=event['id'], body=event).execute()


def change_event_owner(event_id):
    user = input("Please enter your email and id (abc@email.com) :")
    if check_is_organiser(user,event_id):
        # retrieve the event from the API.
        new_destination = input("Please the gmail of the new organiser: ")
        updated_event = get_calendar_api().events().move(calendarId='primary', eventId=event_id, destination=new_destination).execute()
        print(updated_event['updated'])

        # return updated_event['updated']

def modify_attendees(event_id,act,attendees_email ):

    # if check_is_organiser():
    event = get_calendar_api().events().get(calendarId='primary', eventId=event_id).execute()

    attendees = event['attendees']
    if act == 'delete':
        count = 0
        while count < len(attendees):
            if attendees[count] ['email'] == attendees_email:
                del(attendees[count] ['email'])
            else:
                count += 1

    elif act == 'add':
        attendees.append({'email': attendees_email})

    elif act == 'add':
        attendees.append({'email': attendees_email})
    updated_event = get_calendar_api().events().patch(calendarId='primary', eventId=event_id,body=event).execute()



def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = get_upcoming_events(api, time_now, 10)
    print(events)

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    # main()
    # event = get_calendar_api().events().get(calendarId='primary', eventId='2i7qq93nkg53jsg98porpvts7i').execute()
    # # a =change_event_owner('2i7qq93nkg53jsg98porpvts7i')
    # print(a)
    # event['summary'] = 'lunch'
    # event['end'] = {'dateTime': '2027-03-06T00:30:00+11:00', 'timeZone': 'Australia/Sydney'}
    # updated_event = get_calendar_api().events().patch(calendarId='primary', eventId='2i7qq93nkg53jsg98porpvts7i', body = event).execute()
    # print(updated_event)

    # a = [1,2,3,4,5,5]
    # item = 5
    # count = 0
    # while count < len(a):
    #     if a[count] == item:
    #         del(a[count])
    #     else:
    #         count += 1
    # print(a)