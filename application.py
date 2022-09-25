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
                self.delete_event(self.api, self.date_time_now)
            elif input_val == '4':
                self.cancel_event(self.api, self.date_time_now)  
            elif input_val == '5':
                pass #placeholder for updating an event 
            elif input_val == '6':
                self.restore_event(self.api)  
            elif (input_val == 'e') or (input_val == 'E'):
                print('Thank you for using our application!')
                break

    def display_menu(self):
        print('[]============================Menu============================[]')
        print('What would you like to do?')
        print("1) View All Events")
        print("2) Add New Event")
        print("3) Delete Event")
        print("4) Cancel Event")
        print("5) Edit Event")
        print("6) Restore Event")
        print("e) Exit Application")
        input_val = -1
        valid_input = ['1','2','3','4','5','6','e','E']
        while input_val not in valid_input:
            input_val = input("Input your desired action based on the index (input E to exit): \n")
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
        print('[]==========================Add Event==========================[]')
        
        # Obtaining user input 
        #========================================================================
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
            email = input("Input attendee " + str(i+1) + "'s email : " )
            attendee = {'email':'{email_to_insert}'.format(email_to_insert = email) }
            list_of_attendees.append(attendee)

        start_date = input("Insert a start date (follow yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format): ")
        
        end_date = input("Insert a end date (follow yyyy-mm-dd (2022-02-22) or the dd-MON-yy (12-AUG-22) format): ")
        #========================================================================
        
        # Check if input is right format; if so then add it to API; else throw error
        new_event = start_new_event(api, summary, location, list_of_attendees, start_date, end_date)

        # If no error is raised in above section, add the event to the list 
        self.event_list.append(new_event)

    def delete_event(self, api, time_now):
        print('[]========================Delete Event========================[]')
        options_that_can_be_deleted = []

        # Getting all the events that should be allowed to be deleted
        for i in range(len(self.event_list)):
            if self.event_list[i].end['dateTime'] < self.date_time_now:
                options_that_can_be_deleted.append(i)

        # Display options
        for i in range(len(options_that_can_be_deleted)):
            print('[{index}] {event_time} | {event_name}'.format(index=i+1, event_time=self.event_list[options_that_can_be_deleted[i]].start['dateTime'], event_name=self.event_list[options_that_can_be_deleted[i]].summary))
        
        input_val = -1
        valid_input = list(range(1,(len(options_that_can_be_deleted)+1)))
        while int(input_val) not in valid_input:
            input_val = input("Select event to delete by inputting it's index (input E to exit): \n")
            if input_val == 'e' or input_val == 'E':
                return 

        # Remove the event from the application's list of events
        event_to_delete = self.event_list.pop( int(options_that_can_be_deleted[(int(input_val) -1)]) )

        # Obtain event info
        event_to_delete_id = event_to_delete.id
        event_to_delete_time = event_to_delete.start['dateTime']

        # Delete the event from the online calendar
        delete_existing_event(api, event_to_delete_id, event_to_delete_time, time_now)

        # ==================================================================================================

        # options_not_to_delete = get_upcoming_events(api, time_now)
        # first_index_not_to_delete = len(self.event_list) - len(options_not_to_delete)
        # # Display options to delete
        # for i in range(first_index_not_to_delete):
        #     print('[{index}] {event_time} | {event_name}'.format(index=i+1, event_time=self.event_list[i].start['dateTime'], event_name=self.event_list[i].summary))

        # input_val = -1
        # valid_input = list(range(1,(first_index_not_to_delete+1)))
        # while int(input_val) not in valid_input:
        #     input_val = input("Select event to delete by inputting it's index (input E to exit): \n")
        #     if input_val == 'e' or input_val == 'E':
        #         return 

        # # Remove the event from the application's list of events
        # event_to_delete = self.event_list.pop((int(input_val) -1))

        # # Obtain event info
        # event_to_delete_id = event_to_delete.id
        # # temp = event_to_delete.summary
        # event_to_delete_time = event_to_delete.start['dateTime']

        # # print('{one} | {two}'.format(one = event_to_delete_time, two = temp))

        # # Delete the event from the online calendar
        # delete_existing_event(api, event_to_delete_id, event_to_delete_time, time_now)
        

    def cancel_event(self, api, time_now):
        print('[]========================Cancel Event========================[]')
        options_that_can_be_deleted = []

        # Getting all the events that should be allowed to be deleted
        for i in range(len(self.event_list)):
            if self.event_list[i].end['dateTime'] < self.date_time_now:
                options_that_can_be_deleted.append(i)

        # Display options
        for i in range(len(options_that_can_be_deleted)):
            print('[{index}] {event_time} | {event_name}'.format(index=i+1, event_time=self.event_list[options_that_can_be_deleted[i]].start['dateTime'], event_name=self.event_list[options_that_can_be_deleted[i]].summary))

        input_val = -1
        valid_input = list(range(1,(len(options_that_can_be_deleted)+1)))
        while int(input_val) not in valid_input:
            input_val = input("Select event to cancel by inputting it's index (input E to exit): \n")
            if input_val == 'e' or input_val == 'E':
                return 

        # Remove the event from the application's list of events
        event_to_cancel = self.event_list.pop( int(options_that_can_be_deleted[(int(input_val) -1)]) )

        # Put it into a backup / archive list 
        self.archived_event_list.append(event_to_cancel)

        # Obtain event info
        event_to_cancel_id = event_to_cancel.id
        event_to_cancel_time = event_to_cancel.start['dateTime']

        # Delete the event from the online calendar
        delete_existing_event(api, event_to_cancel_id, event_to_cancel_time, time_now)

    def restore_event(self, api):
        if len(self.archived_event_list) == 0:
            print('There are no events in backup/archive')
            return

        for i in range(len(self.archived_event_list)):
            print('[{index}] {event_time} | {event_name}'.format(index=i+1, event_time=self.archived_event_list[i].start, event_name=self.archived_event_list[i].summary))

        input_val = -1
        valid_input = list(range(1,(len(self.archived_event_list)+1)))
        while int(input_val) not in valid_input:
            input_val = input("Select event to cancel by inputting it's index (input E to exit): \n")
            if input_val == 'e' or input_val == 'E':
                return 

        # Obtaining the event to be restored
        event_to_restore = self.archived_event_list.pop(int(input_val) - 1) 

        # Create a new event 
        restored_event = start_new_event(api, event_to_restore.summary, event_to_restore.location, event_to_restore.attendees, event_to_restore.start[:10], event_to_restore.end[:10])

        # Restore (technically add) the event to the list 
        self.event_list.append(restored_event)
            

