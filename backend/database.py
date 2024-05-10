# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# from sqlalchemy import create_engine
# from sqlalchemy.engine import URL


# SQLALCHEMY_DATABASE_URL = "postgresql://postgresql@postgresserver/db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()
from models import Users
from decouple import config
from sqlmodel import Session, create_engine

DATABASE_URL = config("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session

def create_user(users: Users):
    with Session(engine) as session:
        db_users = Users.from_orm(users)
        session.add(db_users)
        session.commit()
        session.refresh(db_users)
        return db_users
    
def delete_users(users: Users):
    with Session(engine) as session:
        db_users = Users.from_orm(users)
        session.delete(db_users)
        session.commit()
        session.refresh(db_users)

