from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import admin_routes, analyst_routes
from config.database import engine,Base  
from models.schemas import Hyderabad,Medak,RangaReddy,Nalgonda,Warangal

app = FastAPI(
    title="Tomato Buffer Stock Management System (BSMS)",
    description="FastAPI backend for managing buffer stocks, weather, and tomato price reports.",
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(analyst_routes.router, prefix="/analyst", tags=["Analyst"])


@app.get("/")
def root():
    return {"message": "BSMS FastAPI backend is running."}
