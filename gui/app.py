import customtkinter as ctk

from gui.dashboard_page import DashboardPage
from gui.live_attendance_page import LiveAttendancePage
from gui.login_page import LoginPage
from gui.records_page import RecordsPage
from gui.register_page import RegisterPage


class FaceMarkApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FaceMark — Face Attendance System")
        self.geometry("1280x760")
        self.minsize(1080, 680)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color="#0b0e14")

        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#11151d"
        )
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        self.content.pack(side="right", fill="both", expand=True)

        self.create_sidebar()
        self.show_login()

    def create_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text="FaceMark",
            font=("Segoe UI", 26, "bold"),
            text_color="#7dd3fc"
        ).pack(pady=(30, 35))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Live Attendance", self.show_live_attendance),
            ("Register Person", self.show_register),
            ("Attendance Records", self.show_records)
        ]

        for text, command in buttons:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#1b2230",
                text_color="#d7dce3",
                anchor="w",
                font=("Segoe UI", 15),
                command=command
            ).pack(fill="x", padx=15, pady=6)

        ctk.CTkLabel(
            self.sidebar,
            text="Local & Private",
            text_color="#6b7280",
            font=("Segoe UI", 12)
        ).pack(side="bottom", pady=20)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_content()
        LoginPage(self.content, on_login_success=self.show_dashboard)

    def show_dashboard(self):
        self.clear_content()
        DashboardPage(self.content)

    def show_live_attendance(self):
        self.clear_content()
        LiveAttendancePage(self.content)

    def show_register(self):
        self.clear_content()
        RegisterPage(self.content)

    def show_records(self):
        self.clear_content()
        RecordsPage(self.content)