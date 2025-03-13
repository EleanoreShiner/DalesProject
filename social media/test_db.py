import pytest
import sqlalchemy.orm as so
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from models import User, Post, Comment, Base

from write_to_db import write_initial_data
from controller import Controller

from models import Base, User, Post, Comment

test_db_location = 'sqlite:///test_database.db'

def test_test():
    assert 3**2 == 9

class TestDatabase:
    @pytest.fixture(scope='class')
    def db_session(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        session = so.Session(engine)
        yield session
        session.close()
        Base.metadata.drop_all(engine)

    def test_valid_user(self, db_session):
        user = User(name="Rayhan", age = 20, gender="male")
        db_session.add(user)
        db_session.commit()
        qry = sa.select(User).where(User.name == "Rayhan")
        rayhan = db_session.scalar(qry)
        assert rayhan is not None
        assert rayhan.name == "Rayhan"
        assert rayhan.age == 20
        assert rayhan.gender == "male"
        assert rayhan.nationality is None

    def test_invalid_user(self, db_session):
        user = User(age=7, nationality='British')
        db_session.add(user)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_add_post(selfself, db_session):
        user = User(name="Eleanore", age = 20, gender="female")
        post = Post(title = 'hi', description = 'hello')
        user.posts.append(post)

class TestController:
    @pytest.fixture(scope='class', autouse=True)
    def test_db(self):
        engine = sa.create_engine(test_db_location)
        Base.metadata.create_all(engine)
        write_initial_data(engine)
        yield
        Base.metadata.drop_all(engine)

    @pytest.fixture(scope='class')
    def controller(self):
        control = Controller(db_location=test_db_location)
        return control

    def test_set_current_user_from_name(self, controller):
        controller.set_current_user_from_name("Alice")
        assert controller.current_user.name == "Alice"
        assert controller.current_user.age == 30
        assert controller.current_user.gender == "Female"

    def test_get_user_names(self):

    def test_create_user(self):
        assert False

    def test_get_posts():
        assert False

    def test_create_posts():
        assert False

    def test_get_comments():
        assert False

    def test_create_comment():
        assert False

    def test_like_post():
        assert False
