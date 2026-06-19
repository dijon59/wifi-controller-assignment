import httpx
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.services import services

router = APIRouter(tags=['sync', 'sync-info'])


@router.post("/sync")
def sync_controller_data(
    simulate_failure: bool = False,
    use_invalid_payload: bool = False,
    db=Depends(get_db),
):
    try:
        response = httpx.get(
            "http://localhost:8000/mock-controller-data",
            params={
                "simulate_failure": simulate_failure,
                "use_invalid_payload": use_invalid_payload,
            },
            timeout=5,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        services.record_failed_sync(
            db,
            "Failed to fetch data from mock controller",
        )
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch data from mock controller",
        ) from exc

    data = response.json()

    try:
        result = services.sync_controller_data(db, data)
    except services.ControllerDataError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except services.SyncFailedError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "status": "success",
        **result,
    }


@router.get("/sync-info")
def fetch_sync_info(page: int = 1, db=Depends(get_db)):
    return services.get_sync_info(db, page=page)
