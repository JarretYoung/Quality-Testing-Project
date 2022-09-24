from MyEventManager import *
from classes import *

class Application():
    def __init__(self, api, date_time) -> None:
        self.api = api
        self.event_list = []
        self.archived_event_list = []
        self.date_time_now = date_time

    def on_start(self):
        self.event_list = self.get_event_list(self.api)
        print('+-------------------------+')
        print('|       Welcome to        |')
        print('|     MyEventManager      |')
        print('|       Application       |')
        print('+-------------------------+')
        while True:
            input_val = self.display_menu()
            if input_val == '1':
                for i in range(len(self.event_list)):
                    print('[{index}] {event_time} | {event_name}'.format(index=i+1, event_time=self.event_list[i].start['dateTime'], event_name=self.event_list[i].summary))
            elif input_val == '2':
                self.add_event(self.api)
            elif input_val == '3':
                self.delete_event(self.api)
            elif input_val == '4':
                self.cancel_event(self.api)  
            elif input_val == '5':
                pass #placeholder for updating an event 
            elif (input_val == 'e') or (input_val == 'E'):
                print('Thank you for using our application!')
                break

    def display_menu(self):
        print('[]==========================================================[]')
        print('What would you like to do?')
        print("1) View All Events")
        print("2) Add New Event")
        print("3) Delete Event")
        print("4) Cancel Event")
        print("5) Edit Event")
        print("e) Exit Application")
        input_val = -1
        valid_input = ['1','2','3','4','5','e','E']
        while input_val not in valid_input:
            input_val = input("Input your desired action based on the index: \n")
        return input_val
    
    def get_event_list(self, api):
        list_of_events = get_all_events(api)
        output_list = []
        for event in list_of_events:
            # There are actually cases where some existing events have no location registered
            try:
                # Check if the event being inspected has a location 
                event['location']
            except KeyError:
                # If the event under inspection has no location, then designate an Event object with no location registered
                output_list.append( Event(event['id'], event['summary'], None, event['creator'], event['organizer'], event['attendees'], event['start'], event['end']) )
            else:
                # If the event under inspection has a location then proceed as normal
                output_list.append( Event(event['id'], event['summary'], event['location'], event['creator'], event['organizer'], event['attendees'], event['start'], event['end']) )
            
        return output_list
    
    def add_event(self, api):
        new_event = start_new_event(api)
        # Check if it is right format
        self.event_list.append(new_event)

    def delete_event(self, api, time_now):
        options_to_delete = get_upcoming_events(api, time_now)
        lastest_event_index = len(self.event_list) - len(options_to_delete)
        # slice list as such list[(big_len - small_len) :]

    def cancel_event(self, apu):
        pass
