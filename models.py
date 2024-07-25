
from sqlalchemy import Boolean, Column, Integer, String, Float, UUID
from database import Base


class Book(Base):
    __tabelename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    genre: Column(String(10))
    price: Column(Float)
    book_id: Column(UUID)
    user_id: Column(Integer)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
