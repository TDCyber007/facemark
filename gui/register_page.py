from pathlib import Path
import customtkinter as ctk
import cv2
import face_recognition
from PIL import Image

from database import add_person, person_exists, save_face_encoding


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        self.selected_image_path = None

        ctk.CTkLabel(
            self,
            text="Register Person",
            font=("Segoe UI", 32, "bold"),
            anchor="w"
        ).pack(fill="x", padx=35, pady=(35, 10))

        ctk.CTkLabel(
            self,
            text="Register only people who have given consent. Face data stays on this computer.",
            text_color="#8b94a6",
            font=("Segoe UI", 13),
            anchor="w"
        ).pack(fill="x", padx=35, pady=(0, 25))

        form = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#12161f",
            border_width=1,
            border_color="#232a36"
        )
        form.pack(fill="both", expand=True, padx=35, pady=10)

        self.person_id = ctk.CTkEntry(
            form,
            width=340,
            height=45,
            placeholder_text="Person ID"
        )
        self.person_id.pack(pady=12)

        self.name = ctk.CTkEntry(
            form,
            width=340,
            height=45,
            placeholder_text="Full Name"
        )
        self.name.pack(pady=12)

        self.role = ctk.CTkComboBox(
            form,
            width=340,
            height=45,
            values=["Student", "Employee", "Teacher", "Other"]
        )
        self.role.set("Student")
        self.role.pack(pady=12)

        ctk.CTkButton(
            form,
            text="Choose Face Image",
            width=340,
            height=45,
            command=self.choose_image
        ).pack(pady=12)

        self.image_label = ctk.CTkLabel(
            form,
            text="No image selected",
            width=340,
            height=180,
            corner_radius=15,
            fg_color="#0b0e14"
        )
        self.image_label.pack(pady=12)

        self.status_label = ctk.CTkLabel(
            form,
            text="",
            text_color="#4ade80",
            font=("Segoe UI", 13)
        )
        self.status_label.pack(pady=8)

        ctk.CTkButton(
            form,
            text="Register Person",
            width=340,
            height=48,
            font=("Segoe UI", 15, "bold"),
            command=self.register_person
        ).pack(pady=15)

    def choose_image(self):
        path = ctk.filedialog.askopenfilename(
            title="Select face image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png")
            ]
        )

        if not path:
            return

        self.selected_image_path = path

        image = Image.open(path)
        image.thumbnail((340, 180))

        ctk_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(340, 180)
        )

        self.image_label.configure(image=ctk_image, text="")
        self.image_label.image = ctk_image

    def register_person(self):
        person_id = self.person_id.get().strip()
        name = self.name.get().strip()
        role = self.role.get().strip()

        if not person_id or not name or not self.selected_image_path:
            self.status_label.configure(
                text="Please fill all fields and choose an image.",
                text_color="#fb7185"
            )
            return

        if person_exists(person_id):
            self.status_label.configure(
                text="This Person ID already exists.",
                text_color="#fb7185"
            )
            return

        image = face_recognition.load_image_file(self.selected_image_path)
        encoding = face_recognition.face_encodings(image)

        if not encoding:
            self.status_label.configure(
                text="No clear face found. Try another photo.",
                text_color="#fb7185"
            )
            return

        add_person(person_id, name, role)
        save_face_encoding(person_id, encoding[0])

        self.person_id.delete(0, "end")
        self.name.delete(0, "end")

        self.status_label.configure(
            text=f"{name} registered successfully.",
            text_color="#4ade80"
        )