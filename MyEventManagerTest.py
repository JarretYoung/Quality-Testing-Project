import unittest
from unittest.mock import MagicMock, Mock, patch
import MyEventManager
# Add other imports here if needed
import importlib.util
import os.path
import sys
from contextlib import contextmanager
from io import StringIO

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
    
    def test_something_event_info_valid_info(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = '282poiu9aam6ed95vk57vncf6l'
        mock_event.summary = 'yes'
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = mock_date

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)

    def test_something_event_info_missing_id(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = None
        mock_event.summary = 'yes'
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = mock_date

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)

    def test_something_event_info_missing_name(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = '282poiu9aam6ed95vk57vncf6l'
        mock_event.summary = None
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = mock_date

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)
    
    def test_something_event_info_missing_location(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = '282poiu9aam6ed95vk57vncf6l'
        mock_event.summary = 'yes'
        mock_event.location = None
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = mock_date

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)
    
    def test_something_event_info_missing_atendees(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = '282poiu9aam6ed95vk57vncf6l'
        mock_event.summary = 'yes'
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = []
        mock_date.start = mock_date

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)

    def test_something_event_info_missing_date(self):
        mock_atendee1 = Mock()
        mock_atendee1.email = 'gyon0004@student.monash.edu'
        mock_atendee2 = Mock()
        mock_atendee2.email = 'garretyong@gmail.com'
        mock_date = Mock()
        mock_date.dateTime = '2022-09-22T13:30:00+08:00'
        mock_date.timeZone = 'Asia/Singapore'
        
        mock_event = Mock()
        mock_event.id = '282poiu9aam6ed95vk57vncf6l'
        mock_event.summary = 'yes'
        mock_event.location = 'https://monash.zoom.us/j/87386332422?pwd=NUtCeTV0Y0VqU3RRMDF0TjN1dlJCdz09'
        mock_event.attendees = [mock_atendee1, mock_atendee2]
        mock_date.start = None

        result = mock_event

        self.assertEqual(MyEventManager.check_input_function(result), True)
def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(MyEventManagerTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()