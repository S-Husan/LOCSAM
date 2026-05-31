"""Location detail page."""

import tkinter as tk

from config import ACCENT, BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT, WHITE
from models import store
from ui_utils import load_image, scrollable_frame, star_rating, styled_button, subtitle_label


class LocationDetailsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.content = tk.Frame(self, bg=BACKGROUND)
        self.content.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.content.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)
        if not loc:
            tk.Label(self.content, text="Location not found.", bg=BACKGROUND).pack()
            return

        back = tk.Label(
            self.content,
            text="← Back",
            fg=PRIMARY,
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        )
        back.pack(anchor="w", padx=16, pady=12)
        back.bind("<Button-1>", lambda e: self.controller.show_frame("HomeFrame"))

        scroll_container, _, inner = scrollable_frame(self.content)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        img = load_image(loc["image"], size=(400, 220))
        img_lbl = tk.Label(inner, image=img, bg=BACKGROUND)
        img_lbl.image = img
        img_lbl.pack(padx=12, pady=(0, 8))

        tk.Label(
            inner,
            text=loc["name"],
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
            anchor="w",
        ).pack(fill=tk.X, padx=16)

        tk.Label(
            inner,
            text=loc["city"],
            font=("Segoe UI", 10),
            fg=TEXT_LIGHT,
            bg=BACKGROUND,
            anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(0, 4))

        star_rating(inner, loc["rating"], BACKGROUND).pack(anchor="w", padx=16, pady=(0, 8))
        subtitle_label(inner, loc["description"]).pack(fill=tk.X, padx=16, pady=(0, 12))

        info_row = tk.Frame(inner, bg=BACKGROUND)
        info_row.pack(fill=tk.X, padx=16, pady=(0, 12))

        for title, value in [("Open Time", loc["open_time"]), ("Ticket Price", f"${loc['price']}")]:
            box = tk.Frame(info_row, bg=CARD, padx=12, pady=10)
            box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)
            tk.Label(box, text=title, font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=CARD).pack(
                anchor="w"
            )
            tk.Label(box, text=value, font=("Segoe UI", 11, "bold"), fg=TEXT, bg=CARD).pack(
                anchor="w"
            )

        tk.Label(
            inner,
            text="Gallery",
            font=("Segoe UI", 14, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
            anchor="w",
        ).pack(fill=tk.X, padx=16, pady=(8, 4))

        gallery = tk.Frame(inner, bg=BACKGROUND)
        gallery.pack(fill=tk.X, padx=12, pady=(0, 16))
        for g in store.get_gallery(loc["id"])[:3]:
            gimg = load_image(g["image_path"], size=(120, 90))
            gl = tk.Label(gallery, image=gimg, bg=BACKGROUND)
            gl.image = gimg
            gl.pack(side=tk.LEFT, padx=4)

        btn_row = tk.Frame(inner, bg=BACKGROUND, padx=16)
        btn_row.pack(fill=tk.X, pady=(0, 24))
        styled_button(
            btn_row,
            "Open Location on Map",
            command=lambda: self._open_map(loc),
            style="secondary",
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))
        styled_button(
            btn_row,
            "Check Ticket Prices",
            command=lambda: self._open_tickets(loc),
        ).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(4, 0))

    def _open_map(self, loc):
        self.controller.selected_location_id = loc["id"]
        self.controller.show_frame("MapFrame")

    def _open_tickets(self, loc):
        self.controller.selected_location_id = loc["id"]
        self.controller.show_frame("TicketBookingFrame")
