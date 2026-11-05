from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

DB_URL = "postgresql+psycopg://sd4:sd4@localhost:5432/board"
engine = create_engine(DB_URL)
# engine = create_engine(DB_URL, echo=True)

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get('/')
def home():
    return {'hello': 'hi'}

@app.get('/posts')
def post_list(request: Request):
    with Session(engine) as db:
        posts=db.scalars(select(Post)).all #전체데이터조화는 스칼라함수 #Post라는 클래스
        return templates.TemplateResponse(
            request=request,
            name='list.html',
            context={'posts':posts}
        )