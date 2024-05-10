import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]



def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
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

  try:
    service = build("calendar", "v3", credentials=creds)
    
    get_events(service)
    create_event(service)

  except HttpError as error:
    print(f"An error occurred: {error}")



def get_events(service):
    # Call the Calendar API
    now = datetime.datetime.now(datetime.UTC).isoformat()  # 'Z' indicates UTC time
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
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])


def create_event(service):
  # Refer to the Python quickstart on how to setup the environment:
  # https://developers.google.com/calendar/quickstart/python
  # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
  # stored credentials.
  

  event = {
    'summary': 'Testing calendar api application that will soon have a place to create events super easy but its in the beginning stages rn ',
    'location': ' no location ',
    'description': 'Hey I dont mean to scare you just seeing if this works if it does you can totally message your bro mathew that it totally works  ',
    'start': {
      'dateTime': '2024-05-03T08:00:00-06:00',
      'timeZone': 'America/Denver',
    },
    'end': {
      'dateTime': '2024-05-03T08:00:00-07:00',
      'timeZone': 'America/Denver',
    },

    'attendees': [
      {'email': '12matt.zamacona@gmail.com'},
      
    ],
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 12 * 60},
        {'method': 'popup', 'minutes': 12 * 60},
      ],
    },
  }

  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))


if __name__ == "__main__":
  main()
