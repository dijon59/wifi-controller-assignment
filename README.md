# Bconnect Wi-Fi Controller Integration Dashboard

Mini full-stack application that simulates syncing data from a third-party Guest Wi-Fi controller into a normalized internal database and displaying it in a React dashboard.

## Features

- FastAPI backend
- React frontend
- PostgreSQL database via Docker Compose
- Mock third-party Wi-Fi controller endpoint
- Sync process for venues, access points, and Wi-Fi sessions
- Duplicate prevention using provider/controller IDs
- Sync status and sync history
- Failed sync logging with a simulated controller failure
- Backend pagination for venues and Wi-Fi sessions
- Basic loading and error states in the UI
- Dockerized backend and database

## Architecture

```text
React Dashboard
      |
      v
FastAPI Backend
      |
      +--> Mock Controller API
      |
      +--> Sync Service
              |
              v
          PostgreSQL

PostgreSQL tables:
- venues
- access_points
- wifi_sessions
- sync_logs
```

The mock controller payload is stored as a static JSON file at `backend/app/data/mock_controller.json`.

## Tech Stack

- Backend: FastAPI, SQLAlchemy(ORM)
- Frontend: React
- Database: PostgreSQL 17
- Containerization: Docker Compose

## Project Structure

```text
backend/
  app/
  migrations/
  alembic.ini
  Dockerfile
  requirements.txt

frontend/
  src/
  package.json
  vite.config.js

docker-compose.yml
README.md
```

## Setup And Run

### 1. Start Backend And Database

From the project root:

```bash
docker compose up --build
```

The backend runs at:

```text
http://localhost:8000
```

API docs:

```text
http://localhost:8000/docs
```

### 2. Run Migrations

In another terminal:

```bash
docker compose exec api alembic upgrade head
```

### 3. Start Frontend

From the project root:

```bash
cd frontend
npm install
npm run start
```

The frontend runs at:

```text
http://127.0.0.1:5174
```

## Main API Endpoints

```text
GET  /mock-controller-data
POST /sync
POST /sync?simulate_failure=true
POST /sync?use_invalid_payload=true
GET  /sync-info
GET  /venues?page=1
GET  /wifi-sessions?page=1
GET  /access_points
```

## Sync Flow

```text
POST /sync
  -> fetch mock controller payload
  -> upsert venues by controller venue ID
  -> upsert access points by controller access point ID
  -> upsert Wi-Fi sessions by controller session ID
  -> write sync log
  -> return synced record counts
```

Repeated syncs should not create  duplicates because synced records are matched by provider/controller IDs.

To test failed sync logging, call:

```text
POST /sync?simulate_failure=true
```

This simulates the mock controller being unavailable. The backend returns a `502` and writes a failed row into `sync_logs`, which appears in the sync history table.

To test a provider payload validation failure, call:

```text
POST /sync?use_invalid_payload=true
```

This loads `backend/app/data/mock_controller_invalid.json`, which intentionally misses a required field. The backend returns a `422` and logs the failure in `sync_logs`.

You can test it easily with fast api docs url, you will see a list of all the projects APIs and it also give you the possibility to add query params in APIs. Or you can also use postman. But it is quick and easy to use fast api docs url

```text
http://127.0.0.1:8000/docs

```



## Pagination

The backend owns page size. The frontend sends page numbers only:

```text
GET /venues?page=1
GET /wifi-sessions?page=1
```

Paginated responses include:

```json
{
  "items": [],
  "total": 100,
  "page": 1,
  "limit": 10,
  "offset": 0
}
```

## Assumptions

- The third-party controller is simulated with a mock FastAPI endpoint.
- Mock controller data is loaded from `backend/app/data/mock_controller.json`.
- Provider IDs are stable and can be used to detect existing records.
- PostgreSQL is the target database for the assignment.
- Sync runs synchronously through `POST /sync`; no background worker is used.
- The mock dataset is intentionally simple.
- The mock dataset contains 100 venues, 10 access points, and 100 Wi-Fi sessions.


## Trade-Offs

- The mock controller is hosted inside the same backend app instead of a separate service. This keeps the project small and easy to run.
- Sync is request/response based rather than queued in a background job.
- Error handling is basic but includes rollback and failed sync logging.

## Optional Extensions Implemented

- Backend pagination for venues and Wi-Fi sessions
- Sync log/history table
- Dockerized backend and PostgreSQL
- Basic error handling and failed sync logging


## What I Would Improve With More Time

- Add automated backend tests for sync idempotency and pagination.
- Add retry logic around external controller fetches.
- Add the AI Extension feature for system insight of data loaded from the third-party API(Mock data)
- Add frontend tests for loading, error, and pagination states.
- Add filtering for Wi-Fi sessions by venue, access point, or active/completed status.

## AI Tool Usage

- I used AI tools to help generate dummy data for the mock Wi-Fi controller. 
- I also used AI as a learning assistant to get a quick overview of how FastAPI works, since my background is mainly in Django.
- I used it to assist me with only the css code for speed development of the frontend and also gave me a quick refresher on how React work, specially in terms hooks because the way it is handled in React is different than Angular.


## Missing Feature / Limits

Due to lack of time I quickly focused on the main requirements for the task and could not add unit/integration Test and AI Extension.