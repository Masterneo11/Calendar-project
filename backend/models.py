from sqlmodel import Field,Relationship, SQLModel, BIGINT

class Users(SQLModel, table=True):
    id : int = Field(default=None, primary_key=True)
    name :str
    phone_number : str
    



