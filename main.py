from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI() # это будет наше предложение

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


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

class BookUpdate(BaseModel):
    book: str


tasks: list[ReadTask] = []

book: str = '' # добавил глобальную переменную book
@app.get('/tasks')
def read_tasks() -> list[ReadTask]:
    return tasks
#paylod это тело запроса
@app.post('/tasks')
def got_task(payload: TaskCreate) -> ReadTask:
    new_task = ReadTask(id=str(uuid4()),title = payload.title, completed = False)
    tasks.append(new_task)
    return new_task

@app.get('/book')
def read_book():
    return f'Любимая книга: {book}'


@app.post('/book')
def got_book(payload: BookUpdate):
    global book
    book = payload.book
    return book

