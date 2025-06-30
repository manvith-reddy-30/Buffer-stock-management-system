# routers/analyst_routes.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test_analyst():
    return {"message": "Analyst route working"}
