from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
from pydantic import BaseModel
import uvicorn

from report.hyderabad import hyderabad_report
from report.warangal import warangal_report
from report.nalgonda import nalgonda_report
from report.medak import medak_report
from report.rangareddy import rangareddy_report
from report.weather import weather_report

# --------------------- FastAPI Setup ---------------------
app = FastAPI(
    title="Buffer Stock Report & Weather",
    description="Tomato price buffer stock and weather report endpoints for 5 Telangana districts",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------- Request Schema ---------------------
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


# --------------------- Weather Endpoint ---------------------
@app.get("/weather/{place}")
async def get_weather(place: str):
    try:
        report = await weather_report(place.lower())
        return {"place": place, "forecast": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------- Buffer Stock Endpoints ---------------------
@app.post("/analysis/hyderabad")
async def get_hyderabad_report(data: BufferInput):
    report = await hyderabad_report(**data.dict())
    return {"report": report}


@app.post("/analysis/warangal")
async def get_warangal_report(data: BufferInput):
    report = await warangal_report(**data.dict())
    return {"report": report}


@app.post("/analysis/nalgonda")
async def get_nalgonda_report(data: BufferInput):
    report = await nalgonda_report(**data.dict())
    return {"report": report}


@app.post("/analysis/medak")
async def get_medak_report(data: BufferInput):
    report = await medak_report(**data.dict())
    return {"report": report}


@app.post("/analysis/rangareddy")
async def get_rangareddy_report(data: BufferInput):
    report = await rangareddy_report(**data.dict())
    return {"report": report}


# --------------------- Run the app (optional) ---------------------
# Run with: uvicorn test_app:app --reload
if __name__ == "__main__":
    uvicorn.run("test_app:app", host="0.0.0.0", port=9000, reload=True)
