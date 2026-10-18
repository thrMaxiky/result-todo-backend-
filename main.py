import traceback
from fastapi import Request
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI,status
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, mapped_column, DeclarativeBase, Mapped, Session

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind = engine)

# по сути это для использования orm объектов
class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key = True, default = lambda: str(uuid4()))
    # очередное значение по умолчанию
class TaskOrm(Base):
    __tablename__ = "tasks"
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default = False ) # значение по умолчанию для всех объектов
@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind = engine) # создание таблиц
    yield

app = FastAPI(lifespan = lifespan) # это будет наше предложение
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def all_exceptions_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return PlainTextResponse("Internal Server Error", status_code=500)
#@app.get('/')
#def read_base_page(): # все взаимодействие в api происходит через json
#   return {'message': 'Hello World!'}
#uvicorn - asgi приложение, которое служит для связи между http и backend
class ReadTask(BaseModel):
    id: str
    title: str
    completed: bool
class TaskCreate(BaseModel):
    title: str
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None # нужно разобраться зачем вообще так пишут
def get_db(): # ???
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()
def task_orm_to_model(task_orm: TaskOrm)-> ReadTask:
    return ReadTask(id = task_orm.id, title = task_orm.title, completed = task_orm.completed)
@app.get('/tasks')
def read_tasks(db: Session = Depends(get_db)) -> list[ReadTask]:
    task_from_db = db.scalars(select(TaskOrm)).all() #?????
    return [task_orm_to_model(task) for task in task_from_db]
#paylod это тело запроса
@app.post('/tasks')
def create_task(payload: TaskCreate,db: Session = Depends(get_db)) -> ReadTask:
    new_task = TaskOrm(title = payload.title, completed = False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)
@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdate,db: Session = Depends(get_db)):
    task_for_update = db.get(TaskOrm, task_id)
    if payload.title is not None:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed
    db.commit()
    return task_for_update
@app.delete('/tasks/{task_id}')
def delete_task(task_id,db: Session = Depends(get_db)):
    task_for_delete = db.get(TaskOrm, task_id)
    db.delete(task_for_delete)
    db.commit()
    return task_for_delete

# попытка написать категории с нуля второй раз
class CategoryORM(Base):
    __tablename__ = "categories"
    name: Mapped[str]
class ReadCategory(BaseModel):
    id: str
    name: str
class CategoryCreate(BaseModel):
    name: str
class CategoryUpdate(BaseModel):
    name: str | None = None
def category_orm_to_model(category_orm: CategoryORM) -> ReadCategory:
    return ReadCategory(id = category_orm.id, name = category_orm.name)


@app.get('/categories')
def read_categories(db: Session = Depends(get_db)):
    categories_from_db = db.scalars(select(CategoryORM)).all()
    return [category_orm_to_model(category) for category in categories_from_db]


@app.post('/categories')
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    new_category = CategoryORM(name = payload.name)
    db.add(new_category)
    db.commit()
    return new_category


@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category_for_update = db.get(CategoryORM, category_id)
    if payload.name is not None:
        category_for_update.name = payload.name
    db.commit()
    return category_for_update


@app.delete('/categories/{category_id}')
def delete_categories(category_id: str, db: Session = Depends(get_db)):
    category_for_delete = db.get(CategoryORM,category_id)
    db.delete(category_for_delete)
    db.commit()
    return category_for_delete













