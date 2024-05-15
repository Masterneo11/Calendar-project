
from google_service import Create_Calendar_Event, get_events, delete_event, update_event, create_event
from datetime import datetime
from fastapi.testclient import TestClient
from database import get_db

from unittest.mock import MagicMock
from unittest.mock import patch
from models import Users
from app import app 

# Define a MagicMock object to mock the Calendar class
calendar_service_mock = MagicMock()

test_client = TestClient(app=app)

def test_get_events():
    # Use the mock Calendar service to get events
    mocked_events_response = {
        "items": [
            {
            'summary': 'getting food',
            'start': {
            'dateTime': '2024-05-15T14:14:24.862Z',
            'timeZone': 'America/Denver',
                    },
            'end': {
                'dateTime': '2024-05-15T20:14:24.862Z',
                'timeZone': 'America/Denver',},
            'id': 'at347947h8dddh',
            'status': 'confirmed',

              
            } ]}
    
    calendar_service_mock.events().list().execute.return_value = mocked_events_response
    
    events = get_events(calendar_service_mock)
    assert len(events) == 1
    assert events[0].summary == "getting food"
    assert events[0].id == 'at347947h8dddh'


def test_delete_event():
    id = "at347947h8dddh"
    result = delete_event(calendar_service_mock, id)
    assert result == None


def test_update_event():
    # Mock data
    event_id = "at347947h8dddh"
    start = {
        'dateTime': '2024-05-15T14:14:24.862Z',
        'timeZone': 'America/Denver',
    }
    date_string = '2024-05-15T14:14:24.862Z'
    datetime_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

    end_date_str = '2024-05-15T20:14:24.862Z'
    end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    event = Create_Calendar_Event(
        start= datetime_obj,
        location= 'somewhere',
        attendees="fake@gmail.com",
        summary='a summary',
        reminders="string",
        eventId='at347947h8dddh',
        end=end_date_obj,
        description='some description',
        )
    update_event(calendar_service_mock, event_id, event)

    assert event.location == 'somewhere'
    assert event.summary == 'a summary'
    assert event.reminders == 'string'
    assert event.end == end_date_obj
    assert event.attendees == "fake@gmail.com"
    assert event.description == 'some description'
    

def test_create_event():

    date_string = '2024-05-15T14:14:24.862Z'
    datetime_obj = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

    end_date_str = '2024-05-15T20:14:24.862Z'
    end_date_obj = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    event = Create_Calendar_Event(
        start= datetime_obj,
        location= 'somewhere',
        attendees="fake@gmail.com",
        summary='a summary',
        reminders="string",
        eventId='at347947h8dddh',
        end=end_date_obj,
        description='some description',
        )
    create_event(calendar_service_mock, event)
    
    assert event.attendees == "fake@gmail.com"
    assert event.description == 'some description'
    assert event.location == 'somewhere'
    assert event.summary == 'a summary'
    assert event.reminders == 'string'
    assert event.end == end_date_obj


def test_create_user():
    # making fake user data lol 
    user_data = {
        "name": "Test User",
        "phone_number": "1234567890"
    }

    # Send a POST request to the create_user endpoint
    response = test_client.post("/create_user", json=user_data)

    assert response.status_code == 200
    assert response.json()["name"] == user_data["name"]
    assert response.json()["phone_number"] == user_data["phone_number"]
    
    
def test_delete():
    user = Users(id=9, phone_number='425-707-9887' ,name='test_name')
    with patch('database.db') as mock_db:
        mock_db.exec().one().return_value = user
        
    # mock returning the user that i have on 124 
    # check to make sure that db.delete with that user

        test_client.delete(f'/users/{user.id}')
        print('checking')

def test_get_user():
    user = Users(id=9, phone_number='425-707-9887' ,name='test_name')
    with patch('database.db') as mock_db:
        mock_db.exec().one().return_value = user
        test_client.get("/users")

def test_update_user():
    user = Users(id=9, phone_number='425-707-9887' ,name='test_name')
    with patch('database.db') as mock_db:
        mock_db.exec().one().return_value = user
        
    # mock returning the user that i have on 124 
    # check to make sure that db.delete with that user

        test_client.put(f"/users/{user.id}")
        print('checking')
