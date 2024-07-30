from sqlalchemy import Boolean, Column, Integer, String, Float, UUID
from database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    user_id = Column(Integer)
    price = Column(Float)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
