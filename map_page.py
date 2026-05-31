"""Map page with coordinates."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from models import store
from ui_utils import load_image, styled_button


class MapFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.body = tk.Frame(self, bg=BACKGROUND)
        self.body.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)
        if not loc:
            return

        back = tk.Label(
            self.body,
            text="← Back",
            fg=PRIMARY,
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        )
        back.pack(anchor="w", padx=16, pady=12)
        back.bind(
            "<Button-1>",
            lambda e: self.controller.show_frame("LocationDetailsFrame"),
        )

        tk.Label(
            self.body,
            text="Map",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", padx=16)

        map_img = load_image("map", size=(380, 280))
        lbl = tk.Label(self.body, image=map_img, bg=BACKGROUND)
        lbl.image = map_img
        lbl.pack(padx=16, pady=12)

        card = tk.Frame(self.body, bg=CARD, padx=16, pady=14)
        card.pack(fill=tk.X, padx=16, pady=8)

        tk.Label(
            card,
            text=f"{loc['name']}\n{loc['city']}",
            font=("Segoe UI", 12, "bold"),
            fg=TEXT,
            bg=CARD,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            card,
            text=f"Coordinates:\n{loc['latitude']}° N  {loc['longitude']}° E",
            font=("Segoe UI", 10),
            fg=TEXT_LIGHT,
            bg=CARD,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        styled_button(
            self.body,
            "Navigate",
            command=lambda: self._navigate(loc),
        ).pack(fill=tk.X, padx=16, pady=20)

    def _navigate(self, loc):
        from tkinter import messagebox

        messagebox.showinfo(
            "Navigate",
            f"Opening directions to {loc['name']} at "
            f"{loc['latitude']}° N, {loc['longitude']}° E",
        )
