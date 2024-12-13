from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from crud import get_all_authors, create_author, get_author_by_name
from database import SessionLocal


#Сінглтон сессії бази даних
app = FastAPI()
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


#Перший параметр - ендпоінт, другий - те що ми очікуємо отримати після виконання запиту
@app.get("/authors", response_model=list[schemas.Author])
async def get_authors(db: Session = Depends(get_db)):
    return get_all_authors(db)

@app.post("/authors", response_model=schemas.Author)
async def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = get_author_by_name(db, author.name)
    if db_author:
        raise HTTPException(status_code=400, detail="Author already registered")
    return create_author(db, author)