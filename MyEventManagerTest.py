<<<<<<< HEAD
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
    The following section is the test cases for the event creation feature
    ===|Event Creation Section Start|======================================================================================
    """
    
    def test_add_event_info_valid_with_physical_location_and_using_yyyy_mm_dd_time_format(self):
        # Dictating user input 
        user_input = ["2","Y","FIT2107 Assignment Test","123 Fake St. Clayton VIC 3400","1","gyon0004@student.monash.edu","2023-09-24","2023-09-25","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            mock_api.events.return_value.insert.return_value.execute.return_value = {'id':'282poiu9aam6ed95vk57vncf6l','creator':{'email':'gyon0004@student.monash.edu'},'organizer':{'email':'gyon0004@student.monash.edu'},'start':{'dateTime':'2023-09-24T09:00:00-07:00'},'end':{'dateTime':'2023-09-25T17:00:00-07:00'}}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2023-09-24T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2023-09-25T17:00:00-07:00")
        # Add more tests if needed

    def test_add_event_info_valid_with_physical_location_and_using_dd_MON_yy_time_format(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            mock_api.events.return_value.insert.return_value.execute.return_value = {'id':'282poiu9aam6ed95vk57vncf6l','creator':{'email':'gyon0004@student.monash.edu'},'organizer':{'email':'gyon0004@student.monash.edu'},'start':{'dateTime':'2023-09-24T09:00:00-07:00'},'end':{'dateTime':'2023-09-25T17:00:00-07:00'}}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2023-09-24T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2023-09-25T17:00:00-07:00")
        # Add more tests if needed

    def test_add_event_info_valid_with_online_location(self):
        # Dictating user input 
        user_input = ["2","Y", "FIT2107 Assignment Test", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            mock_api.events.return_value.insert.return_value.execute.return_value = {'id':'282poiu9aam6ed95vk57vncf6l','creator':{'email':'gyon0004@student.monash.edu'},'organizer':{'email':'gyon0004@student.monash.edu'},'start':{'dateTime':'2023-09-24T09:00:00-07:00'},'end':{'dateTime':'2023-09-25T17:00:00-07:00'}}
            time_now = '2022-09-24T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
            running_application.on_start()
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        # Now check the contents of the input to see if it matches up
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2023-09-24T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2023-09-25T17:00:00-07:00")
        # Add more tests if needed
        
    def test_add_event_info_missing_event_name(self):
        # Dictating user input 
        user_input = ["2","Y",  "", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()
    
    def test_add_event_info_missing_event_location(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()
        
    def test_add_event_info_invalid_online_event_location(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "monash.zoom.us/j/84084382021?pwd=M1Y5UTlNQWZaRm5sQ0ZScXZpSjNSUT09", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_below_4_digits(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_postcode_above_5_digits(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 340000", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()
    
    def test_add_event_info_invalid_physical_event_location_invalid_statecode_below_2_characters(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton V 3400", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_physical_event_location_invalid_statecode_above_3_characters(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VICT 3400", "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()
    
    def test_add_event_info_invalid_start_time_format_dd_MON_yy(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com", "2023-SEP-24", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_start_time_format_yyyy_mm_dd(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com", "23-09-2023", "2023-09-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_dd_MON_yy(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com", "2023-09-24", "2023-SEP-25","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()

    def test_add_event_info_invalid_end_time_format_yyyy_mm_dd(self):
        # Dictating user input 
        user_input = ["2","Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "1", "garretyong@gmail.com", "2023-09-24", "25-09-23","e"]
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            # Simulating user input
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.return_value.list.return_value.execute.return_value = {'items': []}
                time_now = '2022-09-24T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                # Ensure that the lists of events is completely empty for comparison later
                self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
                running_application.on_start()
    """
    The following section is the test cases for the event creation feature
    ===|Event Creation Section End|======================================================================================
    """

    """
    The following section is the test cases for the event deletion feature
    ===|Event Delete Section Start|======================================================================================
    """
    def test_delete_valid_tasks_via_application_UI(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        
        # Dictating user input 
        user_input = ["3","1","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            # Adding 2 events to event_list
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)            
            running_application.on_start()
            
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        self.assertEqual(0, len(running_application.archived_event_list))   # Assert the deleted event is not stored in the archived event list
        # Now check the infomation of last remaining item
        self.assertEqual(running_application.event_list[0].id, "8k6giqb8k2ck6po83pbof50sip")
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.event_list[0].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

    def test_delete_invalid_tasks_via_direct_input_to_method(self):
        # Background: You can only delete/ cancel events that have already passed 
        with self.assertRaises(ValueError):
            mock_api = MagicMock()
            fake_event_id = '8k6giqb8k2ck6po83pbof50sip'
            invalid_date_input = '2022-09-29T09:00:00-07:00'    # Invalid because this event has not passed (this_date > current_date)
            fake_current_date = '2022-09-15T17:00:00-07:00'     
            MyEventManager.delete_existing_event(mock_api, fake_event_id, invalid_date_input, fake_current_date)

    """
    ===|Event Delete Section End|======================================================================================
    """

    """
    The following section is the test cases for the event deletion feature
    ===|Event Cancel Section Start|======================================================================================
    """
    def test_cancel_valid_tasks_via_application_UI(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["4","1","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            # Adding 2 events to event_list
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.archived_event_list))   # Assert the deleted event is stored in the archived event list
        # Now check the infomation of last remaining item
        self.assertEqual(running_application.event_list[0].id, "8k6giqb8k2ck6po83pbof50sip")
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.event_list[0].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

        # Now check the information of the 
        self.assertEqual(running_application.archived_event_list[0].id, "7k6giqb8k7ck6po83pbof50sij")
        self.assertEqual(running_application.archived_event_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(running_application.archived_event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.archived_event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.archived_event_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.archived_event_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")
        
    """
    ===|Event Cancel Section End|======================================================================================
    """
    

    """
    The following section is the test cases for the event deletion feature
    ===|Event Restore Section Start|======================================================================================
    """
    def test_restore_task(self):
        # Dictating user input 
        user_input = ["6","1","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {'items': []}
            mock_api.events.return_value.insert.return_value.execute.return_value = {'id':'282poiu9aam6ed95vk57vncf6l','creator':{'email':'gyon0004@student.monash.edu'},'organizer':{'email':'gyon0004@student.monash.edu'},'start':{'dateTime':'2022-09-14T09:00:00-07:00'},'end':{'dateTime':'2022-09-15T17:00:00-07:00'}}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            test_event_1 = Event("7k6giqb8k7ck6po83pbof50sij", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "gyon0004@student.monash.edu", "gyon0004@student.monash.edu", [{'email':'gyon0004@student.monash.edu'}], {'dateTime':'2022-09-14T09:00:00-07:00'},{'dateTime':'2022-09-15T17:00:00-07:00'})
            running_application.archived_event_list.append(test_event_1)
            # Ensure that the lists of events is completely empty for comparison later
            self.assertEqual(0, len(running_application.event_list))    # Assert that there are no items in the list of events
            self.assertEqual(1, len(running_application.archived_event_list))    # Assert that there is 1 items in the archived list of events
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.event_list))    # Assert that there is now 1 item in the list of events
        self.assertEqual(0, len(running_application.archived_event_list))   # Assert the deleted event is stored in the archived event list
        # Now check the infomation of last remaining item
        self.assertEqual(running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.event_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.event_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")
        # Add more tests if needed
        
    """
    ===|Event Restore Section End|======================================================================================
    """


    """
    The following section is the test cases for the event deletion feature
    ===|Event Navigation Query Section Start|======================================================================================
    """
    def test_query_no_event_matching_query(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","1","No Event with This name","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        self.assertEqual(0, len(running_application.query_events_list))    # Assert that there is now 0 item in the list of queried events
    
    
    def test_query_valid_full_name_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","1","FIT2107 Assignment Test Invalid","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.query_events_list[0].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed
        
    def test_query_valid_keyword_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","2","Invalid","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.query_events_list[0].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

    def test_query_valid_start_year_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","3","2022","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(2, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(running_application.query_events_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")

        self.assertEqual(running_application.query_events_list[1].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.query_events_list[1].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.query_events_list[1].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[1].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[1].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

    def test_query_valid_start_date_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","4","2022-09-14","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(running_application.query_events_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")
        # Add more tests if needed

    def test_query_invalid_start_date_event_by_inputting_dd_mm_yyyy_format(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","4","29-09-2022","e"]
        # Simulating user input
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
                time_now = '2022-09-20T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                running_application.on_start()
        
    
    def test_query_valid_end_year_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","5","2022","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(2, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(running_application.query_events_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")

        self.assertEqual(running_application.query_events_list[1].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.query_events_list[1].location, "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(running_application.query_events_list[1].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[1].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[1].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

    def test_query_valid_end_date_event(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","6","2022-09-15","e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()
        
        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        self.assertEqual(1, len(running_application.query_events_list))    # Assert that there is now 1 item in the list of queried events
        
        # Now check the infomation of queried item(s)
        self.assertEqual(running_application.query_events_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(running_application.query_events_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(running_application.query_events_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(running_application.query_events_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(running_application.query_events_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")
        # Add more tests if needed

    def test_query_invalid_end_date_event_by_inputting_dd_mm_yyyy_format(self):
        test_event_1 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'7k6giqb8k7ck6po83pbof50sij',
            'summary':'FIT2107 Assignment Test Valid',
            'description':'This is a test',
            'location':'123 Fake St. Clayton VIC 3400',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-14T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-15T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }

        test_event_2 = {
            'kind':'calendar#event',
            'etag':'"3327475922566000"',
            'id':'8k6giqb8k2ck6po83pbof50sip',
            'summary':'FIT2107 Assignment Test Invalid',
            'description':'This is a test',
            'location':'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'organizer':{
                'email':'gyon0004@student.monash.edu',
                'self':True
            },
            'start':{
                'dateTime':'2022-09-29T09:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'end':{
                'dateTime':'2022-09-30T17:00:00-07:00',
                'timeZone':'Asia/Singapore'
            },
            'attendees':[
                {
                    'email':'gyon0004@student.monash.edu',
                    'organizer':True,
                    'self':True,
                    'responseStatus':'accepted'
                }
            ]
        }
        
        # Dictating user input 
        user_input = ["7","6","29-09-2022","e"]
        # Simulating user input
        # Invalid input should have prompted an ValueError to be raised 
        with self.assertRaises(ValueError):
            with automatedInputOutput(user_input) as (inGen, outGen):
                mock_api = MagicMock()
                mock_api.events.return_value.list.return_value.execute.return_value = {'items' : [test_event_1, test_event_2]}
                time_now = '2022-09-20T03:29:17.380207Z'
                running_application = Application(mock_api, time_now)
                running_application.on_start()

    """
    ===|Event Navigation Query Section End|======================================================================================
    """

        
    
def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()
=======
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
from googleapiclient.errors import HttpError

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
    The following section is the test cases for the event creation feature
    ===|Event Creation Section Start|======================================================================================
    """

    def test_add_event_info_valid_with_physical_location_and_using_yyyy_mm_dd_time_format(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start, "2023-09-24T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end, "2023-09-25T17:00:00-07:00")
        # Add more tests if needed

    def test_add_event_info_valid_with_physical_location_and_using_dd_MON_yy_time_format(self):
        # Dictating user input
        user_input = ["2", "Y",  "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start, "2023-09-24T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end, "2023-09-25T17:00:00-07:00")
        # Add more tests if needed

    def test_add_event_info_valid_with_online_location(self):
        # Dictating user input
        user_input = ["2", "Y", "FIT2107 Assignment Test", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start, "2023-09-24T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end, "2023-09-25T17:00:00-07:00")
        # Add more tests if needed

    def test_add_event_info_missing_event_name(self):
        # Dictating user input
        user_input = ["2", "Y",  "", "https://monash.zoom.us/j/82612757952?pwd=K3RjcVc5bUtwYm9GZ3REb290eG9NZz09",
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "gyon0004@student.monash.edu", "2023-09-24", "2023-09-25", "e"]
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
                      "1", "garretyong@gmail.com", "2023-SEP-24", "2023-09-25", "e"]
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
                      "1", "garretyong@gmail.com", "23-09-2023", "2023-09-25", "e"]
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
                      "1", "garretyong@gmail.com", "2023-09-24", "2023-SEP-25", "e"]
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
                      "1", "garretyong@gmail.com", "2023-09-24", "25-09-23", "e"]
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
    """
    The following section is the test cases for the event creation feature
    ===|Event Creation Section End|======================================================================================
    """

    """
    The following section is the test cases for the event deletion feature
    ===|Event Delete Section Start|======================================================================================
    """

    def test_delete_valid_tasks_via_application_UI(self):
        test_event_1 = {
            'kind': 'calendar#event',
            'etag': '"3327475922566000"',
            'id': '7k6giqb8k7ck6po83pbof50sij',
            'summary': 'FIT2107 Assignment Test Valid',
            'description': 'This is a test',
            'location': '123 Fake St. Clayton VIC 3400',
            'creator': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'organizer': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'start': {
                'dateTime': '2022-09-14T09:00:00-07:00',
                'timeZone': 'Asia/Singapore'
            },
            'end': {
                'dateTime': '2022-09-15T17:00:00-07:00',
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

        test_event_2 = {
            'kind': 'calendar#event',
            'etag': '"3327475922566000"',
            'id': '8k6giqb8k2ck6po83pbof50sip',
            'summary': 'FIT2107 Assignment Test Invalid',
            'description': 'This is a test',
            'location': 'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'organizer': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'start': {
                'dateTime': '2022-09-29T09:00:00-07:00',
                'timeZone': 'Asia/Singapore'
            },
            'end': {
                'dateTime': '2022-09-30T17:00:00-07:00',
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

        # Dictating user input
        user_input = ["3", "1", "e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            # Adding 2 events to event_list
            mock_api.events.return_value.list.return_value.execute.return_value = {
                'items': [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Assert the deleted event is not stored in the archived event list
        self.assertEqual(0, len(running_application.archived_event_list))
        # Now check the infomation of last remaining item
        self.assertEqual(
            running_application.event_list[0].id, "8k6giqb8k2ck6po83pbof50sip")
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.event_list[0].location,
                         "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

    def test_delete_existing_event_function_in_MyEventManager_invalid_input(self):

        pass
        # Check event list
        # check archive

    """
    ===|Event Delete Section End|======================================================================================
    """

    """
    The following section is the test cases for the event deletion feature
    ===|Event Cancel Section Start|======================================================================================
    """

    def test_cancel_valid_tasks_via_application_UI(self):
        test_event_1 = {
            'kind': 'calendar#event',
            'etag': '"3327475922566000"',
            'id': '7k6giqb8k7ck6po83pbof50sij',
            'summary': 'FIT2107 Assignment Test Valid',
            'description': 'This is a test',
            'location': '123 Fake St. Clayton VIC 3400',
            'creator': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'organizer': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'start': {
                'dateTime': '2022-09-14T09:00:00-07:00',
                'timeZone': 'Asia/Singapore'
            },
            'end': {
                'dateTime': '2022-09-15T17:00:00-07:00',
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

        test_event_2 = {
            'kind': 'calendar#event',
            'etag': '"3327475922566000"',
            'id': '8k6giqb8k2ck6po83pbof50sip',
            'summary': 'FIT2107 Assignment Test Invalid',
            'description': 'This is a test',
            'location': 'https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09',
            'creator': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'organizer': {
                'email': 'gyon0004@student.monash.edu',
                'self': True
            },
            'start': {
                'dateTime': '2022-09-29T09:00:00-07:00',
                'timeZone': 'Asia/Singapore'
            },
            'end': {
                'dateTime': '2022-09-30T17:00:00-07:00',
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

        # Dictating user input
        user_input = ["4", "1", "e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            # Adding 2 events to event_list
            mock_api.events.return_value.list.return_value.execute.return_value = {
                'items': [test_event_1, test_event_2]}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            running_application.on_start()

        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Assert the deleted event is stored in the archived event list
        self.assertEqual(1, len(running_application.archived_event_list))
        # Now check the infomation of last remaining item
        self.assertEqual(
            running_application.event_list[0].id, "8k6giqb8k2ck6po83pbof50sip")
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test Invalid")
        self.assertEqual(running_application.event_list[0].location,
                         "https://monash.zoom.us/j/5863187297?pwd=RDNBZzNmZDlySy9KYk5KbzNLU3hnQT09")
        self.assertEqual(
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start['dateTime'], "2022-09-29T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end['dateTime'], "2022-09-30T17:00:00-07:00")
        # Add more tests if needed

        # Now check the information of the
        self.assertEqual(
            running_application.archived_event_list[0].id, "7k6giqb8k7ck6po83pbof50sij")
        self.assertEqual(
            running_application.archived_event_list[0].summary, "FIT2107 Assignment Test Valid")
        self.assertEqual(
            running_application.archived_event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(
            running_application.archived_event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.archived_event_list[0].start['dateTime'], "2022-09-14T09:00:00-07:00")
        self.assertEqual(
            running_application.archived_event_list[0].end['dateTime'], "2022-09-15T17:00:00-07:00")

    """
    ===|Event Cancel Section End|======================================================================================
    """

    """
    The following section is the test cases for the event deletion feature
    ===|Event Restore Section Start|======================================================================================
    """

    def test_restore_task(self):
        # Dictating user input
        user_input = ["6", "1", "e"]
        # Simulating user input
        with automatedInputOutput(user_input) as (inGen, outGen):
            mock_api = MagicMock()
            mock_api.return_value.list.return_value.execute.return_value = {
                'items': []}
            time_now = '2022-09-20T03:29:17.380207Z'
            running_application = Application(mock_api, time_now)
            test_event_1 = Event("7k6giqb8k7ck6po83pbof50sij", "FIT2107 Assignment Test", "123 Fake St. Clayton VIC 3400", "gyon0004@student.monash.edu",
                                 "gyon0004@student.monash.edu", [{'email': 'gyon0004@student.monash.edu'}], "2022-09-14T09:00:00-07:00", "2022-09-15T17:00:00-07:00")
            running_application.archived_event_list.append(test_event_1)
            # Ensure that the lists of events is completely empty for comparison later
            # Assert that there are no items in the list of events
            self.assertEqual(0, len(running_application.event_list))
            # Assert that there is 1 items in the archived list of events
            self.assertEqual(1, len(running_application.archived_event_list))
            running_application.on_start()

        # At this point, user input has been inputted and a new event has been added
        # Check (and sort of compare) if there is a new item in the list right now
        # Assert that there is now 1 item in the list of events
        self.assertEqual(1, len(running_application.event_list))
        # Assert the deleted event is stored in the archived event list
        self.assertEqual(0, len(running_application.archived_event_list))
        # Now check the infomation of last remaining item
        self.assertEqual(
            running_application.event_list[0].summary, "FIT2107 Assignment Test")
        self.assertEqual(
            running_application.event_list[0].location, "123 Fake St. Clayton VIC 3400")
        self.assertEqual(
            running_application.event_list[0].attendees[0]['email'], "gyon0004@student.monash.edu")
        self.assertEqual(
            running_application.event_list[0].start, "2022-09-14T09:00:00-07:00")
        self.assertEqual(
            running_application.event_list[0].end, "2022-09-15T17:00:00-07:00")
        # Add more tests if needed

    """
    ===|Event Restore Section End|======================================================================================
    """


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
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
                                                    {'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'}, {
                                                        'email': 'jetyip123@hotmail.com', 'responseStatus': 'needsAction'},
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
        self.assertEqual(False, MyEventManager.removeAttendee(
            mock_api, eventId, 'jetyip123@hotmail.com'))

    def test_remove_non_attendee(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.addFirstAttendeeTest
        initialAttendeeAmount = len(self.addFirstAttendeeTest['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.addFirstAttendeeTest
        self.assertEqual(initialAttendeeAmount, len(
            MyEventManager.removeAttendee(mock_api, eventId, 'jetyip@hotmail.com')))

    def test_remove_attendee(self):
        mock_api = Mock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.addFirstAttendeeTest
        initialAttendeeAmount = len(self.addFirstAttendeeTest['attendees'])
        mock_api.events.return_value.patch.return_value.execute.return_value = self.removeAttendeeTest
        self.assertEqual(initialAttendeeAmount-1, len(
            MyEventManager.removeAttendee(mock_api, eventId, 'jetyip123@hotmail.com')))

class ImportEventTest(unittest.TestCase):
    def test_when_file_not_found(self):
        mock_api = Mock
        file= "importTest/newEvent.json"
        self.assertEqual("File not found",MyEventManager.importEventFromJSON(mock_api,file))
    
    def test_import_event__with_file_that_is_not_in_proper_JSON_format(self):
        """
        Tests if file has proper JSON syntax to allow the import to be successful
        """
        mock_api = Mock()
        file = "importTest/invalidJsonFormat.json"
        self.assertEqual("Incorrect JSON file format",MyEventManager.importEventFromJSON(mock_api,file))
        
class ExportEventTest(unittest.TestCase):
    def setUp(self) :
        self.setExportEventTest = {'attendees': [{'email': 'jetyip123@hotmail.com',
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
        
    def test_exporting_event_to_directory(self):
        mock_api = MagicMock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.setExportEventTest
        path = MyEventManager.exportEventToJson(mock_api,eventId)
        self.assertTrue(os.path.exists(path))
        os.remove('Monash_Test_2.json')
        
    def test_non_existent_directory(self):
        mock_api = MagicMock()
        eventId = '5nj9311jsdhg2uq1tj1fqblaj8'
        mock_api.events.return_value.get.return_value.execute.return_value = self.setExportEventTest
        self.assertFalse(MyEventManager.exportEventToJson(mock_api,eventId,"DirectoryDoesNotExist"))

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(ExportEventTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
>>>>>>> import-export
