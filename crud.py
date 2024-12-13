from sqlalchemy.orm import Session

from models import DBAuthor
from schemas import AuthorCreate

def get_author_by_name(db: Session, name: str):
    return db.query(DBAuthor).filter(DBAuthor.name == name).first()


def get_all_authors(db: Session):
    return db.query(DBAuthor).all()


def create_author(db: Session, author: AuthorCreate):
    db_author = DBAuthor(
        name=author.name,
        bio=author.bio
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author