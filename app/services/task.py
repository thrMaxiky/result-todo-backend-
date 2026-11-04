from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import ReadTask, TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self):
        tasks_orm = self.task_repository.get_all()
        return [ReadTask.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreate) -> ReadTask:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        self.db.refresh(task_orm)  # подтягивает id из БД
        return ReadTask.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdate) -> ReadTask:
        task_for_update = self.task_repository.get_by_id(task_id)
        if task_for_update is None:
            raise ValueError(f"Task not found: {task_id}")

        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        self.db.commit()
        # на всякий случай, чтобы поля были актуальны
        self.db.refresh(task_for_update)
        return ReadTask.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(task_id)
        if task_for_delete is None:
            raise ValueError(f"Task not found: {task_id}")

        self.db.delete(task_for_delete)
        self.db.commit()
