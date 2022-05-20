COEN 241 group project API documentation
__author__ = 'Yujie Zhu'

Get all events:
    Method:
        GET
    URL:
        'http://184.169.246.42:8088/api/list_all'
    Body:
        None
    Example:
        GET /api/list_all

Get specific event:
    Method:
        GET
    URL:
        'http://184.169.246.42:8088/api/get_event/<int:eid>'
    Body:
        None
    Example:
        GET /api/get_event/1

Create a new event:
    Method:
        POST
    URL:
        'http://184.169.246.42:8088/api/new_event'
    Body:
        {"event_name": "<EVENTNAME>", "date": "<MM/DD/YYYY>", "place": "<PLACENAME>", 
        "sport": "<SPORTNAME>", "user_name": "<USERNAME>"}
    Example:
        POST /api/new_event
        Body:
            {"event_name": "some event 4", "date": "05/11/2022", 
            "place": "gym1", "sport": "football", "user_name": "someone"}

Add a user to existing event:
    Method:
        POST
    URL:
        'http://184.169.246.42:8088/api/add_user'
    Body:
        {"user_name": "<USERNAME>", "eid": <EID>}
    Example:
        POST /api/add_user
        Body:
            {"user_name": "ben", "eid": 28}


Delete a user from existing event:
    Method:
        DELETE
    URL:
        'http://184.169.246.42:8088/api/delete_user'
    Body:
        {"user_name": "<USERNAME>", "eid": <EID>}
    Example:
        DELETE /api/delete_user
        Body:
            {"user_name": "ben", "eid": 28} 


Delete an event:
    Method:
        DELETE
    URL:
        'http://184.169.246.42:8088/api/delete_event'
    Body:
        {"eid": <EID>}
    Example:
        DELETE /api/delete_event
        Body:
            {"eid": 28} 