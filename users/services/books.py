# Schemas
from users.schemas.books import LikedBooks

# db
from commons.db import db


def get_books(u_id: int) -> LikedBooks:
    """get the user liked books

    Args
        u_id: user_id
    """
    books = db.sp("crud_user_like_books", [f"{u_id}::bigint"])
    books = [LikedBooks(**book) for book in books]
    return books
