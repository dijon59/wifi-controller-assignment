from fastapi import APIRouter, Depends
from app.database import get_db
from app.services import services
from sqlalchemy.orm import Session

router = APIRouter(tags=['venues'])


@router.get("/venues")
def fetch_venues(page: int = 1, db = Depends(get_db)):
    return services.get_venues(db, page=page)
