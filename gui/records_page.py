from datetime import date
import customtkinter as ctk
from database import get_attendance_records


class RecordsPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(
            self,
            text="Attendance Records",
            font=("Segoe UI", 32, "bold"),
            anchor="w"
        ).pack(fill="x", padx=35, pady=(35, 20))

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=35, pady=(0, 15))

        self.search_entry = ctk.CTkEntry(
            controls,
            width=300,
            height=42,
            placeholder_text="Search by name or ID"
        )
        self.search_entry.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            controls,
            text="Search",
            width=110,
            height=42,
            command=self.load_records
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            controls,
            text="Refresh",
            width=110,
            height=42,
            command=self.load_records
        ).pack(side="left")

        self.table_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=18,
            fg_color="#12161f"
        )
        self.table_frame.pack(fill="both", expand=True, padx=35, pady=10)

        self.load_records()

    def load_records(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        records = get_attendance_records(
            search=self.search_entry.get().strip()
        )

        headers = ["ID", "Name", "Date", "Check-in", "Confidence", "Status"]

        for column, header in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Segoe UI", 14, "bold"),
                text_color="#7dd3fc"
            ).grid(
                row=0,
                column=column,
                padx=18,
                pady=12,
                sticky="w"
            )

        if not records:
            ctk.CTkLabel(
                self.table_frame,
                text="No attendance records found.",
                text_color="#8b94a6"
            ).grid(row=1, column=0, columnspan=6, pady=30)

            return

        for row, record in enumerate(records, start=1):
            values = [
                record["person_id"],
                record["name"],
                record["attendance_date"],
                record["check_in"],
                f"{record['confidence']}%",
                record["status"]
            ]

            for column, value in enumerate(values):
                ctk.CTkLabel(
                    self.table_frame,
                    text=str(value),
                    font=("Segoe UI", 13)
                ).grid(
                    row=row,
                    column=column,
                    padx=18,
                    pady=8,
                    sticky="w"
                )