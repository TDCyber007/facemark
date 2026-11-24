import sqlite3
from datetime import date, datetime
from pathlib import Path

DB_PATH = Path("data/attendance.db")
DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS face_encodings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT NOT NULL,
                encoding BLOB NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (person_id) REFERENCES people(person_id)
            );

            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id TEXT NOT NULL,
                name TEXT NOT NULL,
                attendance_date TEXT NOT NULL,
                check_in TEXT NOT NULL,
                confidence REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (person_id) REFERENCES people(person_id),
                UNIQUE (person_id, attendance_date)
            );
            """
        )


def add_person(person_id, name, role):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO people (person_id, name, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (person_id, name, role, datetime.now().isoformat())
        )


def person_exists(person_id):
    with get_connection() as connection:
        result = connection.execute(
            "SELECT 1 FROM people WHERE person_id = ?",
            (person_id,)
        ).fetchone()

    return result is not None


def get_all_people():
    with get_connection() as connection:
        return connection.execute(
            """
            SELECT person_id, name, role, created_at
            FROM people
            ORDER BY name ASC
            """
        ).fetchall()


def save_face_encoding(person_id, encoding):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO face_encodings (person_id, encoding, created_at)
            VALUES (?, ?, ?)
            """,
            (person_id, encoding.tobytes(), datetime.now().isoformat())
        )


def get_known_faces():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                people.person_id,
                people.name,
                face_encodings.encoding
            FROM people
            JOIN face_encodings
                ON people.person_id = face_encodings.person_id
            """
        ).fetchall()

    return [
        {
            "person_id": row["person_id"],
            "name": row["name"],
            "encoding": row["encoding"]
        }
        for row in rows
    ]


def mark_attendance(person_id, name, confidence, status="Present"):
    today = date.today().isoformat()
    now = datetime.now().strftime("%H:%M:%S")

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO attendance
                    (person_id, name, attendance_date, check_in, confidence, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (person_id, name, today, now, confidence, status)
            )

        return True

    except sqlite3.IntegrityError:
        return False


def attendance_exists_today(person_id):
    today = date.today().isoformat()

    with get_connection() as connection:
        result = connection.execute(
            """
            SELECT 1 FROM attendance
            WHERE person_id = ? AND attendance_date = ?
            """,
            (person_id, today)
        ).fetchone()

    return result is not None


def get_attendance_records(search="", selected_date=None):
    query = """
        SELECT
            attendance.id,
            attendance.person_id,
            attendance.name,
            attendance.attendance_date,
            attendance.check_in,
            attendance.confidence,
            attendance.status
        FROM attendance
        WHERE 1 = 1
    """
    parameters = []

    if search:
        query += " AND (attendance.name LIKE ? OR attendance.person_id LIKE ?)"
        search_value = f"%{search}%"
        parameters.extend([search_value, search_value])

    if selected_date:
        query += " AND attendance.attendance_date = ?"
        parameters.append(selected_date)

    query += " ORDER BY attendance.attendance_date DESC, attendance.check_in DESC"

    with get_connection() as connection:
        return connection.execute(query, parameters).fetchall()


def get_dashboard_stats():
    today = date.today().isoformat()

    with get_connection() as connection:
        total_people = connection.execute(
            "SELECT COUNT(*) AS total FROM people"
        ).fetchone()["total"]

        present_today = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM attendance
            WHERE attendance_date = ?
            """,
            (today,)
        ).fetchone()["total"]

    absent_today = max(0, total_people - present_today)
    attendance_rate = (
        round((present_today / total_people) * 100, 1)
        if total_people > 0
        else 0
    )

    return {
        "total_people": total_people,
        "present_today": present_today,
        "absent_today": absent_today,
        "attendance_rate": f"{attendance_rate}%"
    }


def delete_person(person_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM face_encodings WHERE person_id = ?",
            (person_id,)
        )

        connection.execute(
            "DELETE FROM attendance WHERE person_id = ?",
            (person_id,)
        )

        connection.execute(
            "DELETE FROM people WHERE person_id = ?",
            (person_id,)
        )