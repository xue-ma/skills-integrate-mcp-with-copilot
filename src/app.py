"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

from src.activity_repository import ActivityRepository
from src.database import get_connection, init_database

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

init_database()


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    with get_connection() as conn:
        repository = ActivityRepository(conn)
        return repository.list_activities()


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    with get_connection() as conn:
        repository = ActivityRepository(conn)
        try:
            repository.signup(activity_name, email)
            conn.commit()
        except ValueError as exc:
            if str(exc) == "activity_not_found":
                raise HTTPException(status_code=404, detail="Activity not found") from exc
            if str(exc) == "already_signed_up":
                raise HTTPException(
                    status_code=400,
                    detail="Student is already signed up"
                ) from exc
            raise

    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    with get_connection() as conn:
        repository = ActivityRepository(conn)
        try:
            repository.unregister(activity_name, email)
            conn.commit()
        except ValueError as exc:
            if str(exc) == "activity_not_found":
                raise HTTPException(status_code=404, detail="Activity not found") from exc
            if str(exc) == "not_signed_up":
                raise HTTPException(
                    status_code=400,
                    detail="Student is not signed up for this activity"
                ) from exc
            raise

    return {"message": f"Unregistered {email} from {activity_name}"}
