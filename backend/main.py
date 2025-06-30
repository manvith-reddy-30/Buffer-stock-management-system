from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import your routers (will create these later)
from routers import admin_routes, analyst_routes

app = FastAPI(
    title="Tomato Buffer Stock Management System (BSMS)",
    description="FastAPI backend for managing buffer stocks, weather, and tomato price reports.",
    version="1.0.0",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this in production to specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin_routes.router, prefix="/admin", tags=["Admin"])
app.include_router(analyst_routes.router, prefix="/analyst", tags=["Analyst"])


@app.get("/")
def root():
    return {"message": "BSMS FastAPI backend is running."}
