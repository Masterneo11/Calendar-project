from pydantic import BaseModel
from datetime import datetime
from typing import List

class CalendarEvent(BaseModel):
    
    start: datetime 
    end: datetime 
    summary: str 
    description: str | None = None
    attendees : List[str] | None = None
    location :str | None = None
    id: str | None = None
    status: str | None = None
    
    
   
class Create_Calendar_Event(BaseModel):
    
    start: datetime
    end: datetime
    summary: str
    description: str | None = None
    location : str | None = None
    attendees: str 
    eventId: str  | None = None
    reminders: str | None = None
    
    
class CalendarList(BaseModel):
    kind: str
    etag: str
    id: str
    accessRole: str
    defaultReminders: list
    selected: bool
    timeZone: str
    updated: str

    
  