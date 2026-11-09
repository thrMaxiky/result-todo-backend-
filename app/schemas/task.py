from pydantic import BaseModel, ConfigDict


class ReadTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    title: str
    completed: bool


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None
