import sqlalchemy as sa
import sqlalchemy.orm as so
from model import User, Post, Comment, Base

engine = sa.create_engine('sqlite:///social_media.db', echo=True)
session = so.Session(bind=engine)

# Create people
users = [
    User(name="shiney", age=100000, gender="girly", nationality="american"),
    User(name="snakecharmer", age=9, gender="buddy", nationality="british"),
    User(name="Dennis", age=17, gender="tree", nationality="forest"),
]

# Check and create or reuse locations
posts = [
    Post(title=":)", description="Super cool stuff"),
    Post(title=":(", description="Super not cool stuff"),
    Post(title="<3", description="yeeehawww"),
]

for i in range(len(users)):
    users[i].posts.append(posts[i])

# Add likes
users[0].liked_posts.append(posts[1])
users[0].liked_posts.append(posts[2])
users[1].liked_posts.append(posts[0])
users[1].liked_posts.append(posts[3])
users[2].liked_posts.append(posts[0])
users[2].liked_posts.append(posts[3])

session.add_all(users)
session.commit()

comments = [
    Comment(user_id=users[1].id, comment="agreed"),
    Comment(user_id=users[2].id, comment="agreed"),
    Comment(user_id=users[3].id, comment="agreed"),
    Comment(user_id=users[3].id, comment="disagree"),
    Comment(user_id=users[0].id, comment="disagree"),
]

posts[0].comments.append(comments[0])
posts[0].comments.append(comments[1])
posts[1].comments.append(comments[2])
posts[2].comments.append(comments[3])
posts[3].comments.append(comments[4])

session.add_all(comments)
session.commit()