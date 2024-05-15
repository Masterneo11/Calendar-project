
from googleapiclient.errors import HttpError
from fastapi import FastAPI, HTTPException, Depends
from schemas import CalendarEvent, Create_Calendar_Event
from googleapiclient.discovery import build
from typing import List
import google_service

from database import get_db
from models import Users
from sqlmodel import Session, select


app = FastAPI()


@app.get("/events")
async def get_calendar_events():
    try:
        service = google_service.get_google_service()
        return google_service.get_events(service)
    except Exception as e:
        print(f"An error occurred while getting Google service or events: {e}")

@app.post("/events", response_model=Create_Calendar_Event)
async def create_event(event: Create_Calendar_Event, db: Session = Depends(get_db)):
    try:
        # getting the google service and getting a list of the events 
        service = google_service.get_google_service()
        event_id, _ = google_service.create_event(service, event)
        event.eventId = event_id
        return event
    except Exception as e:
         raise HTTPException(status_code=404, detail="Most likely an issue w/ : date-times format or an email for attendees section")
        

@app.delete("/events/{event_id}")
async def delete_calendar_event(event_id: str):
    #will delete an event using the event id as a str
    service = google_service.get_google_service()
    try:
        google_service.delete_event(service, event_id)
        return {"message": f"Event with ID {event_id} deleted successfully."}
    except HttpError as error:
        raise HTTPException(status_code=400, detail=f"An error occurred while deleting the event: {error}")

@app.put("/events/{event_id}")
async def update_event_endpoint(event_id: str, event: CalendarEvent):
   try:
        service = google_service.get_google_service()
        google_service.update_event(service, event_id, event)
        return {"message": "Event updated successfully"}
   except HttpError as error:
      raise HTTPException(status_code=400, detail=f' That user id might already be deleted try another one{error}')
   
@app.get("/calendars")
async def get_list_calendars():
    service = google_service.get_google_service()
    calendars = google_service.get_list_of_calendars(service)
    return {"message": "successfully gathered list of calendars just keeping my info private "}


# saving this feature for another day further down the road if I get to it
# @app.get("/flitered_events")
# async def get_filtered_events() -> List[CalendarEvent]:
#     try:
#         service = google_service.get_google_service()
#         events = google_service.get_events(service)
#         filtered_events = google_service.filter_events(events)
#         return filtered_events
#     except HttpError as error:
#         return {"error": f"An error occurred: {error}"}
    

@app.post("/create_user")
async def create_user(users: Users, db: Session = Depends(get_db)):
    try:
        db.add(users)
        db.commit()
        return {"message": "user was succesfully Created"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}maybe delte the pk column and try again')
    
@app.get("/users")
async def get_users(db: Session = Depends(get_db)) -> list[Users]:
    return db.exec(select(Users)).all()

@app.put("/users/{user_id}")
async def update_users(user_id: int, users: Users, db: Session = Depends(get_db)):
    try:
        user = db.get(Users, user_id)
        if user:
            user.name = users.name
            user.phone_number = users.phone_number
            db.add(user)
            db.commit()
            return {"message": "User updated successfully"}
        else:
            # add a new one 
            new_user = Users(id=user_id, name=users.name, phone_number=users.phone_number)
            db.add(new_user)
            db.commit()
            return {"message": "New user created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=" try another user id ")


@app.delete("/users/{user_id}")
async def delete_users(user_id: int, db: Session = Depends(get_db)):
    try:    
        statement = select(Users).where(Users.id == user_id)
        results = db.exec(statement)
        user = results.one()
        db.delete(user)
        db.commit()
        return {"message": "User was deleted succesfully"}    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}That user id might not exist try another one")

