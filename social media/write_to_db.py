from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model import User, Like, Post

# Create people
Users = [
    User(name="shiney", age=100000, gender="girly", nationality="american"),
    User(name="snakecharmer", age=9, gender="buddy", nationality="british"),
    User(name="Dennis", age=17, gender="tree", nationality="forest"),
]

# Check and create or reuse locations
def get_or_create_like(session, post_title):
    post = session.query(Post).filter_by(room=post_title).first()
    if not post:
        post = Post(title = post_title)
        session.add(post)
        session.add(post)
    return post

post1 = Post(title="post 1")

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
