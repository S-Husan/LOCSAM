"""Search attractions page."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from models import store
from ui_utils import bottom_nav, entry_field, get_entry_value, load_image, star_rating


class SearchFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller

        header = tk.Frame(self, bg=BACKGROUND, padx=16, pady=12)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="Search",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w")

        search_row = tk.Frame(self, bg=BACKGROUND, padx=16)
        search_row.pack(fill=tk.X)
        self.search_entry = entry_field(search_row, "Search by name, category, rating...")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        tk.Button(
            search_row,
            text="Search",
            bg=PRIMARY,
            fg="white",
            relief=tk.FLAT,
            command=self._search,
            padx=12,
        ).pack(side=tk.LEFT, padx=(8, 0))

        from ui_utils import scrollable_frame

        scroll_container, _, self.results = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        bottom_nav(
            self,
            [("🏠", "Home"), ("🔍", "Search"), ("🎫", "Tickets"), ("❤", "Saved"), ("👤", "Profile")],
            1,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def on_show(self):
        q = getattr(self.controller, "search_query", "")
        if q:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, q)
            self.search_entry.config(fg=TEXT)
        self._search()

    def _search(self):
        for w in self.results.winfo_children():
            w.destroy()

        q = get_entry_value(self.search_entry, "Search by name, category, rating...")
        locations = store.get_locations("All", q)

        if not locations:
            tk.Label(
                self.results,
                text="No results found.",
                bg=BACKGROUND,
                fg=TEXT_LIGHT,
                font=("Segoe UI", 11),
            ).pack(pady=40)
            return

        for loc in locations:
            row = tk.Frame(
                self.results,
                bg=CARD,
                highlightbackground="#E0E0E0",
                highlightthickness=1,
                cursor="hand2",
            )
            row.pack(fill=tk.X, padx=8, pady=6)

            img = load_image(loc["image"], size=(80, 60))
            img_lbl = tk.Label(row, image=img, bg=CARD)
            img_lbl.image = img
            img_lbl.pack(side=tk.LEFT, padx=8, pady=8)

            info = tk.Frame(row, bg=CARD)
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
            tk.Label(
                info,
                text=f"{loc['reviews']} reviews",
                font=("Segoe UI", 9),
                fg=TEXT_LIGHT,
                bg=CARD,
            ).pack(anchor="w")

            fav = "❤" if store.is_favorite(loc["id"]) else "♡"
            fav_btn = tk.Label(row, text=fav, font=("Segoe UI", 16), bg=CARD, cursor="hand2")
            fav_btn.pack(side=tk.RIGHT, padx=12)

            def open_detail(_=None, lid=loc["id"]):
                self.controller.selected_location_id = lid
                self.controller.show_frame("LocationDetailsFrame")

            def toggle_fav(e, lid=loc["id"]):
                store.toggle_favorite(lid)
                self._search()

            for w in (row, img_lbl, info):
                w.bind("<Button-1>", open_detail)
            fav_btn.bind("<Button-1>", toggle_fav)
