import threading
import customtkinter as ctk
import cv2
import face_recognition
from PIL import Image

from attendance import AttendanceService


class LiveAttendancePage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.camera = None
        self.is_running = False
        self.attendance_service = AttendanceService(tolerance=0.5)

        ctk.CTkLabel(
            self,
            text="Live Attendance",
            font=("Segoe UI", 32, "bold"),
            anchor="w"
        ).pack(fill="x", padx=35, pady=(35, 20))

        self.camera_label = ctk.CTkLabel(
            self,
            text="",
            width=760,
            height=480,
            corner_radius=20,
            fg_color="#0b0e14"
        )
        self.camera_label.pack(pady=10)

        self.status_label = ctk.CTkLabel(
            self,
            text="Camera stopped",
            text_color="#8b94a6",
            font=("Segoe UI", 16)
        )
        self.status_label.pack(pady=12)

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(pady=10)

        ctk.CTkButton(
            controls,
            text="Start Camera",
            width=170,
            height=45,
            command=self.start_camera
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            controls,
            text="Stop Camera",
            width=170,
            height=45,
            fg_color="#fb7185",
            hover_color="#e05b6d",
            command=self.stop_camera
        ).pack(side="left", padx=8)

    def start_camera(self):
        if self.is_running:
            return

        self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.status_label.configure(
                text="Camera not available",
                text_color="#fb7185"
            )
            return

        self.is_running = True
        self.status_label.configure(
            text="Camera running. Look at the camera.",
            text_color="#4ade80"
        )

        threading.Thread(target=self.update_camera, daemon=True).start()

    def stop_camera(self):
        self.is_running = False

        if self.camera:
            self.camera.release()
            self.camera = None

        self.camera_label.configure(image=None, text="Camera stopped")
        self.status_label.configure(
            text="Camera stopped",
            text_color="#8b94a6"
        )

    def update_camera(self):
        while self.is_running and self.camera:
            success, frame = self.camera.read()

            if not success:
                break

            frame = cv2.flip(frame, 1)
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations
            )

            for (top, right, bottom, left), encoding in zip(
                face_locations,
                face_encodings
            ):
                result = self.attendance_service.process_encoding(encoding)

                if result["status"] == "marked":
                    color = (0, 255, 0)
                elif result["status"] == "already_marked":
                    color = (0, 200, 255)
                else:
                    color = (0, 0, 255)

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                label = result.get("name", "Unknown")
                cv2.rectangle(
                    frame,
                    (left, bottom - 35),
                    (right, bottom),
                    color,
                    cv2.FILLED
                )

                cv2.putText(
                    frame,
                    label,
                    (left + 6, bottom - 8),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (20, 20, 20),
                    2
                )

                self.after(
                    0,
                    lambda message=result["message"]: self.status_label.configure(
                        text=message,
                        text_color="#4ade80"
                        if result["status"] == "marked"
                        else "#fbbf24"
                    )
                )

            rgb_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_display)
            image.thumbnail((760, 480))

            ctk_image = ctk.CTkImage(
                light_image=image,
                dark_image=image,
                size=image.size
            )

            self.after(
                0,
                lambda img=ctk_image: self.camera_label.configure(
                    image=img,
                    text=""
                )
            )

        self.stop_camera()