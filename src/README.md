# Mergington High School Activities API

A FastAPI application that allows students to view and sign up for extracurricular activities.
Data is persisted in a local SQLite database.

## Features

- View all available extracurricular activities
- Sign up for activities
- Unregister from activities
- Data persists across app restarts
- SQL migration bootstrap on startup

## Getting Started

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the application:

   ```
   uvicorn src.app:app --reload
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                            | Description                                                         |
| ------ | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                       | Get all activities with details and current participant list        |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu`  | Sign up a student for an activity                                   |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student from an activity                               |

## Database and Migrations

- Database engine: SQLite (`src/db/school.db`)
- Migration strategy: SQL-file migrations applied automatically at startup
- Migration files location: `src/db/migrations`

Current schema includes these tables:

- `users`
- `activities`
- `activity_participants`
- `clubs` (future-ready)
- `club_memberships` (future-ready)
- `schema_migrations`

When the app starts, it will:

1. Create the database file if it does not exist.
2. Apply all unapplied `.sql` migrations from `src/db/migrations`.
3. Seed default activities and participants only if activities are empty.

## Data Model

The API still exposes activities keyed by activity name and participant email list,
while internally storing normalized records in relational tables.
