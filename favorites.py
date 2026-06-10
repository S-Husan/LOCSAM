"""Saved places / favorites page."""

import tkinter as tk

from i18n import t
from models import store
from theme import PAD_LG
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    load_image,
    page_header,
    star_rating,
)


class FavoritesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller

        page_header(self, t("saved_places"))

        from ui_utils import scrollable_frame

        scroll_container, _, self.list_frame = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=8)

        bottom_nav(
            self,
            [
                ("🏠", t("home")),
                ("🔍", t("search")),
                ("🎫", t("tickets")),
                ("❤", t("saved")),
                ("👤", t("profile")),
            ],
            3,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def on_show(self):
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        wrap = tk.Frame(self.list_frame, bg=c("BACKGROUND"))
        wrap.pack(anchor="center", fill=tk.X)

        favorites = store.get_favorites()
        if not favorites:
            create_label(
                wrap,
                t("no_saved"),
                style="body",
                justify="center",
            ).pack(pady=60)
            return

        for loc in favorites:
            card = create_card(wrap, padx=12, pady=10)
            card.pack(fill=tk.X, padx=4, pady=6)
            card.config(cursor="hand2")

            inner = tk.Frame(card, bg=c("CARD"))
            inner.pack(fill=tk.X)

            img = load_image(loc["image"], size=(96, 72))
            img_lbl = tk.Label(inner, image=img, bg=c("CARD"))
            img_lbl.image = img
            img_lbl.pack(side=tk.LEFT, padx=(0, 12))

            info = tk.Frame(inner, bg=c("CARD"))
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            create_label(info, loc["name"], style="subheading", bg=c("CARD")).pack(
                anchor="w"
            )
            star_rating(info, loc["rating"], c("CARD")).pack(anchor="w", pady=(2, 0))

            remove = tk.Label(
                inner,
                text="✕",
                font=("Segoe UI", 14),
                fg=c("DANGER"),
                bg=c("CARD"),
                cursor="hand2",
                padx=12,
            )
            remove.pack(side=tk.RIGHT)

            def open_detail(_=None, lid=loc["id"]):
                self.controller.selected_location_id = lid
                self.controller.show_frame("LocationDetailsFrame")

            def remove_fav(e, lid=loc["id"]):
                store.toggle_favorite(lid)
                self._refresh()

            for w in (card, inner, img_lbl, info):
                w.bind("<Button-1>", open_detail)
            remove.bind("<Button-1>", remove_fav)
