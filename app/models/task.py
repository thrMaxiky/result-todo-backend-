from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TaskOrm(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)
