from fastapi import APIRouter, Depends
from app.database import get_db
from app.services import services
from sqlalchemy.orm import Session

router = APIRouter(tags=['access_points'])


@router.get("/access_points")
def fetch_access_points(db=Depends(get_db)):
    return services.get_access_points(db)
