from application import *
from unittest.mock import MagicMock, Mock, patch


    
if __name__ == '__main__':
    time_now = '2022-09-20T03:29:17.380207Z'
    api = get_calendar_api()
    mock_api = MagicMock()
    mock_api.events.return_value.list.return_value.execute.return_value = {'items' : []}
    app = Application(api, time_now)
    app.on_start()
    