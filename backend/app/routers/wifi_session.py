from fastapi import APIRouter, Depends
from app.database import get_db
from app.services import services
from sqlalchemy.orm import Session

router = APIRouter(tags=['wifi-sessions'])


@router.get("/wifi-sessions")
def fetch_wifi_sessions(
    page: int = 1,
    db=Depends(get_db),
):
    return services.get_wifi_session(db, page=page)
