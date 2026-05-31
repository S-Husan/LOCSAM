"""Saved places / favorites page."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from models import store
from ui_utils import bottom_nav, load_image, star_rating


class FavoritesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller

        tk.Label(
            self,
            text="Saved Places",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", padx=16, pady=(16, 8))

        from ui_utils import scrollable_frame

        scroll_container, _, self.list_frame = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        bottom_nav(
            self,
            [("🏠", "Home"), ("🔍", "Search"), ("🎫", "Tickets"), ("❤", "Saved"), ("👤", "Profile")],
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

        favorites = store.get_favorites()
        if not favorites:
            tk.Label(
                self.list_frame,
                text="No saved places yet.\nTap ♡ on any location to save it.",
                bg=BACKGROUND,
                fg=TEXT_LIGHT,
                font=("Segoe UI", 11),
                justify="center",
            ).pack(pady=60)
            return

        for loc in favorites:
            card = tk.Frame(
                self.list_frame,
                bg=CARD,
                highlightbackground="#E0E0E0",
                highlightthickness=1,
                cursor="hand2",
            )
            card.pack(fill=tk.X, padx=8, pady=6)

            img = load_image(loc["image"], size=(80, 60))
            img_lbl = tk.Label(card, image=img, bg=CARD)
            img_lbl.image = img
            img_lbl.pack(side=tk.LEFT, padx=8, pady=8)

            info = tk.Frame(card, bg=CARD)
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=8)
            tk.Label(
                info,
                text=loc["name"],
                font=("Segoe UI", 12, "bold"),
                fg=TEXT,
                bg=CARD,
                anchor="w",
            ).pack(fill=tk.X)
            star_rating(info, loc["rating"], CARD).pack(anchor="w")

            remove = tk.Label(
                card,
                text="✕",
                font=("Segoe UI", 14),
                fg="#DC3545",
                bg=CARD,
                cursor="hand2",
            )
            remove.pack(side=tk.RIGHT, padx=12)

            def open_detail(_=None, lid=loc["id"]):
                self.controller.selected_location_id = lid
                self.controller.show_frame("LocationDetailsFrame")

            def remove_fav(e, lid=loc["id"]):
                store.toggle_favorite(lid)
                self._refresh()

            for w in (card, img_lbl, info):
                w.bind("<Button-1>", open_detail)
            remove.bind("<Button-1>", remove_fav)
