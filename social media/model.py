from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

# Abstract base class
class Base(so.DeclarativeBase):
    pass

class Like(Base):
    __tablename__ = "likes"
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    likers: so.Mapped[list["User"]] = so.relationship("User", order_by="(User.name)", back_populates="likes")
    post_id: so.Mapped[Optional[int]] = so.mapped_column(sa.ForeignKey("posts.id"))
    post: so.Mapped[Optional["Post"]] = so.relationship("Post", back_populates="likes")

    def __repr__(self) -> str:
        return f"Like(id={self.id}, post_id={self.post_id})"

class User(Base):
    __tablename__ = 'users'
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    name: so.Mapped[Optional[str]]
    age: so.Mapped[int]
    gender: so.Mapped[Optional[str]]
    nationality: so.Mapped[Optional[str]]
    likes: so.Mapped[list[Like]] = so.relationship("Like", order_by="Like.post_id", back_populates="likers")
    posts: so.Mapped[list["Post"]] = so.relationship("Post", order_by="Post.id", back_populates="user")

    def greeting(self) -> None:
        print(f"Hello, my name is {self.name}")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, age={self.age}, gender={self.gender})"

class Post(Base):
    __tablename__ = "posts"
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    title: so.Mapped[str]
    description: so.Mapped[str]
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("users.id"))
    user: so.Mapped[User] = so.relationship("User", back_populates="posts")
    likes: so.Mapped[list[Like]] = so.relationship("Like", back_populates="post")

    def __repr__(self) -> str:
        return f"Post(id={self.id}, title={self.title}, description={self.description})"
