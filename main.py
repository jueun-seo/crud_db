from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

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

@app.get('/posts/new')
def post_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='new.html'
    )

@app.post('/posts/create')
def post_create(title: str = Form(), content: str = Form()):
    with Session(engine) as db:
        post=Post(title=title, content=content)
        db.add(post) #db에 저장되는순간 post가 id받음
        db.commit()

        # from fastapi.response import RedirectionResponse
        return RedirectResponse(f'/posts/{post.id}', status_code=303) # post는 방금 생성된 id

@app.get('/posts')
def post_list(request: Request):
    with Session(engine) as db:
        posts = db.scalars(select(Post)).all() #전체데이터조화는 스칼라함수 #Post라는 클래스
        return templates.TemplateResponse(
            request=request,
            name='list.html',
            context={'posts':posts}
        )

@app.get('/posts/{post_id}')
def post_detail(request: Request, post_id: int):
    with Session(engine) as db:
        post = db.get(Post, post_id)

    return templates.TemplateResponse(
        request=request,
        name='detail.html',
        context={'post':post}
    )
