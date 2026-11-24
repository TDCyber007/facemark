import customtkinter as ctk
from database import get_dashboard_stats


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        stats = get_dashboard_stats()

        ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 32, "bold"),
            anchor="w"
        ).pack(fill="x", padx=35, pady=(35, 25))

        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.pack(fill="x", padx=35)

        cards = [
            ("Registered People", stats["total_people"], "#7dd3fc"),
            ("Present Today", stats["present_today"], "#4ade80"),
            ("Absent Today", stats["absent_today"], "#fb7185"),
            ("Attendance Rate", stats["attendance_rate"], "#a78bfa")
        ]

        for title, value, color in cards:
            card = ctk.CTkFrame(
                cards_frame,
                height=150,
                corner_radius=18,
                fg_color="#12161f",
                border_width=1,
                border_color="#232a36"
            )
            card.pack(side="left", padx=10, pady=10, fill="both", expand=True)

            ctk.CTkLabel(
                card,
                text=title,
                text_color="#8b94a6",
                font=("Segoe UI", 13)
            ).pack(pady=(28, 8))

            ctk.CTkLabel(
                card,
                text=str(value),
                text_color=color,
                font=("Segoe UI", 34, "bold")
            ).pack()