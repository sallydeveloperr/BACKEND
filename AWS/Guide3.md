# Guide2번까지 실습한후...  ec2 + RDS 

# 가상환경생성
```
   # 기존 venv 삭제 (선택사항)
    rm -rf venv
   
    # Python 3.11로 가상환경 생성
    python3.11 -m venv venv

  2. 가상환경 활성화
    source venv/bin/activate

  3. 버전 확인
  활성화된 상태에서 아래 명령어를 쳤을 때 Python 3.11.x가 나오면 성공입니다.

 4. 라이브러리 설치
 pip install fastapi uvicorn sqlalchemy pymysql pydantic dotenv
   python --version
```


fastapi_main.py
```
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy import create_engine,Column, Integer, String,DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os
load_dotenv()

# RDS 정보 입력
RDS_HOST=os.getenv('RDS_HOST')
RDS_USER=os.getenv('RDS_USER')
RDS_PASSWORD=os.getenv('RDS_PASSWORD')
RDS_DB_NAME=os.getenv('RDS_DB_NAME')
RDS_PORT=os.getenv('RDS_PORT')

DATABASE_URL = f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False ,bind=engine)
Base = declarative_base()

# DB 모델
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(20), default='member')
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)

# pydantic 모델
class UserCreate(BaseModel):
    name:str
    email:str
    role:str = 'member'
class UserUpdate(BaseModel):
    name:str | None = None    
    role:str | None = None

class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    role:str
    created_at:datetime
    class config:
        from_attributes = True
# FastAPI 앱
app = FastAPI()
# DB 접속 function - 공통
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/',summary='헬스체크')
def read_root():
    return {'status':'ok','time':datetime.now()}

#사용자 생성
@app.post('/users', response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail='이미 존재하는 사용자입니다.')
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#사용자 목록 조회
#사용자 검색
#사용자 정보 수정
#사용자 정보 삭제
       
```

# 실행
uvicorn fastapi_main:app --host 0.0.0.0 --port 8000 --reload
