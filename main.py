from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
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
class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None # нужно разобраться зачем вообще так пишут
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
@app.patch('/tasks/{task_id}')
def update_task(task_id: str, payload: TaskUpdate):
    for task in tasks:
        if task.id == task_id:
            if payload.title is not None:
                task.title = payload.title
            if payload.completed is not None:
                task.completed = payload.completed
            return task
        raise HTTPException(status_code=404, detail='Задача не найдена')

@app.delete('/tasks/{task_id}')
def delete_task(task_id):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return task
        raise HTTPException(status_code=404, detail='Задача не найдена')
# напишем теперь код для категорий
class Category(BaseModel):
    id: str
    name: str
class CategoryCreate(BaseModel):
    name: str
class CategoryUpdate(BaseModel):
    name: str | None = None
    id: str | None = None
categories: list[Category] = []
@app.get('/categories')
def read_categories() -> list[Category]:
    return categories
@app.post('/categories')
def got_categories(payload: CategoryCreate) -> Category:
    new_category =Category(id = str(uuid4()),name = payload.name)
    categories.append(new_category)
    return new_category
@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            if payload.name is not None:
                category.name = payload.name
            return category
        raise HTTPException(status_code=404, detail='Задача не найдена')
@app.delete('/categories/{category_id}')
def delete_category(category_id):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return category
        raise HTTPException(status_code=404, detail = 'Задача не найдена')



