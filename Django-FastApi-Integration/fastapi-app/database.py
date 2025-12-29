from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from contextlib import contextmanager

# Base 추가
Base = declarative_base()

# 데이터 베이스 url 설정
SQLALCHEMY_DATABASE_URL = 'sqlite:///./products.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()