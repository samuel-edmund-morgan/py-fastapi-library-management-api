from datetime import datetime, timezone

from sqlalchemy.orm import Session

from models import DBAuthor, DBBook
from schemas import AuthorCreate, BookCreate


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def get_all_authors(
        db: Session,
        skip: int = 0,
        limit: int = 10
):
    return db.query(DBAuthor).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, author_id: int):
    return db.query(DBAuthor).filter(DBAuthor.id == author_id).first()


#Now work with books


def get_all_books(
        db: Session,
        skip: int = 0,
        limit: int = 10
):
    books = db.query(DBBook).offset(skip).limit(limit).all()
    for book in books:
        if isinstance(book.publication_date, int):
            book.publication_date = datetime.fromtimestamp(book.publication_date, tz=timezone.utc).date()
    return books


def create_book(db: Session, book: BookCreate):
    print(book.publication_date)
    print(type(book.publication_date))
    db_book = DBBook(
        title=book.title,
        summary=book.summary,
        publication_date=int(datetime.combine(book.publication_date, datetime.min.time(), tzinfo= timezone.utc).timestamp()),
        author_id=book.author_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book_by_name(db: Session, title: str):
    return db.query(DBBook).filter(DBBook.title == title).first()

def get_author_books(db: Session, author_id: int):
    return db.query(DBBook).filter(DBBook.author_id == author_id).all()


