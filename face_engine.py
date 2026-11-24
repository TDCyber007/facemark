import face_recognition
import numpy as np


class FaceEngine:
    def __init__(self, tolerance=0.5):
        self.tolerance = tolerance

    def get_encoding_from_image(self, image):
        encodings = face_recognition.face_encodings(image)

        if not encodings:
            return None

        return encodings[0]

    def recognize_face(self, unknown_encoding, known_faces):
        if unknown_encoding is None or not known_faces:
            return None

        known_encodings = [
            np.frombuffer(face["encoding"], dtype=np.float64)
            for face in known_faces
        ]

        matches = face_recognition.compare_faces(
            known_encodings,
            unknown_encoding,
            tolerance=self.tolerance
        )

        face_distances = face_recognition.face_distance(
            known_encodings,
            unknown_encoding
        )

        best_match_index = np.argmin(face_distances)

        if not matches[best_match_index]:
            return None

        matched_face = known_faces[best_match_index]

        return {
            "person_id": matched_face["person_id"],
            "name": matched_face["name"],
            "confidence": round((1 - face_distances[best_match_index]) * 100, 2)
        }