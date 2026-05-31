"""Home page — tourist locations listing."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT, WHITE
from data import FILTER_TABS
from models import store
from ui_utils import bottom_nav, entry_field, get_entry_value, load_image, star_rating


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.active_filter = "All"
        self.filter_buttons = {}

        header = tk.Frame(self, bg=WHITE, padx=16, pady=12)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="LOCSAM",
            font=("Segoe UI", 22, "bold"),
            fg=PRIMARY,
            bg=WHITE,
        ).pack(side=tk.LEFT)

        icons = tk.Frame(header, bg=WHITE)
        icons.pack(side=tk.RIGHT)
        for sym, frame_name in [("🔍", "SearchFrame"), ("👤", "ProfileFrame")]:
            lbl = tk.Label(
                icons,
                text=sym,
                font=("Segoe UI", 16),
                bg=WHITE,
                cursor="hand2",
            )
            lbl.pack(side=tk.LEFT, padx=6)
            lbl.bind(
                "<Button-1>",
                lambda e, f=frame_name: controller.show_frame(f),
            )

        search_row = tk.Frame(self, bg=BACKGROUND, padx=16)
        search_row.pack(fill=tk.X, pady=(0, 8))
        self.search_entry = entry_field(search_row, "Enter place name...")
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        tk.Button(
            search_row,
            text="Go",
            bg=PRIMARY,
            fg=WHITE,
            relief=tk.FLAT,
            command=self._apply_search,
            padx=12,
        ).pack(side=tk.LEFT, padx=(8, 0))

        tabs = tk.Frame(self, bg=BACKGROUND, padx=12)
        tabs.pack(fill=tk.X)
        for tab in FILTER_TABS:
            btn = tk.Label(
                tabs,
                text=tab,
                font=("Segoe UI", 9, "bold"),
                padx=10,
                pady=6,
                cursor="hand2",
            )
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, t=tab: self._set_filter(t))
            self.filter_buttons[tab] = btn

        from ui_utils import scrollable_frame

        scroll_container, _, self.list_frame = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=4)

        bottom_nav(
            self,
            [("🏠", "Home"), ("🔍", "Search"), ("🎫", "Tickets"), ("❤", "Saved"), ("👤", "Profile")],
            0,
            self._nav_select,
        )

        self._refresh_list()

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _set_filter(self, tab):
        self.active_filter = tab
        for name, btn in self.filter_buttons.items():
            if name == tab:
                btn.config(bg=PRIMARY, fg=WHITE)
            else:
                btn.config(bg=CARD, fg=TEXT)
        self._refresh_list()

    def _apply_search(self):
        q = get_entry_value(self.search_entry, "Enter place name...")
        self.controller.search_query = q
        self.controller.show_frame("SearchFrame")

    def on_show(self):
        self._refresh_list()

    def _refresh_list(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for name, btn in self.filter_buttons.items():
            if name == self.active_filter:
                btn.config(bg=PRIMARY, fg=WHITE)
            else:
                btn.config(bg=CARD, fg=TEXT)

        locations = store.get_locations(self.active_filter)
        for loc in locations:
            self._build_card(loc)

    def _build_card(self, loc):
        card = tk.Frame(
            self.list_frame,
            bg=CARD,
            highlightbackground="#E0E0E0",
            highlightthickness=1,
            cursor="hand2",
        )
        card.pack(fill=tk.X, padx=8, pady=8)

        img = load_image(loc["image"], size=(380, 160))
        img_lbl = tk.Label(card, image=img, bg=CARD)
        img_lbl.image = img
        img_lbl.pack(fill=tk.X)

        info = tk.Frame(card, bg=CARD, padx=12, pady=10)
        info.pack(fill=tk.X)

        tk.Label(
            info,
            text=loc["name"],
            font=("Segoe UI", 14, "bold"),
            fg=TEXT,
            bg=CARD,
            anchor="w",
        ).pack(fill=tk.X)

        tk.Label(
            info,
            text=loc["city"],
            font=("Segoe UI", 9),
            fg=TEXT_LIGHT,
            bg=CARD,
            anchor="w",
        ).pack(fill=tk.X)

        row = tk.Frame(info, bg=CARD)
        row.pack(fill=tk.X, pady=(4, 0))
        star_rating(row, loc["rating"], CARD).pack(side=tk.LEFT)
        tk.Label(
            row,
            text=f"  ({loc['reviews']} reviews)  ·  ${loc['price']}",
            font=("Segoe UI", 9),
            fg=TEXT_LIGHT,
            bg=CARD,
        ).pack(side=tk.LEFT)

        fav = "❤" if store.is_favorite(loc["id"]) else "♡"
        fav_btn = tk.Label(row, text=fav, font=("Segoe UI", 14), bg=CARD, cursor="hand2")
        fav_btn.pack(side=tk.RIGHT)

        def open_detail(_=None, lid=loc["id"]):
            self.controller.selected_location_id = lid
            self.controller.show_frame("LocationDetailsFrame")

        def toggle_fav(e, lid=loc["id"]):
            store.toggle_favorite(lid)
            self._refresh_list()

        for w in (card, img_lbl, info):
            w.bind("<Button-1>", open_detail)
        fav_btn.bind("<Button-1>", toggle_fav)
