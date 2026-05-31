"""LOCSAM — Smart Tourism Management System (UI Demo)."""

import tkinter as tk

from about import AboutFrame
from admin_dashboard import AdminDashboardFrame
from admin_login import AdminLoginFrame
from config import APP_HEIGHT, APP_WIDTH, BACKGROUND
from contact import ContactFrame
from favorites import FavoritesFrame
from home import HomeFrame
from location_details import LocationDetailsFrame
from login import LoginFrame
from map_page import MapFrame
from my_tickets import MyTicketsFrame
from profile import ProfileFrame
from register import RegisterFrame
from search import SearchFrame
from splash import SplashFrame
from ticket_booking import TicketBookingFrame
from ui_utils import ensure_assets


class LocsamApp(tk.Tk):
    """Main application controller with frame-based navigation."""

    def __init__(self):
        super().__init__()
        self.title("LOCSAM — Samarkand Tourism")
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(380, 640)
        self.configure(bg=BACKGROUND)
        self.resizable(True, True)

        self.selected_location_id = 1
        self.search_query = ""

        ensure_assets()

        container = tk.Frame(self, bg=BACKGROUND)
        container.pack(fill=tk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frames = (
            SplashFrame,
            LoginFrame,
            RegisterFrame,
            HomeFrame,
            LocationDetailsFrame,
            TicketBookingFrame,
            MapFrame,
            SearchFrame,
            MyTicketsFrame,
            ProfileFrame,
            FavoritesFrame,
            AboutFrame,
            ContactFrame,
            AdminLoginFrame,
            AdminDashboardFrame,
        )

        self.frames = {}
        for F in frames:
            name = F.__name__
            frame = F(container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SplashFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()


def main():
    app = LocsamApp()
    app.mainloop()


if __name__ == "__main__":
    main()
