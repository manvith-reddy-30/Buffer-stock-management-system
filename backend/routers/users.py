from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.schemas import User

from pydantic import BaseModel
from datetime import date

class user(BaseModel):
    govt_id:int
    username:str
    password:str
    user_type :str

class authUser(BaseModel):
    govt_id:int
    password:str

router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message": "FastAPI backend is running."}

@router.post("/newUser")
def create_user(user_data: user, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.govt_id == user_data.govt_id).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists. Please login.")

    entry = User(
        govt_id=user_data.govt_id,
        username=user_data.username,
        password=user_data.password,
        user_type=user_data.user_type
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"message": "User created successfully", "user": {"username": entry.username}}


@router.post("/auth")
def authenticate_user(user_data: authUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.govt_id == user_data.govt_id, User.password == user_data.password).first()
    if user:
        return {"message": "User authenticated successfully", "user": user}
    else:
        raise HTTPException(status_code=404, detail="Invalid username or password")



