import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
# Add other imports here if needed
import importlib.util
import os.path
import sys
from contextlib import contextmanager
from io import StringIO
from application import Application
"""
This method is used to simulate input to interact with the UI (this case is console)
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
        mock_atendee2.email = 'garretyong@gmail.com'
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
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0,
                             len(running_application.event_list))  # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1,
                         len(running_application.event_list))  # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "2023-09-24")
        self.assertEqual(running_application.event_list[0].end, "2023-09-25")
        # Add more tests if needed

    def test_add_event_info_valid_with_physical_location_and_using_dd_MON_yy_time_format(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0,
                             len(running_application.event_list))  # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1,
                         len(running_application.event_list))  # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "23-SEP-23")
        self.assertEqual(running_application.event_list[0].end, "24-SEP-23")
        # Add more tests if needed

    def test_add_event_info_valid_with_online_location(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test",
                      "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0,
                             len(running_application.event_list))  # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1,
                         len(running_application.event_list))  # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location,
                         "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09")
        self.assertEqual(running_application.event_list[0].attendee[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start, "2023-09-24")
        self.assertEqual(running_application.event_list[0].end, "2023-09-25")
        # Add more tests if needed

    def test_add_event_info_missing_event_name(self):
        # Dictating user input
        user_input = ["2", "Y", "", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_missing_event_location(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "", "1", "gyon0004@student.monash.edu", "2023-09-24",
                      "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_online_event_location(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test",
                      "monash.zoom.us/j/84084382021?pwd=M1Y5UTlNQWZaRm5sQ0ZScXZpSjNSUT09", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_below_4_digits(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_above_5_digits(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340000", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_statecode_below_2_characters(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton V 3400", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_statecode_above_3_characters(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VICT 3400", "1",
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_start_time_format_dd_MON_yy(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com",
                      "2023-SEP-24", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_start_time_format_yyyy_mm_dd(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com",
                      "23-09-2023", "2023-09-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_dd_MON_yy(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com",
                      "2023-09-24", "2023-SEP-25"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_yyyy_mm_dd(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com",
                      "2023-09-24", "25-09-23"]
        # Invalid input should have prompted an ValueError to be raised
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0,
                                 len(running_application.event_list))  # Assert that there are no items in the list of events
                running_application.on_start()

    # def test_create_event_by_organiser(self):
    #     api = MyEventManager.get_calendar_api()
    #     existing_event = api.events().get(calendarId='primary', eventId='2i7qq93nkg53jsg98porpvts7i').execute()
    #     even_new = MyEventManager.create_event_by_organiser('2i7qq93nkg53jsg98porpvts7i')

    def test_create_event_on_behalf_others_organiser(self):
        user_input = ["8","Y","FIT2107 Assignment Test","123 Fake St. Clayton VIC 3400","1","gyon0004@student.monash.edu","2023-09-24","2023-09-25",'bishan0420@gmail.com',"e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            self.assertEqual(running_application.event_list[0].organiser, 'bcho0029@student.monash.edu')
            running_application.on_start()

        self.assertEqual(running_application.event_list[0].organiser, 'bishan0420@gmail.com')
        self.assertNotEqual(running_application.event_list[0].creator,running_application.event_list[0].organiser )

    def test_create_event_on_behalf_others_not_organiser(self):
        user_input = ["8","Y","FIT2107 Assignment Test","123 Fake St. Clayton VIC 3400","1","gyon0004@student.monash.edu","2023-09-24","2023-09-25",'bishan0420@gmail.com',"e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # self.assertNotEqual(running_application.event_list[0].organiser, 'acc1234@student.monash.edu')
            self.assertRaises(IndexError, running_application.on_start())

            # running_application.on_start()

        # raise the error asssert
        # self.assertEqual(running_application.event_list[0].creator, running_application.event_list[0].organiser)

    def test_organiser_update_with_valid_date_using_dd_MON_yy_time_format(self):

        # set the existing event in the calendar
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
            ]
        }

        user_input = ["5", '2', '1', "bcho0029@student.monash.edu", "2023-11-24", "2023-11-25", 'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # self.assertNotEqual(running_application.event_list[0].organiser, 'acc1234@student.monash.edu')
            running_application.on_start()

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        new_start_date ='2023-11-24T09:00:00-07:00'
        new_end_date = '2023-11-25T17:00:00-07:00'

        self.assertNotEqual(running_application.event_list[0].start['dateTime'],ori_start_date)
        self.assertNotEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertEqual(running_application.event_list[0].start['dateTime'],new_start_date)
        self.assertEqual(running_application.event_list[0].start['dateTime'], new_end_date)


    def test_organiser_update_with_valid_date_using_yy_MON_dd_time_format(self):
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
            ]
        }

        user_input = ["5", '2','1', "bcho0029@student.monash.edu", "24-11-24", "24-11-25",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # self.assertNotEqual(running_application.event_list[0].organiser, 'acc1234@student.monash.edu')
            running_application.on_start()

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        new_start_date = '2024-11-24T09:00:00-07:00'
        new_end_date = '2024-11-25T17:00:00-07:00'

        self.assertNotEqual(running_application.event_list[0].start['dateTime'],ori_start_date)
        self.assertNotEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertEqual(running_application.event_list[0].start['dateTime'],new_start_date)
        self.assertEqual(running_application.event_list[0].start['dateTime'], new_end_date)


    def test_organiser_update_with_not_valid_date_2050(self):
        # set the existing event in the calendar
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
            ]
        }

        user_input = ["5", '2', "1", "bcho0029@student.monash.edu", "2050-11-24", "2050-11-25",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # self.assertNotEqual(running_application.event_list[0].organiser, 'acc1234@student.monash.edu')
            running_application.on_start()
            # self.assertRaises(lambda : running_application.event_list[0])

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        expected_new_start_date ='2050-11-24T09:00:00-07:00'
        expected_new_end_date = '2050-11-25T17:00:00-07:00'

        self.assertEqual(running_application.event_list[0].start['dateTime'],ori_start_date)
        self.assertEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'],expected_new_start_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_end_date)

    def test_organiser_update_with_not_valid_date_2001(self):
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
            ]
        }

        user_input = ["5", '1', "1", "bcho0029@student.monash.edu", "2001-11-24", "2001-11-25",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        expected_new_start_date = '2001-11-24T09:00:00-07:00'
        expected_new_end_date = '2001-11-25T17:00:00-07:00'

        self.assertEqual(running_application.event_list[0].start['dateTime'], ori_start_date)
        self.assertEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_start_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_end_date)

    def test_not_organiser_update_with_not_valid_date_2050(self):
        # set the existing event in the calendar
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
            ]
        }

        user_input = ["5", '1', "1", "abc1234@student.monash.edu", "2050-11-24", "2050-11-25", 'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # self.assertNotEqual(running_application.event_list[0].organiser, 'acc1234@student.monash.edu')
            running_application.on_start()

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        expected_new_start_date = '2050-11-24T09:00:00-07:00'
        expected_new_end_date = '2050-11-25T17:00:00-07:00'

        self.assertNotEqual(running_application.event_list[0].organiser['email'],'abc1234@student.monash.edu')
        self.assertEqual(running_application.event_list[0].start['dateTime'], ori_start_date)
        self.assertEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_start_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_end_date)

    def test_not_organiser_update_with_valid_date_2001(self):
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
            ]
        }

        user_input = ["5", '2', "1", "bcho0029@student.monash.edu", "2001-11-24", "2001-11-25", 'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        ori_start_date = '2023-09-14T09:00:00-07:00'
        ori_end_date = '2023-09-15T17:00:00-07:00'
        expected_new_start_date = '2001-11-24T09:00:00-07:00'
        expected_new_end_date = '2001-11-25T17:00:00-07:00'

        self.assertNotEqual(running_application.event_list[0].organiser['email'], 'abc1234@student.monash.edu')
        self.assertEqual(running_application.event_list[0].start['dateTime'], ori_start_date)
        self.assertEqual(running_application.event_list[0].end['dateTime'], ori_end_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_start_date)
        self.assertNotEqual(running_application.event_list[0].start['dateTime'], expected_new_end_date)
        pass

    def test_organiser_change_event_owner(self):
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
            ]
        }
        user_input = ["5", '4', "1", "bcho0029@student.monash.edu", "biannyzj0506@gmailcom",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        self.assertEqual("biannyzj0506@gmailcom", running_application.event_list[0].organiser['email'])

    def test_not_organiser_change_event_owner(self):
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
            ]
        }
        user_input = ["5", '4', "1", "abc1234@student.monash.edu","biannyzj0506@gmailcom",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        self.assertNotEqual(running_application.event_list[0].organiser['email'], "biannyzj0506@gmailcom")

    def organiser_dlt_attendees(self):
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
            ]
        }

        user_input = ["5", "5", "1", "bcho0029@student.monash.edu", "delete", "1"
                      "gyon0004@student.monash.edu", 'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        self.assertEqual(len(running_application.event_list[0].attendees), 0)

    def not_organiser_dlt_attendees(self):
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
            ]
        }

        user_input = ["5", "5", "1", "bcho1234@student.monash.edu", "delete", "1", "gyon0004@student.monash.edu",'e']  # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        self.assertEqual(len(running_application.event_list[0].attendees), 1)
        self.assertEqual(running_application.event_list[0].attendees['email'], "gyon0004@student.monash.edu")


    def not_organiser_add_no_attendees(self):
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
            ]
        }
        user_input = ["5", "5", "1", "bcho1234@student.monash.edu", "delete", "1", "e"]  # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        self.assertEqual(len(running_application.event_list[0].attendees), 1)
        self.assertEqual(running_application.event_list[0].attendees['email'], "gyon0004@student.monash.edu")

    def organiser_add_attendees(self):
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
            ]
        }

        user_input = ["5", "5", "1", "bcho0029@student.monash.edu", "add", "1", "bishan.choo04@gmail",'e']
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        self.assertEqual(len(running_application.event_list[0].attendees), 2)
        self.assertEqual(running_application.event_list[0].attendees['email'], "bishan.choo04@gmail")

    def test_reminder_no_set(self):
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
        user_input = ["9", "1", "e"]
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items': [test_event_1]}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        # self.assertTrue(running_application.event_list[0].reminders)
        self.assertFalse(running_application.event_list[0].reminders)



def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
