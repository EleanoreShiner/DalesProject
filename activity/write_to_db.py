from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Person, Activity

people = [Person(first_name="Eleanore", last_name="Shiner"),
          Person(first_name='Snake', last_name="Charmer"),
          Person(first_name='Dennis', last_name="Zazuliak"),
          ]

chess = Activity(name="Chess")
fives = Activity(name="Fives")
outdoor_ed = Activity(name="Outdoor Ed")

people[0].activities.append(chess)
people[0].activities.append(fives)
people[1].activities.append(outdoor_ed)
people[1].activities.append(fives)

engine = create_engine('sqlite:///activities.sqlite', echo=True)

with Session(engine) as sess:
    sess.add_all(people)
    sess.commit()

