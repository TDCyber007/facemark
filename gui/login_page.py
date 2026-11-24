import customtkinter as ctk

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent, fg_color="transparent")
        self.on_login_success = on_login_success

        self.pack(fill="both", expand=True)

        card = ctk.CTkFrame(
            self,
            width=380,
            corner_radius=22,
            fg_color="#12161f",
            border_width=1,
            border_color="#232a36"
        )
        card.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            card,
            text="FaceMark",
            font=("Segoe UI", 30, "bold"),
            text_color="#7dd3fc"
        ).pack(pady=(40, 5))

        ctk.CTkLabel(
            card,
            text="Admin Login",
            text_color="#8b94a6",
            font=("Segoe UI", 14)
        ).pack(pady=(0, 30))

        self.username = ctk.CTkEntry(
            card,
            width=280,
            height=45,
            placeholder_text="Username"
        )
        self.username.pack(pady=10)

        self.password = ctk.CTkEntry(
            card,
            width=280,
            height=45,
            placeholder_text="Password",
            show="•"
        )
        self.password.pack(pady=10)

        self.error_label = ctk.CTkLabel(
            card,
            text="",
            text_color="#fb7185",
            font=("Segoe UI", 12)
        )
        self.error_label.pack(pady=5)

        ctk.CTkButton(
            card,
            text="Login",
            width=280,
            height=45,
            corner_radius=12,
            font=("Segoe UI", 15, "bold"),
            command=self.login
        ).pack(pady=20)

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.on_login_success()
        else:
            self.error_label.configure(text="Invalid username or password")