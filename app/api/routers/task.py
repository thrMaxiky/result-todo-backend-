from fastapi import APIRouter, Depends

from app.api.dependencies import get_task_service
from app.schemas.task import ReadTask, TaskCreate, TaskUpdate
from app.services.task import TaskService

router = APIRouter()


@router.get("/tasks")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[ReadTask]:
    return task_service.list_tasks()


@router.post("/tasks")
def create_task(
    payload: TaskCreate, task_service: TaskService = Depends(get_task_service)
) -> ReadTask:
    return task_service.create_task(payload)


@router.patch("/tasks/{task_id}")
def update_task(
    task_id: str,
    payload: TaskUpdate,
    task_service: TaskService = Depends(get_task_service),
) -> ReadTask:
    return task_service.update_task(task_id, payload)


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str, task_service: TaskService = Depends(get_task_service)
) -> None:
    return task_service.delete_task(task_id)
