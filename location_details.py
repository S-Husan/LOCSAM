"""Location detail page."""

import tkinter as tk

from i18n import t
from models import store
from theme import CONTENT_MAX_WIDTH, PAD_LG
from ui_utils import (
    back_button,
    button_row,
    c,
    create_card,
    create_label,
    load_image,
    scrollable_frame,
    star_rating,
    styled_button,
    subtitle_label,
)


class LocationDetailsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.content = tk.Frame(self, bg=c("BACKGROUND"))
        self.content.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.content.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)
        if not loc:
            create_label(self.content, "Location not found.").pack(pady=40)
            return

        back_button(self.content, lambda: self.controller.show_frame("HomeFrame"))

        scroll_container, _, inner = scrollable_frame(self.content)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        col = tk.Frame(inner, bg=c("BACKGROUND"))
        col.pack(anchor="center", padx=PAD_LG)

        img = load_image(loc["image"], size=(min(520, CONTENT_MAX_WIDTH - 80), 280))
        img_lbl = tk.Label(col, image=img, bg=c("BACKGROUND"))
        img_lbl.image = img
        img_lbl.pack(pady=(0, 12))

        create_label(col, loc["name"], style="heading").pack(fill=tk.X)
        create_label(col, loc["city"], style="small").pack(fill=tk.X, pady=(4, 6))
        star_rating(col, loc["rating"], c("BACKGROUND")).pack(anchor="w", pady=(0, 8))
        subtitle_label(col, loc["description"], wrap=520).pack(fill=tk.X, pady=(0, 16))

        info_row = tk.Frame(col, bg=c("BACKGROUND"))
        info_row.pack(fill=tk.X, pady=(0, 16))
        for title, value in [
            (t("open_time"), loc["open_time"]),
            (t("ticket_price"), f"${loc['price']}"),
        ]:
            box = create_card(info_row, padx=14, pady=12)
            box.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=4)
            create_label(box, title, style="tiny", bg=c("CARD")).pack(anchor="w")
            create_label(box, value, style="subheading", bg=c("CARD")).pack(anchor="w")

        create_label(col, t("gallery"), style="subheading").pack(fill=tk.X, pady=(8, 8))
        gallery = tk.Frame(col, bg=c("BACKGROUND"))
        gallery.pack(fill=tk.X, pady=(0, 20))
        for g in store.get_gallery(loc["id"])[:3]:
            gimg = load_image(g["image_path"], size=(150, 110))
            gl = tk.Label(gallery, image=gimg, bg=c("BACKGROUND"))
            gl.image = gimg
            gl.pack(side=tk.LEFT, padx=4)

        btn_row = button_row(col, max_width=520)
        styled_button(
            btn_row,
            t("open_map"),
            command=lambda: self._open_map(loc),
            style="outline",
            width=22,
        ).pack(side=tk.LEFT, padx=4)
        styled_button(
            btn_row,
            t("check_tickets"),
            command=lambda: self._open_tickets(loc),
            style="primary",
            width=22,
        ).pack(side=tk.LEFT, padx=4)

    def _open_map(self, loc):
        self.controller.selected_location_id = loc["id"]
        self.controller.show_frame("MapFrame")

    def _open_tickets(self, loc):
        self.controller.selected_location_id = loc["id"]
        self.controller.show_frame("TicketBookingFrame")
