
from googleapiclient.errors import HttpError
from fastapi import FastAPI, HTTPException, Depends, Response
from schemas import CalendarEvent, Create_Calendar_Event
from googleapiclient.discovery import build
from typing import List
import quickstart2

from quickstart2 import delete_event
from database import get_db
from models import Users
from sqlmodel import Session, select

from googleapiclient.discovery import build

from models import Users
from database import create_user, get_db

app = FastAPI()


@app.get("/events")
async def get_calendar_events():
    service = quickstart2.get_google_service()
    return quickstart2.get_events(service)

@app.post("/events", response_model=Create_Calendar_Event)
async def create_event(event: Create_Calendar_Event, db: Session = Depends(get_db)):
    service = quickstart2.get_google_service()
    event_id, _ = quickstart2.create_event(service, event)
    event.eventId = event_id
    return event

@app.delete("/events/{event_id}")
async def delete_calendar_event(event_id: str):
    # Assuming you have defined 'service' elsewhere in your code
    service = quickstart2.get_google_service()
    try:
        quickstart2.delete_event(service, event_id)
        return {"message": f"Event with ID {event_id} deleted successfully."}
    except HttpError as error:
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting the event: {error}")


@app.put("/events/{id}")
async def update_event(id: str, event):
    service = quickstart2.get_google_service()
    quickstart2.update_event( event, id, service)


@app.get("/flitered_events")
async def get_filtered_events() -> List[CalendarEvent]:
    try:
        service = quickstart2.get_google_service()
        events = quickstart2.get_events(service)
        filtered_events = quickstart2.filter_events(events)
        return filtered_events
    except HttpError as error:
    
        return {"error": f"An error occurred: {error}"}
    


@app.post("/create_user")
async def create_user(users: Users, db: Session = Depends(get_db)):
    db.add(users)
    db.commit()

@app.get("/users")
async def get_users(db: Session = Depends(get_db)) -> list[Users]:
    return db.exec(select(Users)).all()

@app.put("/users/{user_id}")
async def update_users(db: Session = Depends(get_db)):
    pass

@app.delete("/users/{user_id}")
async def delete_users(users: Users,db: Session = Depends(get_db)):
    db.delete(users)
    db.commit()













# credentials = service_account.Credentials.from_service_account_file("token.json")
# scoped_credentials = credentials.with_scopes(SCOPES)
# calendar_client = build("calendar", "v3", credentials=scoped_credentials)
