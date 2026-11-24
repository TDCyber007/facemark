import customtkinter as ctk
from database import initialize_database
from gui.app import FaceMarkApp

if __name__ == "__main__":
    initialize_database()
    app = FaceMarkApp()
    app.mainloop()
