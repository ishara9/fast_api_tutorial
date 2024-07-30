import json
import os
from uuid import uuid4
import random
from fastapi.encoders import jsonable_encoder
from mangum import Mangum

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated, Literal, Optional

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# BOOKS_FILE = "books.json"
# BOOKS = []
#
# if os.path.exists(BOOKS_FILE):
#     with open(BOOKS_FILE, "r") as f:
#         BOOKS = json.load(f)

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# handler = Mangum(app)


class BookBase(BaseModel):
    name: str
    price: float
    user_id: int


class UserBase(BaseModel):
    username: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore app!"}


@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    print(user)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return user


@app.post("/books/", status_code=status.HTTP_201_CREATED)
async def create_book(book: BookBase, db: db_dependency):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def find_book(book_id: int, db: db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} is not available")
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int, db: db_dependency):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book {book_id} is not found")
    db.delete(book)
    db.commit()

# @app.get("/random-book")
# async def random_book():
#     return random.choice(BOOKS)


# @app.get("/list-books")
# async def list_books():
#     return {"books": BOOKS}


# @app.get("/book_by_index/{index}")
# async def book_by_index(index: int):
#     if index < len(BOOKS):
#         return BOOKS[index]
#     else:
#         raise HTTPException(404, f"Book index {index} out of range ({len(BOOKS)}).")


# @app.post("/add-book")
# async def add_book(book: models.Book):
#     book.book_id = uuid4().hex
#     json_book = jsonable_encoder(book)
#     BOOKS.append(json_book)
#
#     with open(BOOKS_FILE, "w") as f:
#         json.dump(BOOKS, f)
#
#     return {"book_id": book.book_id}


# @app.get("/get-book")
# async def get_book(book_id: str):
#     for book in BOOKS:
#         if book.book_id == book_id:
#             return book
#
#     raise HTTPException(404, f"Book ID {book_id} not found in database.")
