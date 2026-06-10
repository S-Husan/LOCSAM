"""Map page with coordinates."""

import tkinter as tk
from tkinter import messagebox

from i18n import t
from models import store
from theme import PAD_LG
from ui_utils import (
    back_button,
    button_row,
    c,
    create_card,
    create_label,
    load_image,
    styled_button,
)


class MapFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.body = tk.Frame(self, bg=c("BACKGROUND"))
        self.body.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)
        if not loc:
            return

        back_button(self.body, lambda: self.controller.show_frame("LocationDetailsFrame"))

        col = tk.Frame(self.body, bg=c("BACKGROUND"))
        col.pack(anchor="center", padx=PAD_LG, pady=PAD_LG)

        create_label(col, t("map"), style="heading").pack(anchor="w", pady=(0, 12))

        map_img = load_image("map", size=(480, 300))
        lbl = tk.Label(col, image=map_img, bg=c("BACKGROUND"))
        lbl.image = map_img
        lbl.pack(pady=(0, 16))

        card = create_card(col, padx=18, pady=16)
        card.pack(fill=tk.X, pady=8)

        create_label(
            card,
            f"{loc['name']}\n{loc['city']}",
            style="subheading",
            bg=c("CARD"),
        ).pack(anchor="w")

        create_label(
            card,
            f"Coordinates:\n{loc['latitude']}° N  {loc['longitude']}° E",
            style="small",
            bg=c("CARD"),
        ).pack(anchor="w", pady=(10, 0))

        btn_col = button_row(col)
        styled_button(
            btn_col,
            t("navigate"),
            command=lambda: self._navigate(loc),
            style="primary",
            width=18,
        ).pack(pady=12)

    def _navigate(self, loc):
        messagebox.showinfo(
            "Navigate",
            f"Opening directions to {loc['name']} at "
            f"{loc['latitude']}° N, {loc['longitude']}° E",
        )
