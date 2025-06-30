# routers/admin_routes.py

from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test_admin():
    return {"message": "Admin route working"}
