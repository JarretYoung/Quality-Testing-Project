+=============================================+
|                                             |
|            FIT2107 Assignment 2             |
|      Test Strategies and Justification      |
|                                             |
+=============================================+=========+
|Students:                                              |
| - Garret Yong Shern Min (31862616)                    |
| - Yip Kin Keat (30722063)                             |
| - Choo Bi Shan (33053758)                             |
+=======================================================+

(]==============================================================[)
Student Name :          Garret Yong Shern Min
Student ID :            31862616
Sections Worked on :    Events & Navigation
Branches Created :      application_navigation_feature
                        deleting_events_tester
                        creating_events_tester
 
          ==============================================
For the creation of the test cases, several testing strategies were put into play to ensure the feasibility and robustness of the application.
 
The inspiration for the test cases for the creation/ starting of events would be the MC/DC testing method. This is due to the nature of the validation check that had to be conducted by the check_event_input() method which takes in 5 arguments. If I were to test every possible combination, there would be 32 test cases alone for the validation check. Hence MC/DC testing was used to only target important combinations with the widest coverage. Eventually, the number of test cases was reduced to 14. In addition, branch coverage testing strategy was kept in mind when designing all my test cases. Especially for creation of events where there are many decision statements which should be tested for feasibility and robustness.
 
There were several black box testing strategy rules that were included to increase the coverage of the test cases. For instance, when testing date entry, Equivalence Partitioning’s must rule dictated that there had to be one test case for invalid date and one for valid. However, since the invalid test cases for yyyy-mm-dd format and dd-MON-yy format were the same, they could be merged; however, to ensure branch coverage(because of the use of try, except statements to check the date formats) the two were kept separate. Another example of the must rule would be that all inputs must not be None or an empty string. So by combining MC/DC testing with this Equivalence Partitioning(EP) rule, we are able to easily cover the assertion of no missing input by having at least one valid input while one invalid input for each missing input. Besides that, validation done for the locations involved checking the state codes and postcodes. State codes are usually 2-3 characters long while postcodes are usually 4-5 digits long, since the valid test case was created (as mentioned earlier using MC/DC testing) we follow the EP rule of ranges. Hence two invalid cases were created each where one was testing below minimum and the other testing above maximum. 
 
The next development was the delete and cancel functions for the application. Due to the nature of the application, delete and cancel functions have drastically similar functionalities whereby the event is deleted from the API (cancel just stores the deleted event in the application’s archive list). Based on the specification, only past events are allowed to be deleted and/or cancelled which means that this falls under the Equivalence Partitioning’s range rule but since there is no minimum for the range, only one valid and one invalid test cases needed to be developed. However, due to the programming of the application which tries to prevent errors (keeps asking for input until valid) testing invalid input would be impossible using the UI. So, first the valid test cases were developed for both delete and cancel functions by simulating user inputs and validating (checking) the output to ensure that the values match up with expectations. On the other hand, to ensure an invalid case would be present, invalid inputs are inserted into the delete_existing_event() method in MyEventManager.py; this is done as the method will raise an error if the event’s date is during the future. In addition, since deleting and cancelling events can use the same invalid test case, only one test case is developed for both functionalities. 
 
The next development was the restore function, despite not being mentioned in the specifications explicitly, the notation was indicative that this function needed to be developed. Due to the application’s nature to prevent user error, and since there are no constraints to which events can or cannot be restored, there is only one test case present to prove that the function works. In a sense, the testing strategy used was intuition testing. 
 
The final development from my part would be the query function which allows users to search for specific events based on certain keywords/ queries. For this function, there are multiple categories which mainly include query by name and query by date time. This specification has no constraints that are explicitly mentioned so some assumptions were made. When querying the name of the event, the name cannot be None nor an empty string; when querying the start and end date, the input must follow the yyyy-mm-dd format. So, when developing the test cases for this section similar test strategies to the create events are used to ensure maximum coverage. When querying the names of the events via full name and keyword, one invalid test case with input as empty string and another valid test case with a non-empty string input and double-checking the queried events (Equivalence Partitioning: Must rule). Then, for querying start and end dates each, one input of incorrect/ invalid date format input and another of valid date format input (Equivalence Partitioning: Must rule). 

(]==============================================================[)


