from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.schemas import Hyderabad, Medak, RangaReddy, Nalgonda, Warangal

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

@router.get("/hyderabad")
def get_hyderabad_prices(db: Session = Depends(get_db)):
    return db.query(Hyderabad).all()

@router.post("/hyderabad")
def add_hyderabad_price(date: str, price: float, db: Session = Depends(get_db)):
    entry = Hyderabad(date=date, price=price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/medak")
def get_medak_prices(db: Session = Depends(get_db)):
    return db.query(Medak).all()

@router.post("/medak")
def add_medak_price(date: str, price: float, db: Session = Depends(get_db)):
    entry = Medak(date=date, price=price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/rangareddy")
def get_rangareddy_prices(db: Session = Depends(get_db)):
    return db.query(RangaReddy).all()

@router.post("/rangareddy")
def add_rangareddy_price(date: str, price: float, db: Session = Depends(get_db)):
    entry = RangaReddy(date=date, price=price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/nalgonda")
def get_nalgonda_prices(db: Session = Depends(get_db)):
    return db.query(Nalgonda).all()

@router.post("/nalgonda")
def add_nalgonda_price(date: str, price: float, db: Session = Depends(get_db)):
    entry = Nalgonda(date=date, price=price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/warangal")
def get_warangal_prices(db: Session = Depends(get_db)):
    return db.query(Warangal).all()

@router.post("/warangal")
def add_warangal_price(date: str, price: float, db: Session = Depends(get_db)):
    entry = Warangal(date=date, price=price)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry