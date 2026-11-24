from database import (
    attendance_exists_today,
    get_known_faces,
    mark_attendance
)
from face_engine import FaceEngine


class AttendanceService:
    def __init__(self, tolerance=0.5):
        self.face_engine = FaceEngine(tolerance=tolerance)

    def process_encoding(self, encoding):
        known_faces = get_known_faces()
        match = self.face_engine.recognize_face(encoding, known_faces)

        if match is None:
            return {
                "status": "unknown",
                "message": "Unknown person"
            }

        person_id = match["person_id"]
        name = match["name"]
        confidence = match["confidence"]

        if attendance_exists_today(person_id):
            return {
                "status": "already_marked",
                "name": name,
                "message": f"{name} is already marked present today"
            }

        marked = mark_attendance(
            person_id=person_id,
            name=name,
            confidence=confidence
        )

        if not marked:
            return {
                "status": "already_marked",
                "name": name,
                "message": f"{name} is already marked present today"
            }

        return {
            "status": "marked",
            "name": name,
            "confidence": confidence,
            "message": f"Attendance marked for {name}"
        }