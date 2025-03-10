import sqlalchemy as sa
import sqlalchemy.orm as so

from models import User, Post, Comment
import pyinputplus as pyip

class Controller:
    def __init__(self, db_location = 'sqlite:///social_media.db'):
        self.current_user = None
        self.engine = sa.create_engine(db_location)

    def set_current_user_from_name(self, name):
        with so.Session(bind=self.engine) as session:
            self.current_user = session.scalars(sa.select(User).where(User.name == name)).one_or_none()

    def get_user_names(self):
        with so.Session(bind=self.engine) as session:
            user_names = session.scalars(sa.select(User.name).order_by(User.name)).all()
        return list(user_names)

    def create_user(self, name:str, age:int, gender:str, nationality:str) -> User:
        with so.Session(bind=self.engine) as session:
            user = User(name=name, age=age, gender=gender, nationality=nationality)
            session.add(user)
            session.commit()
            self.current_user = user
        return user

    def get_posts(self, user_name: str) -> list[dict]:
        with so.Session(bind=self.engine) as session:
            user = session.scalars(sa.select(User).where(User.name == user_name)).one_or_none()
            if not user:
                return []
            posts_info = [{
                'title': post.title,
                'id': post.id,
                'description': post.description,
                'number_likes': len(post.liked_by_users)
            } for post in user.posts]
        return posts_info

    def create_posts(self, title:str, content:str):
        with so.Session(bind=self.engine) as session:
            user = session.merge(self.current_user)
            post = Post(title=title, description=content, user_id=user.id, user=user)
            session.add(post)
            session.commit()

    def like_post(self, post_id):
        with so.Session(bind=self.engine) as session:
            user = session.merge(self.current_user)
            post = session.get(Post, post_id)  # Fetch post
            if post and user not in post.liked_by_users:
                post.liked_by_users.append(user)
                session.commit()

class CLI:
    def __init__(self):
        self.controller = Controller()
        self.login()

    @staticmethod
    def show_title(title):
        print('\n' + title)
        print('-' * len(title) + '\n')

    def login(self):
        self.show_title('Login Screen')
        users = self.controller.get_user_names()
        menu_items = users + ['Create a new account',
                              'Exit',
                              ]
        menu_choice = pyip.inputMenu(menu_items,
                                     prompt='Select user or create a new account\n',
                                     numbered=True,
                                     )
        if menu_choice.lower() == 'create a new account':
            self.create_account()
        elif menu_choice.lower() == 'exit':
            print('Goodbye')
        else:
            user_name = menu_choice
            self.controller.set_current_user_from_name(user_name)
            self.user_home()

    def create_account(self, existing_users=None):
        self.show_title('Create Account Screen')
        print('Enter Account Details')
        user_name = pyip.inputStr('Username: ', blockRegexes=existing_users, strip=None)
        age = pyip.inputInt('Age: ', min=0, max=150, blank=True)
        gender = pyip.inputMenu(['male', 'female', 'other'], prompt='Gender: ', blank=True)
        nationality = pyip.inputStr('Nationality: ')
        self.controller.create_user(user_name, age, gender, nationality)
        self.login()

    def user_home(self):
        self.show_title(f'{self.controller.current_user.name} Home Screen')
        print(f'Name: {self.controller.current_user.name}')
        print(f'Age: {self.controller.current_user.age}')
        print(f'Nationality: {self.controller.current_user.nationality}')
        self.show_posts(self.controller.current_user.name)

        menu_items = {'Show posts from another user': self.show_posts,
                      'Create posts' : self.create_posts,
                      'Logout': self.login}

        menu_choice = pyip.inputMenu(list(menu_items.keys()),
                                     prompt='Select an action\n',
                                     numbered=True,
                                     )
        menu_items[menu_choice]()
        if menu_choice != 'Logout':
            self.user_home()

    def post_menu(self, posts):
        self.show_title('Post Actions')
        post_map = {post["title"]: post for post in posts}
        post_titles = list(post_map.keys()) + ['Exit']
        like_menu = pyip.inputMenu(post_titles, prompt='Choose a post to like/unlike or exit\n', numbered=True)
        if like_menu.lower() == 'exit':
            return
        else:
            post = post_map[like_menu]
            self.controller.like_post(post["id"])
            self.post_menu(posts)

    def show_posts(self, user_name: str | None = None):
        if user_name is None:
            users = self.controller.get_user_names()
            menu_choice = pyip.inputMenu(users,
                                         prompt='Select a user\n',
                                         numbered=True,
                                         )
            user_name = menu_choice

        self.show_title(f"{user_name}'s Posts")
        posts = self.controller.get_posts(user_name)
        for post in posts:
            print(f'ID: {post["id"]}')
            print(f'Title: {post["title"]}')
            print(f'Content: {post["description"]}')
            print(f'Likes: {post["number_likes"]}')

        if not posts:
            print('No Posts')
        else:
            self.post_menu(posts)


    def create_posts(self):
        print('Enter Post Details')
        title = pyip.inputStr('Title: ')
        content = pyip.inputStr('Content: ', blank=True)
        self.controller.create_posts(title, content)
        self.login()




cli = CLI()
controller = Controller()