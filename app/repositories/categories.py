from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categories import CategoryOrm


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_category(self):
        return self.db.scalars(select(CategoryOrm)).all()

    def get_by_id_category(self, category_id: str):
        return self.db.get(CategoryOrm, category_id)

    def create_category(self, name: str):
        new_category = CategoryOrm(name=name)
        self.db.add(new_category)
        return new_category

    def delete_category(self, category: CategoryOrm):
        return self.db.delete(category)


# этап 3 создание класса репозитория для дальнейшего использования в сервисе
