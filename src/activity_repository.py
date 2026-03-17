"""Repository layer for activity reads and enrollment writes."""

from __future__ import annotations

import sqlite3


class ActivityRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def list_activities(self) -> dict[str, dict]:
        rows = self.conn.execute(
            """
            SELECT
                a.name,
                a.description,
                a.schedule,
                a.max_participants,
                u.email AS participant_email
            FROM activities a
            LEFT JOIN activity_participants ap ON ap.activity_id = a.id
            LEFT JOIN users u ON u.id = ap.user_id
            ORDER BY a.name, u.email
            """
        ).fetchall()

        result: dict[str, dict] = {}
        for row in rows:
            activity_name = row["name"]
            if activity_name not in result:
                result[activity_name] = {
                    "description": row["description"],
                    "schedule": row["schedule"],
                    "max_participants": row["max_participants"],
                    "participants": [],
                }

            if row["participant_email"]:
                result[activity_name]["participants"].append(row["participant_email"])

        return result

    def signup(self, activity_name: str, email: str) -> None:
        activity = self.conn.execute(
            "SELECT id FROM activities WHERE name = ?", (activity_name,)
        ).fetchone()
        if not activity:
            raise ValueError("activity_not_found")

        user = self.conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            self.conn.execute(
                "INSERT INTO users(email, display_name) VALUES (?, ?)",
                (email, email.split("@")[0].replace(".", " ").title()),
            )
            user = self.conn.execute(
                "SELECT id FROM users WHERE email = ?", (email,)
            ).fetchone()

        existing_signup = self.conn.execute(
            """
            SELECT 1
            FROM activity_participants
            WHERE activity_id = ? AND user_id = ?
            """,
            (activity["id"], user["id"]),
        ).fetchone()
        if existing_signup:
            raise ValueError("already_signed_up")

        self.conn.execute(
            "INSERT INTO activity_participants(activity_id, user_id) VALUES (?, ?)",
            (activity["id"], user["id"]),
        )

    def unregister(self, activity_name: str, email: str) -> None:
        activity = self.conn.execute(
            "SELECT id FROM activities WHERE name = ?", (activity_name,)
        ).fetchone()
        if not activity:
            raise ValueError("activity_not_found")

        user = self.conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if not user:
            raise ValueError("not_signed_up")

        deleted = self.conn.execute(
            """
            DELETE FROM activity_participants
            WHERE activity_id = ? AND user_id = ?
            """,
            (activity["id"], user["id"]),
        )
        if deleted.rowcount == 0:
            raise ValueError("not_signed_up")
