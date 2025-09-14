from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db, engine
from models import User, UserCreate, UserUpdate, UserResponse

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CSU Page API", description="간단한 CRUD API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "CSU Page API에 오신 것을 환영합니다!"}

# 사용자 생성 (CREATE)
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 이메일 중복 확인
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400, 
            detail="이미 등록된 이메일입니다."
        )
    
    # 새 사용자 생성
    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 모든 사용자 조회 (READ)
@app.get("/users/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# 특정 사용자 조회 (READ)
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail="사용자를 찾을 수 없습니다."
        )
    return user

# 사용자 수정 (UPDATE)
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="사용자를 찾을 수 없습니다."
        )
    
    # 이메일 중복 확인 (다른 사용자가 같은 이메일을 사용하는지)
    if user_update.email and user_update.email != db_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, 
                detail="이미 등록된 이메일입니다."
            )
    
    # 업데이트할 필드만 수정
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

# 사용자 삭제 (DELETE)
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=404, 
            detail="해당 ID의 사용자를 찾을 수 없습니다. ID를 확인해주세요."
        )
    
    db.delete(db_user)
    db.commit()
    return {
        "message": "사용자가 성공적으로 삭제되었습니다.",
        "status": "성공",
        "deleted_user": {
            "id": user_id,
            "name": db_user.name,
            "email": db_user.email
        }
    }

# 이메일로 사용자 검색
@app.get("/users/search/email/{email}")
async def search_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(
            status_code=404, 
            detail="해당 이메일의 사용자를 찾을 수 없습니다. 이메일을 확인해주세요."
        )
    return {
        "message": "이메일로 사용자를 성공적으로 검색했습니다.",
        "status": "성공",
        "data": user
    }