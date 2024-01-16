# Schemas
from books.schemas.books import CreateBook, Book, CUBook
from books.schemas.categories import Category

# Db
from commons.db import db


def get_books(
    q: str = None, categories: list[int] = None, b_id: int = None
) -> list[Book] | Book:
    """Get all the books with the filters

    Args:
        q: name or author to search
        categories: list of categories ids
        b_id: book_id
    """
    s_categories = str(categories)

    db_books = db.sp(
        "crud_get_books",
        [
            f"'{q}'::varchar" if q else "null::varchar",
            f"array{s_categories}::int[]" if categories else "null::int[]",
            f"array[{b_id}]::bigint[]" if b_id else "null::bigint[]",
            f"null::bigint",
        ],
    )

    if not db_books:
        return
    books = [Book(**book) for book in db_books]
    return books[0] if b_id else books


def _create_udpate_books(b_type: CUBook, book: CreateBook, b_id: int = None) -> Book:
    """select params to update or create books

    Args:
        b_type (CUBook): action wanted to execute
        book (CreateBook): book informations
        b_id (int, optional): book id to update. Defaults to None.
    """
    categories = str(book.categories)

    params = [
        f"'{book.name}'::varchar",
        f"'{book.author}'::varchar" if book.author else "null::varchar",
        f"array{categories}::int[]" if book.categories else "null::int[]",
    ]

    if b_type == CUBook.create:
        sp = "crud_create_books"
    else:
        sp = "crud_update_books"
        params = [f"{b_id}::bigint", *params]

    created_book = db.sp(sp, params)[0]
    n_book = Book(**created_book)
    return n_book


def create_books(book: CreateBook) -> Book:
    """create books

    Args:
        book (CreateBook): book information
    """
    return _create_udpate_books(CUBook.create, book)


def udpate_books(b_id: int, book: CreateBook) -> Book:
    """update books and categories

    Args:
        b_id (int): book id
        book (CreateBook): book information
    """
    return _create_udpate_books(CUBook.udpate, book, b_id)


def delete_books(b_id: int) -> None:
    """deactivate books

    Args:
        b_id (int): book id
    """
    db.sp("crud_delete_books", [f"{b_id}::bigint"])


def like_book(b_id: int, u_id: int) -> None:
    """create a user like to a book

    Args:
        b_id (int): book id
        u_id (int): user id
    """
    db.sp("crud_like_books", [f"{b_id}::bigint", f"{u_id}::bigint"])
