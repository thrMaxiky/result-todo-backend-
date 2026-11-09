from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import ReadTask, TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    """Задача с указанным id не найдена."""

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id
        super().__init__(f"Task not found: {task_id}")


class TaskService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[ReadTask]:
        tasks_orm = self.task_repository.get_all()
        return [ReadTask.model_validate(task) for task in tasks_orm]

    def create_task(self, task_create: TaskCreate) -> ReadTask:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        self.db.refresh(task_orm)
        return ReadTask.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdate) -> ReadTask:
        task_for_update = self.task_repository.get_by_id(task_id)
        if task_for_update is None:
            raise TaskNotFoundError(task_id)

        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

        self.db.refresh(task_for_update)
        return ReadTask.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self.task_repository.get_by_id(task_id)
        if task_for_delete is None:
            raise TaskNotFoundError(task_id)  # ← было ValueError

        self.db.delete(task_for_delete)
        self.db.commit()
