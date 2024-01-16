# Db
from commons.db import db

# Schemas
from books.schemas.categories import BaseCategory, Category


def get_all_categories(q: str) -> list[Category]:
    """get books categories

    Args:
        q (str): name of category
    """
    db_categories = db.sp(
        "crud_get_categories", [f"'{q}'::varchar" if q else "null::varchar"]
    )
    categories = [Category(**cat) for cat in db_categories]
    return categories


def create_a_category(category: BaseCategory) -> Category:
    """create a new book category

    Args:
        category (BaseCategory): category information
    """
    db_category = db.sp("crud_create_category", [f"'{category.name}'::varchar"])[0]
    category = Category(**db_category)
    return category


def delete_a_category(c_id: int) -> Category:
    """deactivate a category

    Args:
        c_id (int): category id
    """
    db_category = db.sp("crud_delete_categories", [f"{c_id}::bigint"])[0]
    category = Category(**db_category)
    return category
