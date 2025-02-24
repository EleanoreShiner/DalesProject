from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

# Abstract base class
class Base(so.DeclarativeBase):
    pass


likes_table = sa.Table(
    'likes',
    Base.metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    sa.Column('post_id', sa.Integer, sa.ForeignKey('posts.id'), nullable=False),
)

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[Optional[str]] = so.mapped_column(unique=True)
    age: so.Mapped[int|None]
    gender: so.Mapped[Optional[str|None]]
    nationality: so.Mapped[Optional[str|None]]
    liked_posts: so.Mapped[list['Post']] = so.relationship
    posts: so.Mapped[list["Post"]] = so.relationship( back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, age={self.age}, gender={self.gender})"

class Post(Base):
    __tablename__ = "posts"
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    user: so.Mapped["User"] = so.relationship("User", back_populates="posts")
    likes: so.Mapped[list["User"]] = so.relationship(secondary=likes_table,
                                                     back_populates='liked_posts')
    comments: so.Mapped[list["Comment"]] = so.relationship(back_populates='post')

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, description={self.description})"

class Comment(Base):
    __tablename__ = 'comments'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('users.id'))
    post_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('posts.id'))
    comment: so.Mapped[str]
    post: so.Mapped['Post'] = so.relationship(back_populates='comments')
    user: so.Mapped['User'] = so.relationship(back_populates='comments_made')

    def __repr__(self):
        return f"Comment(user_id={self.user_id}, post_id={self.post_id}, comment='{self.comment}')"