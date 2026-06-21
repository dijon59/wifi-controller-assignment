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

## Requirements

To run the project, you need:

- Docker Desktop or Docker Engine with Docker Compose.
- Node.js and npm for the React frontend.
- A terminal from the project root directory.

The backend Python runtime and PostgreSQL database run inside Docker, so you do not need to install PostgreSQL or create a local Python virtual environment unless you want to run the backend outside Docker.

Recommended versions:

```text
Docker Compose v2+
Node.js 20+
npm 10+
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
GET  /sync-info?page=1
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

The pagination takes place in the backend, the frontend sends page numbers only:

```text
GET /venues?page=1
GET /wifi-sessions?page=1
GET /sync-info?page=1
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

- The mock third-party controller is implemented inside the same FastAPI app instead of as a separate external service. This keeps the project simple to run while still showing the provider integration boundary.

- The sync process runs synchronously through `POST /sync` instead of using a background worker or queue. For a small assignment this is easier to reason about, but in production I would move longer sync jobs to a background task system.

- The mock provider data is stored in static JSON files. This makes the data easy to inspect and test, but it does not fully represent the unpredictability of a real third-party API.

- Missing required provider fields cause the whole sync to fail and roll back. This protects data consistency.

- Error handling is intentionally basic. Failed sync attempts are logged, but there is no retry logic, alerting, or detailed rejected-record reporting yet.

- The frontend is intentionally simple and focused on clarity rather than heavy styling or complex state management.

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
- Add a bash file that runs all the start up projects command automatically instead of typing them manually. 

## AI Tool Usage

- I used AI tools to help generate dummy data for the mock Wi-Fi controller. 
- I also used AI as a learning assistant to get a quick overview of how FastAPI works, since my background is mainly in Django.
- I used it to assist me with only the css code for speed development of the frontend and also gave me a quick refresher on how React work, specially in terms hooks because the way it is handled in React is different than Angular.


## Missing Feature / Limits

Due to lack of time I quickly focused on the main requirements for the task and could not add unit/integration Test and AI Extension.
