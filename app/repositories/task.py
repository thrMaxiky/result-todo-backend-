from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskOrm


# чтобы писать сервис нужен готовый класс репозитория
class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self):  # получить все записи
        return self.db.scalars(select(TaskOrm)).all()

    def get_by_id(self, task_id: str) -> TaskOrm | None:
        return self.db.get(TaskOrm, task_id)

    def create(self, title: str):
        new_task = TaskOrm(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, task: TaskOrm) -> None:
        self.db.delete(task)
