from fastapi import APIRouter, Depends

from app.api.dependencies import get_category_service
from app.schemas.categories import CategoryCreate, CategoryUpdate, ReadCategory
from app.services.categories import CategoryService

router = APIRouter()


@router.get("/categories")
def read_category(
    category_service: CategoryService = Depends(get_category_service),
) -> list[ReadCategory]:
    return category_service.list_categories()


@router.post("/categories")
def create_category(
    payload: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.create_category(payload)


@router.patch("/categories/{category_id}")
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.update_category(category_id, payload)


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int, category_service: CategoryService = Depends(get_category_service)
):
    return category_service.delete_category(category_id)
