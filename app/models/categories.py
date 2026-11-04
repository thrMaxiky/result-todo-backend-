from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CategoryOrm(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


# далее необходимо прописать модель для категорий назовем это этапом номер 2
