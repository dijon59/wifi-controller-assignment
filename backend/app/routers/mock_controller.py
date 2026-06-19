import json
from pathlib import Path

from fastapi import APIRouter, HTTPException


router = APIRouter(tags=["mock controller"])
MOCK_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "mock_controller.json"
INVALID_MOCK_DATA_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "mock_controller_invalid.json"
)


@router.get("/mock-controller-data")
def get_controller_data(
    simulate_failure: bool = False,
    use_invalid_payload: bool = False,
):
    if simulate_failure:
        raise HTTPException(
            status_code=503,
            detail="Mock controller is temporarily unavailable",
        )

    data_path = INVALID_MOCK_DATA_PATH if use_invalid_payload else MOCK_DATA_PATH

    try:
        with data_path.open(encoding="utf-8") as data_file:
            return json.load(data_file)
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Mock controller data file was not found",
        ) from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=500,
            detail="Mock controller data file is not valid JSON",
        ) from exc
