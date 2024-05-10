
import base64
import datetime
import json
import os.path
from typing import Tuple
from schemas import CalendarEvent, Create_Calendar_Event
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import googleapiclient.discovery
from google.oauth2 import service_account


from google.auth import jwt
SCOPES = ["https://www.googleapis.com/auth/calendar"]



def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  try:
    service = get_google_service()
    get_events(service)
    create_event(service)
    service = initialize_calendar_client()
  except HttpError as error:
    print(f"An error occurred: {error}")


def get_google_service():
  creds = get_creds()
  service = build("calendar", "v3", credentials=creds)
  return service


def get_creds():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  return creds


def initialize_calendar_client():
    # Create Google Calendar API client
    credentials = service_account.Credentials.from_service_account_file("path/to/service_account_key.json")
    scoped_credentials = credentials.with_scopes(SCOPES)
    calendar_client = build("calendar", "v3", credentials=scoped_credentials)
    return calendar_client

def get_events(service):
  # Call the Calendar API
  now = datetime.datetime.now(datetime.UTC).isoformat()
  print("Getting the upcoming 10 events")
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=now,
          maxResults=10,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])
  if not events:
    print("No upcoming events found.")
    return
  # Prints the start and name of the next 10 events
  calendar_events: list[CalendarEvent] = []
  for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    summary = event["summary"]
    description = event.get("description", None)
    id = event["id"]
    attendees = event["attendees"]
    location = event["location"]
    status = event["status"]


    calendar_events.append(CalendarEvent(start=start,
                                         end=end,
                                         summary=summary,
                                         description=description ,
                                         id=id,
                                        #  attendees=attendees,
                                         location=location,
                                         status=status,

                                         ))
  return calendar_events


def convert_to_iso_date_time(date_str: str, time_str: str, tz: str = "America/Denver") -> str:
    # Assuming date_str and time_str are in the format "YYYY-MM-DD" and "HH:MM:SS"
    dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
    dt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=0)))  # Convert to UTC
    dt = dt.astimezone(datetime.timezone(datetime.timedelta(hours=-7)))  # Convert to America/Denver
    return dt.isoformat()


def create_event(service, event: Create_Calendar_Event):
    # Convert date and time to ISO 8601 format
    start_datetime = str(event.start.astimezone())
    end_datetime = str(event.end.astimezone())
    event_body = {
        'summary': event.summary,
        'location': event.location, 
        'description': event.description,
        'start': {
            'dateTime': event.start.isoformat(),
            'timeZone': 'America/Denver',  # You can change the timeZone as needed
        },
        'end': {
            'dateTime': event.end.isoformat(),
            'timeZone': 'America/Denver',
        },
         'attendees': [{'email': event.attendees},{'email': event.attendees}],
          'reminders': {
              'useDefault': False,
              'overrides': [
                  {'method': 'email', 'minutes': 24 * 60},
                  {'method': 'popup', 'minutes': 10},

              ] if event.reminders else [],
          },
          
    }
    

    event = service.events().insert(calendarId='primary', body=event_body).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    event_id = event['id']
    print('Event created with ID: %s' % event_id)
    return event_id, event


def delete_event(service, event_id: str):
        service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f"Event with ID {event_id} deleted successfully.")
    
      
def update_event(service, event_id:str, event: CalendarEvent ):
  #  service = get_google_service()
   
   event_body = {
        'summary': event.summary,
        'location': event.location, 
        'description': event.description,
        'start': {
            'dateTime': event.start.isoformat(),
            'timeZone': 'America/Denver',  # You can change the timeZone as needed
        },
        'end': {
            'dateTime': event.end.isoformat(),
            'timeZone': 'America/Denver',
        },
         'attendees': [{'email': event.attendees}],
          'reminders': {
              'useDefault': False,
              'overrides': [
                  {'method': 'email', 'minutes': 24 * 60},
                  {'method': 'popup', 'minutes': 10},
              ]if event.reminders else [],
          },'eventId': 'summary'} 
   event = service.events().update(id=id, body=event_body).execute()
   service.events().update( body=event_body).execute()
   service.events().update(calendarId='primary', eventId=event_id).ececute()


def filter_events(events: list[CalendarEvent]) -> list[CalendarEvent]:
    filtered_events = []
    for event in events:
        # Extract the day of the week from the start date of the event
        start_day_of_week = event.start.date.weekday()
        # Check if the event falls on Friday (4) or Saturday (5)
        if start_day_of_week in [4, 5]:
            filtered_events.append(event)
    return filtered_events




def decode_header(token):
    # Add padding to the token if needed to ensure its length is a multiple of 4
    padding_needed = len(token) % 4
    if padding_needed:
        token += '=' * (4 - padding_needed)
    # Split the token into its components (header, payload, signature)
    parts = token.split(".")
    # Decode the header (first part of the token)
    encoded_header = parts[0]
    decoded_header = base64.urlsafe_b64decode(encoded_header + "==").decode("utf-8")
    
    # Parse the decoded header as JSON
    header_data = json.loads(decoded_header)
    
    return header_data

# Example usage:
encoded_jwt = "your_encoded_jwt_here"

try:
    # Decode only the header of the JWT
    header = decode_header(encoded_jwt)
    print("Decoded JWT Header:")
    print(header)
except Exception as e:
    print("JWT Decode Error:", e)



if __name__ == "__main__":
  main()