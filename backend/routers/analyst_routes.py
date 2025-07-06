from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
from models.schemas import Hyderabad, Medak, RangaReddy, Nalgonda, Warangal, BufferClass

from inference.hyderabad import predict_next_7_days as hyderabad_predict
from inference.medak import predict_next_7_days as medak_predict
from inference.rangareddy import predict_next_7_days as rangareddy_predict
from inference.nalgonda import predict_next_7_days as nalgonda_predict
from inference.warangal import predict_next_7_days as warangal_predict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict

from report.hyderabad import hyderabad_report
from report.warangal import warangal_report
from report.nalgonda import nalgonda_report
from report.medak import medak_report
from report.rangareddy import rangareddy_report
from report.weather import weather_report

router = APIRouter()

class City(BaseModel):
    city: str

class BufferInput(BaseModel):
    warangal_last_week_actual: list[float]
    warangal_next_week_pred: list[float]
    hyderabad_last_week_actual: list[float]
    hyderabad_next_week_pred: list[float]
    nalgonda_last_week_actual: list[float]
    nalgonda_next_week_pred: list[float]
    rangareddy_last_week_actual: list[float]
    rangareddy_next_week_pred: list[float]
    medak_last_week_actual: list[float]
    medak_next_week_pred: list[float]
    buffer_quantity: Dict[str, float]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import func

def fetch_buffer_quantities(db: Session) -> dict[str, float]:
    subquery = (
        db.query(
            BufferClass.place,
            func.max(BufferClass.last_modified_date).label('latest_date')
        )
        .group_by(BufferClass.place)
        .subquery()
    )

    results = (
        db.query(BufferClass)
        .join(subquery, (BufferClass.place == subquery.c.place) & (BufferClass.last_modified_date == subquery.c.latest_date))
        .all()
    )

    buffer_quantity = {}
    for row in results:
        buffer_quantity[row.place.lower()] = row.quantity

    return buffer_quantity


        
@router.get("/test")
def test_analyst():
    return {"message": "Analyst route working"}

@router.post("/predictnext")
def predict_next(city: City, db: Session = Depends(get_db)):
    Query = f"SELECT * FROM {city.city} ORDER BY date DESC LIMIT 30"
    result = db.execute(text(Query)).fetchall()
    if not result:
        return {"message": "No data available for prediction"}
    
    data = [dict(row._mapping) for row in result]
    prices = [row['Price'] for row in data][::-1]
    predictions = []

    if (city.city == "hyderabad"):
        predictions = hyderabad_predict(prices)
    elif (city.city == "medak"):
        predictions = medak_predict(prices)
    elif (city.city == "rangareddy"):
        predictions = rangareddy_predict(prices)
    elif (city.city == "nalgonda"):
        predictions = nalgonda_predict(prices)
    elif (city.city == "warangal"): 
        predictions = warangal_predict(prices)

    return predictions

@router.post("/weather")
async def get_weather(city: City):
    weather_data = await  weather_report(city.city)
    return weather_data
from typing import Dict

@router.post("/buffer/report")
async def get_buffer_report(city: City, db: Session = Depends(get_db)):
    cities = ["warangal", "hyderabad", "nalgonda", "rangareddy", "medak"]
    last_week_actual = {}
    next_week_pred = {}

    for c in cities:
        Query = f"SELECT * FROM {c} ORDER BY date DESC LIMIT 30"
        result = db.execute(text(Query)).fetchall()
        if not result:
            return {"message": f"No data available for {c}"}
        
        data = [dict(row._mapping) for row in result]
        prices = [row['Price'] for row in data][::-1]
        last_week_actual[c] = prices[-7:]  

        if c == "hyderabad":
            pred = hyderabad_predict(prices)
        elif c == "medak":
            pred = medak_predict(prices)
        elif c == "rangareddy":
            pred = rangareddy_predict(prices)
        elif c == "nalgonda":
            pred = nalgonda_predict(prices)
        elif c == "warangal":
            pred = warangal_predict(prices)
        
        next_week_pred[c] = pred

    buffer_quantity = fetch_buffer_quantities(db)
    #print(buffer_quantity)

    response = {
        "warangal_last_week_actual": last_week_actual["warangal"],
        "warangal_next_week_pred": next_week_pred["warangal"],
        "hyderabad_last_week_actual": last_week_actual["hyderabad"],
        "hyderabad_next_week_pred": next_week_pred["hyderabad"],
        "nalgonda_last_week_actual": last_week_actual["nalgonda"],
        "nalgonda_next_week_pred": next_week_pred["nalgonda"],
        "rangareddy_last_week_actual": last_week_actual["rangareddy"],
        "rangareddy_next_week_pred": next_week_pred["rangareddy"],
        "medak_last_week_actual": last_week_actual["medak"],
        "medak_next_week_pred": next_week_pred["medak"],
        "buffer_quantity": buffer_quantity
    }


    if city.city.lower() == "hyderabad":
        report = await hyderabad_report(**response)
    elif city.city.lower() == "warangal":
        report = await warangal_report(**response)
    elif city.city.lower() == "nalgonda":
        report = await nalgonda_report(**response)
    elif city.city.lower() == "medak":
        report = await medak_report(**response)
    elif city.city.lower() == "rangareddy":
        report = await rangareddy_report(**response)
    

    return report
