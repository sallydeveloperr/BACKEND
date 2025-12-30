from fastapi import FastAPI,Depends,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware   #  Django(8000) 와 FastAPI(8001) 연동시 필요  CORS 문제 해결
from sqlalchemy.orm import Session 
from typing import List
import models
import schemas
from database import engine, get_db
from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    check_permission,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# 테이블 생성
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Product API",
    description='제품관리',
    version='1.0.0'
)

# CROS 설정 - Django 와 FastAPI 연동시 필요
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000","http://127.0.0.1:8000"],
    allow_credentials=True, # 쿠키, 인증정보 허용
    allow_methods=["*"], # 모든 메서드 허용  GET POST PUT DELETE
    allow_headers=["*"], # 모든 헤더 허용 Authorization, Content-Type ...
)


# 라우터 설정
@app.get('/')
def root():
    return {
        "message": "Product API",
        'docs': '/docs',
        'endpoints' : {
            'products' : '/api/products',
            'product':'/api/products/{id}',
            'register':'/api/auth/register',
            'login':'/api/auth/token',
            'me':'/api/auth/me'
        }
    }
# 인증관련
@app.post('/api/auth/register',response_model=schemas.User,status_code=status.HTTP_201_CREATED)
def register_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    '''사용자 등록'''
    # 중복체크
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username {user.username} is already registered"
        )
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"email {user.email} is already registered"
        )
    # 사용자 생성
    hashed_password =  get_password_hash(user.password)
    db_user =  models.User(
        username = user.username,
        email = user.email,
        full_name = user.full_name,
        hashed_password = hashed_password,
        role = user.role    
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 제품 목록 조회
#response_model 
    # 반환데이터 자동검증
    # ORM 모델 -> JSON 변환
    # Swagger 문서 자동생성
@app.get("/api/products",response_model=List[schemas.Product])
def get_products(
    skip:int = 0,
    limit:int = 100,
    db:Session=Depends(get_db)  # 함수실행이 끝나면 DB 세션 자동 종료
):
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products

# 제품 상세 조회
@app.get("/api/products/{product_id}",response_model=schemas.Product)
def get_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    return product

# 제품생성
# 성공하면 HTTP_201_CREATED  상태 코드
@app.post("/api/products",response_model=schemas.Product,status_code=status.HTTP_201_CREATED)
def create_product(product:schemas.ProductCreate, db:Session=Depends(get_db)):
    db_product = models.Product(**product.model_dump())
    # db에 저장
    db.add(db_product)  # db 세션에 저장
    db.commit()   # 실제 db에 insert
    db.refresh(db_product)  # 방금 저장된 데이터를 다시 조회
    return db_product

# 제품 수정
@app.put("/api/products/{product_id}",response_model=schemas.Product)
def update_product(product_id:int, product:schemas.ProductUpdate,db:Session=Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    update_product =  product.model_dump(exclude_unset=True)  # 전달된 필드만 업데이트
    for key,value in update_product.items():
        setattr(db_product,key,value)  # 동적으로 속성 설정  변경감지 기능이 있어서 업데이트된 필드만 반영
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/api/products/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id:int, db:Session=Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product not found with id {product_id}"
        )
    db.delete(product)
    db.commit()
    return None