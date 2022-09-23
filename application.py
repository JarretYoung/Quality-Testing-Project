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
                temp = get_upcoming_events(self.api, self.date_time_now, 40)
            elif input_val == '2':
                start_new_event(self.api)
            elif input_val == '3':
                get_all_events(self.api)  
            elif (input_val == 'e') or (input_val == 'E'):
                print('Thank you for using our application!')
                break

    def display_menu(self):
        print('[]===============================[]')
        print('What would you like to do?')
        print("1) View Future Events")
        print("2) Add New Event")
        print("3) View All Events")
        print("e) Exit Application")
        input_val = -1
        while (input_val != 1) and (input_val != 2) and (input_val != 3):
            input_val = input("Input your desired action based on the index")
        return input_val
    
    def get_event_list(self, api):
        list_of_events = get_all_events(api)
        output_list = []
        for event in list_of_events:
            output_list.append( Event(event['id'], event['summary'], event['location'], event['creator'], event['organizer'], event['attendees'], event['start'], event['end']) )
        return output_list
    
    def add_event(self, api):
        new_event = start_new_event(api)
        self.event_list.append(new_event)

    def delete_event(self, api):
        pass

    def cancel_event(self, apu):
        pass
