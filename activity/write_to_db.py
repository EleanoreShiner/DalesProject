from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person, Activity, Location

# Create people
people = [
    Person(first_name="snake", last_name="charmer"),
    Person(first_name='elle', last_name='shiner'),
    Person(first_name='Adam', last_name='Reeves'),
    Person(first_name="dennis", last_name="zazuliak"),
]

# Check and create or reuse locations
def get_or_create_location(session, room_name):
    location = session.query(Location).filter_by(room=room_name).first()
    if not location:
        location = Location(room=room_name)
        session.add(location)
    return location

# Create activities
chess = Activity(name="Chess", location=location_chess)
fives = Activity(name="Fives", location=location_fives)
outdoor_ed = Activity(name="Outdoor Ed", location=location_fives)
drawing = Activity(name="Drawing", location=location_chess)

# Assign activities to people
people[0].activities.append(chess)
people[0].activities.append(fives)
people[1].activities.append(outdoor_ed)
people[1].activities.append(drawing)

# Insert into the database
engine = create_engine('sqlite:///activities.sqlite', echo=True)

with Session(engine) as sess:
    location_chess = get_or_create_location(sess, '7')
    location_fives = get_or_create_location(sess, 'Fives court')
    sess.add_all(people)
    sess.commit()
