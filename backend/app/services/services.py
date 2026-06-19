from datetime import UTC, datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.models import AccessPoint, SyncLog, Venue, WifiSession


PAGE_SIZE = 10


class ControllerDataError(Exception):
    pass


class SyncFailedError(Exception):
    pass


def sync_controller_data(db: Session, data):
    """
    """
    sync_log = SyncLog(status="running", started_at=datetime.now(UTC))
    db.add(sync_log)

    try:
        result = {
            "venues_synced": 0,
            "access_points_synced": 0,
            "sessions_synced": 0,
        }
        access_points_by_controller_id = {}
        provider_access_point_ids = set()
        sync_started_at = sync_log.started_at

        # create venues
        for ctr_venue in data['venues']:

            venue = db.query(Venue).filter(Venue.ctr_venue_id == ctr_venue['id']).first()

            if venue is None:
                venue = Venue(ctr_venue_id=ctr_venue['id'])
                db.add(venue)

            venue.name = ctr_venue['name']
            venue.timezone = ctr_venue['timezone']
            venue.synced_at = sync_started_at

            for ctr_access_point in ctr_venue['access_points']:
                provider_access_point_ids.add(ctr_access_point['id'])
                access_point = db.query(AccessPoint).filter(AccessPoint.ctr_access_point_id == ctr_access_point['id']).first()

                if access_point is None:
                    access_point = AccessPoint(ctr_access_point_id=ctr_access_point['id'])
                    db.add(access_point)

                access_point.name = ctr_access_point['name']
                access_point.mac_address = ctr_access_point['mac_address']
                access_point.status = ctr_access_point['status']
                access_point.venue = venue

                access_points_by_controller_id[ctr_access_point['id']] = access_point
                result["access_points_synced"] += 1

            result["venues_synced"] += 1

        db.flush()

        for ctr_session in data['sessions']:
            access_point = access_points_by_controller_id.get(ctr_session['access_point_id'])

            if access_point is None:
                access_point = db.query(AccessPoint).filter(
                    AccessPoint.ctr_access_point_id == ctr_session['access_point_id']
                ).first()

            if access_point is None:
                raise KeyError("Session references an unknown access point")

            session = db.query(WifiSession).filter(
                WifiSession.ctr_session_id == ctr_session['id']
            ).first()

            if session is None:
                session = WifiSession(ctr_session_id=ctr_session['id'])
                db.add(session)

            session.access_point = access_point
            session.client_mac = ctr_session['client_mac']
            session.started_at = ctr_session['started_at']
            session.ended_at = ctr_session['ended_at']
            session.bytes_received = ctr_session['bytes_received']
            session.bytes_sent = ctr_session['bytes_sent']
            session.synced_at = sync_started_at
            result["sessions_synced"] += 1

        stale_access_points = (
            db.query(AccessPoint)
            .filter(AccessPoint.ctr_access_point_id.notin_(provider_access_point_ids))
            .all()
        )
        for stale_access_point in stale_access_points:
            db.delete(stale_access_point)

        sync_log.status = "success"
        sync_log.finished_at = datetime.now(UTC)
        sync_log.venues_synced = result["venues_synced"]
        sync_log.access_points_synced = result["access_points_synced"]
        sync_log.sessions_synced = result["sessions_synced"]

        db.commit()
        return result
    except (KeyError, TypeError) as exc:
        db.rollback()
        _record_failed_sync(db, sync_log.started_at, "Controller payload is missing required fields")
        raise ControllerDataError("Controller payload is missing required fields") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        _record_failed_sync(db, sync_log.started_at, "Failed to store controller data")
        raise SyncFailedError("Failed to store controller data") from exc


def _record_failed_sync(db: Session, started_at: datetime, message: str):
    failed_log = SyncLog(
        status="failed",
        started_at=started_at,
        finished_at=datetime.now(UTC),
        error_message=message,
    )
    db.add(failed_log)
    db.commit()


def record_failed_sync(db: Session, message: str, started_at: datetime | None = None):
    _record_failed_sync(db, started_at or datetime.now(UTC), message)


def serialize_sync_log(sync_log: SyncLog):
    return {
        "id": sync_log.id,
        "status": sync_log.status,
        "startedAt": sync_log.started_at.isoformat(),
        "finishedAt": sync_log.finished_at.isoformat()
        if sync_log.finished_at
        else None,
        "lastSync": sync_log.finished_at.isoformat() if sync_log.finished_at else None,
        "error": sync_log.error_message,
        "venuesSynced": sync_log.venues_synced,
        "accessPointsSynced": sync_log.access_points_synced,
        "sessionsSynced": sync_log.sessions_synced,
    }


def get_sync_info(db: Session, page):
    page = max(page, 1)
    offset = (page - 1) * PAGE_SIZE
    qs = (
        db.query(SyncLog)
        .order_by(SyncLog.started_at.desc())
    )

    total = qs.count()
    sync_logs = qs.offset(offset).limit(PAGE_SIZE).all()
    latest_sync_log = qs.first()

    if latest_sync_log is None:
        latest = {
            "status": "never_synced",
            "lastSync": "Never synced",
            "error": None,
            "venuesSynced": 0,
            "accessPointsSynced": 0,
            "sessionsSynced": 0,
        }
    else:
        latest = serialize_sync_log(latest_sync_log)

    return {
        "latest": latest,
        "history": [serialize_sync_log(sync_log) for sync_log in sync_logs],
        "total": total,
        "page": page,
        "limit": PAGE_SIZE,
        "offset": offset,
    }


def get_venues(db: Session, page: int = 1):
    page = max(page, 1)
    offset = (page - 1) * PAGE_SIZE
    qs = db.query(Venue).order_by(Venue.synced_at.desc().nullslast(), Venue.name.asc())

    total = qs.count()
    venues = qs.offset(offset).limit(PAGE_SIZE).all()

    return {
        "items": [
            {
                "venue_id": venue.ctr_venue_id,
                "name": venue.name,
                "timezone": venue.timezone,
                "last_synced_at": venue.synced_at.isoformat()
                if venue.synced_at else None,
                "access_points_count": len(venue.access_points),
            }
            for venue in venues
        ],
        "total": total,
        "page": page,
        "limit": PAGE_SIZE,
        "offset": offset,
    }


def get_access_points(db: Session):
    access_points = db.query(AccessPoint).all()

    return [
        {
            "access_point_id": access_point.ctr_access_point_id,
            "name": access_point.name,
            "mac_address": access_point.mac_address,
            "status": access_point.status,
        }
        for access_point in access_points
    ]


def get_wifi_session(db: Session, page: int = 1):
    page = max(page, 1)
    offset = (page - 1) * PAGE_SIZE
    qs = db.query(WifiSession).order_by(
        WifiSession.synced_at.desc().nullslast(),
        WifiSession.started_at.desc(),
    )

    total = qs.count()
    wifi_sessions = qs.offset(offset).limit(PAGE_SIZE).all()

    return {
        "items": [
            {
                "session_id": wifi_session.ctr_session_id,
                "access_point_id": wifi_session.access_point_id,
                "access_point_name": wifi_session.access_point.name,
                "venue_name": wifi_session.access_point.venue.name,
                "client_mac": wifi_session.client_mac,
                "started_at": wifi_session.started_at,
                "ended_at": wifi_session.ended_at,
                "bytes_received": wifi_session.bytes_received,
                "bytes_sent": wifi_session.bytes_sent,
                "last_synced_at": wifi_session.synced_at.isoformat() if wifi_session.synced_at else None,
            }
            for wifi_session in wifi_sessions
        ],
        "total": total,
        "page": page,
        "limit": PAGE_SIZE,
        "offset": offset,
    }
