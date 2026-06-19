from datetime import datetime

from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

STRING_FIELD= String(255)

class Venue(Base):
    __tablename__ = "venues"

    id: Mapped[int] = mapped_column(primary_key=True)
    ctr_venue_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(STRING_FIELD, nullable=False)
    timezone: Mapped[str] = mapped_column(STRING_FIELD)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    access_points: Mapped[list["AccessPoint"]] = relationship(back_populates="venue", cascade="all, delete-orphan")


class AccessPoint(Base):
    __tablename__ = "access_points"

    id: Mapped[int] = mapped_column(primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"))
    name: Mapped[str] = mapped_column(STRING_FIELD)
    ctr_access_point_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
    )
    mac_address: Mapped[str] = mapped_column(STRING_FIELD)
    status: Mapped[str] = mapped_column(STRING_FIELD)
    venue: Mapped["Venue"] = relationship(back_populates="access_points")
    wifi_sessions: Mapped[list["WifiSession"]] = relationship(
        back_populates="access_point",
        cascade="all, delete-orphan",
    )


class WifiSession(Base):
    __tablename__ = 'wifi_sessions'

    id: Mapped[int] = mapped_column(primary_key=True)
    ctr_session_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    access_point_id: Mapped[int] = mapped_column(
        ForeignKey("access_points.id"),
        index=True,
    )
    client_mac: Mapped[str] = mapped_column(STRING_FIELD)
    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    ended_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    bytes_received: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    bytes_sent: Mapped[BigInteger] = mapped_column(BigInteger, default=0)
    synced_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    access_point: Mapped["AccessPoint"] = relationship(back_populates='wifi_sessions')


class SyncLog(Base):
    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    venues_synced: Mapped[int] = mapped_column(default=0)
    access_points_synced: Mapped[int] = mapped_column(default=0)
    sessions_synced: Mapped[int] = mapped_column(default=0)
