"""LOCSAM — Smart Tourism Management System."""

import tkinter as tk

from about import AboutFrame
from admin_dashboard import AdminDashboardFrame
from admin_login import AdminLoginFrame
from config import APP_HEIGHT, APP_WIDTH, MIN_HEIGHT, MIN_WIDTH
from contact import ContactFrame
from favorites import FavoritesFrame
from home import HomeFrame
from i18n import t
from location_details import LocationDetailsFrame
from login import LoginFrame
from map_page import MapFrame
from models import store
from my_tickets import MyTicketsFrame
from profile import ProfileFrame
from register import RegisterFrame
from search import SearchFrame
from splash import SplashFrame
from ticket_booking import TicketBookingFrame
from ui_utils import c, configure_ttk_styles, ensure_assets


class LocsamApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(t("app_title"))
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(bg=c("BACKGROUND"))
        self.resizable(True, True)

        self.selected_location_id = 1
        self.search_query = ""
        self.current_frame_name = "SplashFrame"

        ensure_assets()
        configure_ttk_styles()

        self.container = tk.Frame(self, bg=c("BACKGROUND"))
        self.container.pack(fill=tk.BOTH, expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frame_classes = (
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
        self._build_frames()

        if store.current_user:
            self.show_frame("HomeFrame")
        else:
            self.show_frame("SplashFrame")

    def _build_frames(self):
        for F in self.frame_classes:
            name = F.__name__
            frame = F(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name):
        self.current_frame_name = name
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

    def apply_theme(self):
        """Rebuild all frames so every page picks up the new theme."""
        saved = self.current_frame_name
        for frame in self.frames.values():
            frame.destroy()
        self.frames.clear()
        self.configure(bg=c("BACKGROUND"))
        self.container.configure(bg=c("BACKGROUND"))
        configure_ttk_styles()
        self._build_frames()
        self.show_frame(saved)


def main():
    app = LocsamApp()
    app.mainloop()


if __name__ == "__main__":
    main()
