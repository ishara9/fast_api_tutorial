from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_USER = 'root'
DATABASE_PASSWORD = 'admin'
DATABASE_HOST = 'localhost'  # Container name or IP address
DATABASE_PORT = '3306'
DATABASE_NAME = 'BookApp'

URL_DATABASE = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bund=engine)

Base = declarative_base()
