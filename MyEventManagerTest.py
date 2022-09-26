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

"""
This method is used to simulate input to interact with the UI (this case is console)

This code is a modified version of similar code used for testing by FIT2085
"""


@contextmanager
def automatedInputOutput(inputList=[]):
    newIn, newOut = StringIO("\n".join(inputList)), StringIO()
    oldIn, oldOut = sys.stdin, sys.stdout
    try:
        sys.stdin, sys.stdout = newIn, newOut
        yield sys.stdin, sys.stdout
    finally:
        sys.stdin, sys.stdout = oldIn, oldOut


class MyEventManagerTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = MyEventManager.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # Add more test cases here

    """
    The following section is the test cases for the 'Event' feature
    ===|Event Section Start|======================================================================================
    """
    """
    The following is the template for the event object

    mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'gyon0004@student.monash.edu'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = ''
        mock_event.summary = 'yes'
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = mock_date
    """

    def test_add_event_info_valid_with_physical_location_and_using_yyyy_mm_dd_time_format(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {
                'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            # Assert that there are no items in the list of events
            self.assertEqual(0, len(running_application.event_list))
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Now check the contents of the input to see if it matches up
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(
            running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(
            running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "2023-09-24")
        self.assertEqual(running_application.event_list[0].end, "2023-09-25")
        # Add more tests if needed

    def test_add_event_info_valid_with_physical_location_and_using_dd_MON_yy_time_format(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {
                'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            # Assert that there are no items in the list of events
            self.assertEqual(0, len(running_application.event_list))
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Now check the contents of the input to see if it matches up
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(
            running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(
            running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "23-SEP-23")
        self.assertEqual(running_application.event_list[0].end, "24-SEP-23")
        # Add more tests if needed

    def test_add_event_info_valid_with_online_location(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {
                'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            # Assert that there are no items in the list of events
            self.assertEqual(0, len(running_application.event_list))
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Now check the contents of the input to see if it matches up
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location,
                         "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09")
        self.assertEqual(
            running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "2023-09-24")
        self.assertEqual(running_application.event_list[0].end, "2023-09-25")
        # Add more tests if needed

    def test_add_event_info_missing_event_name(self):
        # Dictating user input
        user_input = ["2", "Y",  "", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_missing_event_location(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_online_event_location(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "monash.zoom.us/j/84084382021?pwd=M1Y5UTlNQWZaRm5sQ0ZScXZpSjNSUT09",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_below_4_digits(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_above_5_digits(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340000",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_statecode_below_2_characters(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton V 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_statecode_above_3_characters(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VICT 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_start_time_format_dd_MON_yy(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "garretyong@gmail.com", "2023-SEP-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_start_time_format_yyyy_mm_dd(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "garretyong@gmail.com", "23-09-2023", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_dd_MON_yy(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "garretyong@gmail.com", "2023-09-24", "2023-SEP-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_yyyy_mm_dd(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "garretyong@gmail.com", "2023-09-24", "25-09-23"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {
                    'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                # Assert that there are no items in the list of events
                self.assertEqual(0, len(running_application.event_list))
                running_application.on_start()


class AddAttendeeTest(unittest.TestCase):
    def setUp(self):
        self.addFirstAttendeeTest = {'attendees': [{'email': 'jetyip123@hotmail.com', 
                                                    'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2022-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2022-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}
        self.addSecondAttendeeTest = {'attendees': [{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2022-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2022-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}
        self.maxAttendeeAmountTest = {'attendees': [{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                         {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2022-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2022-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}
        self.setEventLaterThan2050Test = {'attendees': [{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2051-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2052-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}

    def test_event_later_than_2050(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.setEventLaterThan2050Test
        self.assertEqual(False, MyEventManager.addAttendee(
            mock_api, eventId, 'jetyip123@hotmail.com'))

    def test_number_of_attendee_maxed(self):
        mock_api = MagicMock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.maxAttendeeAmountTest
        self.assertEqual(False, MyEventManager.addAttendee(
            mock_api, eventId, 'jetyip@hotmail.my'))

    def test_add_attendee(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.addFirstAttendeeTest
        initialAttendeeAmount = len(self.addFirstAttendeeTest['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.addSecondAttendeeTest
        self.assertEqual(initialAttendeeAmount+1, len(MyEventManager.addAttendee(
            mock_api, eventId, 'jetyip123@hotmail.com')))

class RemoveAttendeeTest(unittest.TestCase):
    def setUp(self): 
        self.addFirstAttendeeTest = {'attendees': [{'email': 'jetyip123@hotmail.com', 
                                                    'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2022-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2022-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}
        self.removeAttendeeTest = {'attendees': [],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2022-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2022-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}
        self.setEventLaterThan2050Test = {'attendees': [{'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}],
                                        'kind': 'calendar#event', 
                                      'etag': '"3328225280887000"', 
                                      'id': '5nj9311jsdhg2uq1tj1fqblaj8', 
                                      'status': 'confirmed',
                                      'htmlLink': 'https://www.google.com/calendar/event?eid=NW5qOTMxMWpzZGhnMnVxMXRqMWZxYmxhajgga3lpcDAwMDdAc3R1ZGVudC5tb25hc2guZWR1',
                                      'created': '2022-09-25T13:30:40.000Z', 
                                      'updated': '2022-09-25T13:30:40.491Z', 
                                      'summary': 'Monash Test 2',
                                      'location': '98 Shirley Street PIMPAMA QLD 4209', 
                                      'creator': {'email': 'kyip0007@student.monash.edu', 'self': True},
                                      'organizer': {'email': 'kyip0007@student.monash.edu', 'self': True}, 
                                      'start': {'dateTime': '2051-09-25T00:00:00+08:00', 'timeZone': 'Asia/Singapore'}, 
                                      'end': {'dateTime': '2052-09-26T08:00:00+08:00', 'timeZone': 'Asia/Singapore'},
                                      'iCalUID': '5nj9311jsdhg2uq1tj1fqblaj8@google.com', 
                                      'sequence': 0,
                                      'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 1440}]},
                                      'eventType': 'default'}

    
    def test_event_later_than_2050(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.setEventLaterThan2050Test
        self.assertEqual(False,MyEventManager.removeAttendee(mock_api,eventId,'jetyip123@hotmail.com'))


    def test_remove_non_attendee(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.addFirstAttendeeTest
        initialAttendeeAmount = len(self.addFirstAttendeeTest['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.addFirstAttendeeTest
        self.assertEqual(initialAttendeeAmount,len(MyEventManager.removeAttendee(mock_api,eventId,'jetyip@hotmail.com')))

    def test_remove_attendee(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.addFirstAttendeeTest
        initialAttendeeAmount = len(self.addFirstAttendeeTest['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.removeAttendeeTest
        self.assertEqual(initialAttendeeAmount-1,len(MyEventManager.removeAttendee(mock_api,eventId,'jetyip123@hotmail.com')))

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(AddAttendeeTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
