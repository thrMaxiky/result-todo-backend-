from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.schemas.categories import CategoryCreate, CategoryUpdate
from app.services.categories import CategoryService

# ---------- list ----------


def test_list_categories_returns_pydantic_models(
    category_service: CategoryService,
    category_repository_mock: Mock,
    make_task_category,
) -> None:
    category_repository_mock.get_all_category.return_value = [
        make_task_category("1", "изучить pytest"),
        make_task_category("2", "написать тест для категорий"),
    ]

    result = category_service.list_categories()

    category_repository_mock.get_all_category.assert_called_once()
    assert [c.model_dump() for c in result] == [
        {"id": "1", "name": "изучить pytest"},
        {"id": "2", "name": "написать тест для категорий"},
    ]


def test_list_categories_empty(
    category_service: CategoryService,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_all_category.return_value = []

    assert category_service.list_categories() == []


# ---------- create ----------


def test_create_category_commits_created_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    make_task_category,
) -> None:
    created = make_task_category("1", "Новая задача")
    category_repository_mock.create_category.return_value = created

    result = category_service.create_category(CategoryCreate(name="Новая задача"))

    category_repository_mock.create_category.assert_called_once_with(
        name="Новая задача"
    )
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(created)
    assert result.model_dump() == {"id": "1", "name": "Новая задача"}


# ---------- update ----------


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdate(name="Обновить название"),
            "Обновить название",
            id="with-name",
        ),
        pytest.param(CategoryUpdate(name=None), "Старое имя", id="name-not-provided"),
    ],
)
def test_update_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    make_task_category,
    payload: CategoryUpdate,
    expected_name: str,
) -> None:
    existing = make_task_category("1", "Старое имя")
    category_repository_mock.get_by_id_category.return_value = existing

    result = category_service.update_category("1", payload)

    category_repository_mock.get_by_id_category.assert_called_once_with("1")
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once_with(existing)
    assert result.name == expected_name


def test_update_category_not_found_raises(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id_category.return_value = None

    with pytest.raises(ValueError, match="Category 42 not found"):
        category_service.update_category("42", CategoryUpdate(name="x"))

    db_mock.commit.assert_not_called()


# ---------- delete ----------


def test_delete_category(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
    make_task_category,
) -> None:
    existing = make_task_category("1", "Удаляемая")
    category_repository_mock.get_by_id_category.return_value = existing

    result = category_service.delete_category("1")

    category_repository_mock.get_by_id_category.assert_called_once_with("1")
    db_mock.delete.assert_called_once_with(existing)
    db_mock.commit.assert_called_once()
    assert result is None


def test_delete_category_not_found_raises(
    category_service: CategoryService,
    db_mock: Mock,
    category_repository_mock: Mock,
) -> None:
    category_repository_mock.get_by_id_category.return_value = None

    with pytest.raises(ValueError, match="Category 7 not found"):
        category_service.delete_category("7")

    db_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()


# ---------- схемы ----------


def test_category_create_requires_name() -> None:
    with pytest.raises(ValidationError):
        CategoryCreate()


def test_category_update_allows_missing_name() -> None:
    assert CategoryUpdate().name is None
