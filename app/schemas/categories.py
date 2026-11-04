from pydantic import BaseModel, ConfigDict


class ReadCategory(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None


# по сути при написании любого проекта начинают писать именно с
# pydantic-схем, пускай это будет этап 1
