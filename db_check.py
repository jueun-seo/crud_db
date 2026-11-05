from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

DB_URL = "postgresql+psycopg://sd4:sd4@localhost:5432/board"
engine = create_engine(DB_URL, echo=True)

class Base():
    pass

class Post(Base):
    __tablename__='posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]

with Session(engine) as db:
    posts = db.scalars(select(post)).all() #조회하는 함수 #sql 에서 select와 select () 같음

    for post in posts:
        print(post.id, post.title, post.content)
