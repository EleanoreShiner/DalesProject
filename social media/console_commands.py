from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import sqlalchemy as sa
from model import User, Like

engine = create_engine('sqlite:///activities.sqlite', echo=True)
sess = Session(engine)