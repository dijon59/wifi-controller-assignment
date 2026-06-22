import os

from fastapi import FastAPI

from app.routers import access_point, health, mock_controller, sync, venue, wifi_session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Bconnect Wi-Fi Controller API",
    version="0.1.0",
)

allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5174,http://127.0.0.1:5174",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(mock_controller.router)
app.include_router(sync.router)
app.include_router(venue.router)
app.include_router(access_point.router)
app.include_router(wifi_session.router)
