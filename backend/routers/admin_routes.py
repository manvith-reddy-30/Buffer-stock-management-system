from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.schemas import Hyderabad, Medak, RangaReddy, Nalgonda, Warangal, BufferClass

from pydantic import BaseModel
from datetime import date

class PriceCreate(BaseModel):
    date: date
    price: float

class Buffer(BaseModel):
    city: str
    user_type: str
    quantity: float
    last_modified_date: date

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def root():
    return {"message": "BSMS FastAPI admin backend is running."}

# ----------- HYDERABAD -----------
@router.get("/hyderabad")
def get_hyderabad_prices(db: Session = Depends(get_db)):
    return db.query(Hyderabad).all()

@router.post("/hyderabad")
def add_hyderabad_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    existing = db.query(Hyderabad).filter(Hyderabad.date == price_data.date).first()
    if existing:
        raise HTTPException(status_code=409, detail="Entry for this date already exists")
    entry = Hyderabad(date=price_data.date, price=price_data.price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ----------- MEDAK -----------
@router.get("/medak")
def get_medak_prices(db: Session = Depends(get_db)):
    return db.query(Medak).all()

@router.post("/medak")
def add_medak_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    existing = db.query(Medak).filter(Medak.date == price_data.date).first()
    if existing:
        raise HTTPException(status_code=409, detail="Entry for this date already exists")
    entry = Medak(date=price_data.date, price=price_data.price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ----------- RANGAREDDY -----------
@router.get("/rangareddy")
def get_rangareddy_prices(db: Session = Depends(get_db)):
    return db.query(RangaReddy).all()

@router.post("/rangareddy")
def add_rangareddy_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    existing = db.query(RangaReddy).filter(RangaReddy.date == price_data.date).first()
    if existing:
        raise HTTPException(status_code=409, detail="Entry for this date already exists")
    entry = RangaReddy(date=price_data.date, price=price_data.price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ----------- NALGONDA -----------
@router.get("/nalgonda")
def get_nalgonda_prices(db: Session = Depends(get_db)):
    return db.query(Nalgonda).all()

@router.post("/nalgonda")
def add_nalgonda_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    existing = db.query(Nalgonda).filter(Nalgonda.date == price_data.date).first()
    if existing:
        raise HTTPException(status_code=409, detail="Entry for this date already exists")
    entry = Nalgonda(date=price_data.date, price=price_data.price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

# ----------- WARANGAL -----------
@router.get("/warangal")
def get_warangal_prices(db: Session = Depends(get_db)):
    return db.query(Warangal).all()

@router.post("/warangal")
def add_warangal_price(price_data: PriceCreate, db: Session = Depends(get_db)):
    existing = db.query(Warangal).filter(Warangal.date == price_data.date).first()
    if existing:
        raise HTTPException(status_code=409, detail="Entry for this date already exists")
    entry = Warangal(date=price_data.date, price=price_data.price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.post("/buffer")
def add_buffer_entry(buffer_data: Buffer, db: Session = Depends(get_db)):
    # Check if entry already exists for same place and date
    existing_entry = db.query(BufferClass).filter(
        BufferClass.place == buffer_data.city,
        BufferClass.last_modified_date == buffer_data.last_modified_date
    ).first()
    
    if existing_entry:
        raise HTTPException(status_code=409, detail="Entry already exists for this place and date. Please update instead.")
    
    # Create new entry
    entry = BufferClass(
        place=buffer_data.city,
        user_type=buffer_data.user_type,
        quantity=buffer_data.quantity,
        last_modified_date=buffer_data.last_modified_date
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"message": "Buffer entry created successfully", "data": {
        "place": entry.place,
        "quantity": entry.quantity,
        "date": entry.last_modified_date
    }}
