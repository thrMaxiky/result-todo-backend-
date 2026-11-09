from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.models.categories import CategoryOrm
from app.models.task import TaskOrm
from app.repositories.categories import CategoryRepository
from app.repositories.task import TaskRepository
from app.services.categories import CategoryService
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.task_repository = repository_mock  # ← исправили имя
    return task_service


@pytest.fixture
def category_repository_mock() -> Mock:
    return Mock(spec=CategoryRepository)


@pytest.fixture
def category_service(db_mock: Mock, category_repository_mock: Mock) -> CategoryService:
    category_service = CategoryService(db_mock)
    category_service.category_repository = category_repository_mock
    return category_service


@pytest.fixture
def make_task():
    def _make(id: str, title: str, completed: bool = False) -> TaskOrm:
        task = TaskOrm(title=title, completed=completed)
        task.id = id  # ← вот здесь обходим default из Base
        return task

    return _make


@pytest.fixture
def make_task_category():
    def _make(id: str, name: str) -> CategoryOrm:
        category = CategoryOrm(name=name)
        category.id = id
        return category

    return _make


# нужно будет разобраться что это такое
