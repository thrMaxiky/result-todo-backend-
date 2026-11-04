from sqlalchemy.orm import Session

from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryCreate, CategoryUpdate, ReadCategory


class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def list_categories(self):
        category_orm = self.category_repository.get_all_category()
        return [ReadCategory.model_validate(category) for category in category_orm]

    def create_category(self, category_create: CategoryCreate):
        category_for_create = self.category_repository.create_category(
            name=category_create.name
        )
        self.db.commit()
        self.db.refresh(category_for_create)
        return ReadCategory.model_validate(category_for_create)

    def update_category(
        self,
        category_id: int,
        category_update: CategoryUpdate,
    ):
        category_for_update = self.category_repository.get_by_id_category(category_id)
        if category_for_update is None:
            raise ValueError(f"Category {category_id} not found")

        if category_update.name is not None:
            category_for_update.name = category_update.name
        self.db.commit()
        self.db.refresh(category_for_update)
        return ReadCategory.model_validate(category_for_update)

    def delete_category(self, category_id: int) -> None:
        category_for_delete = self.category_repository.get_by_id_category(category_id)
        if category_for_delete is None:
            raise ValueError(f"Category {category_id} not found")

        self.db.delete(category_for_delete)
        self.db.commit()


# этап номер 4 пишем уже с импортом из предыдущих файлов
