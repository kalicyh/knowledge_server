from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Database configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define your SQLAlchemy models
class Record(Base):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True)
    month = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)
    text = Column(String(5000))

class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    last_updated = Column(String(20))
    total_rows = Column(Integer)

class Number(Base):
    __tablename__ = 'numbers'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String(255), nullable=True)
    text = Column(String(5000))

class NumberInfo(Base):
    __tablename__ = 'numbers_info'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(5000))

Base.metadata.create_all(bind=engine)
