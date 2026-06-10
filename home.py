"""Home page — tourist locations listing (desktop responsive grid)."""

import tkinter as tk

from data import FILTER_TABS
from i18n import t
from models import store
from theme import theme_manager
from ui_utils import (
    bottom_nav,
    c,
    desktop_card_width,
    desktop_columns,
    entry_field,
    get_entry_value,
    load_image,
    star_rating,
)


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.active_filter = "All"
        self.filter_buttons = {}

        header = tk.Frame(self, bg=c("WHITE"), padx=20, pady=14)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="LOCSAM",
            font=("Segoe UI", 24, "bold"),
            fg=c("PRIMARY"),
            bg=c("WHITE"),
        ).pack(side=tk.LEFT)

        icons = tk.Frame(header, bg=c("WHITE"))
        icons.pack(side=tk.RIGHT)
        for sym, frame_name in [("🔍", "SearchFrame"), ("👤", "ProfileFrame")]:
            lbl = tk.Label(
                icons,
                text=sym,
                font=("Segoe UI", 16),
                bg=c("WHITE"),
                cursor="hand2",
            )
            lbl.pack(side=tk.LEFT, padx=8)
            lbl.bind("<Button-1>", lambda e, f=frame_name: controller.show_frame(f))

        search_row = tk.Frame(self, bg=c("BACKGROUND"), padx=20)
        search_row.pack(fill=tk.X, pady=(0, 10))
        self.search_entry = entry_field(search_row, t("search_placeholder"))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6)
        tk.Button(
            search_row,
            text=t("go"),
            bg=c("PRIMARY"),
            fg="#FFFFFF",
            relief=tk.FLAT,
            command=self._apply_search,
            padx=14,
        ).pack(side=tk.LEFT, padx=(10, 0))

        tabs = tk.Frame(self, bg=c("BACKGROUND"), padx=16)
        tabs.pack(fill=tk.X)
        for tab in FILTER_TABS:
            btn = tk.Label(
                tabs,
                text=tab,
                font=("Segoe UI", 9, "bold"),
                padx=12,
                pady=7,
                cursor="hand2",
            )
            btn.pack(side=tk.LEFT, padx=3)
            btn.bind("<Button-1>", lambda e, tb=tab: self._set_filter(tb))
            self.filter_buttons[tab] = btn

        from ui_utils import scrollable_frame

        scroll_container, _, self.list_frame = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        self.bind("<Configure>", self._on_resize)

        bottom_nav(
            self,
            [
                ("🏠", t("home")),
                ("🔍", t("search")),
                ("🎫", t("tickets")),
                ("❤", t("saved")),
                ("👤", t("profile")),
            ],
            0,
            self._nav_select,
        )

    def _on_resize(self, event):
        if event.widget == self and event.width > 100:
            self._refresh_list(event.width)

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _set_filter(self, tab):
        self.active_filter = tab
        self._refresh_list()

    def _apply_search(self):
        q = get_entry_value(self.search_entry, t("search_placeholder"))
        self.controller.search_query = q
        self.controller.show_frame("SearchFrame")

    def on_show(self):
        self._refresh_list()

    def _refresh_list(self, width=None):
        for w in self.list_frame.winfo_children():
            w.destroy()

        for name, btn in self.filter_buttons.items():
            if name == self.active_filter:
                btn.config(bg=c("PRIMARY"), fg="#FFFFFF")
            else:
                btn.config(bg=c("CARD"), fg=c("TEXT"))

        w = width or self.winfo_width()
        cols = desktop_columns(w)
        card_w = desktop_card_width(w)

        grid = tk.Frame(self.list_frame, bg=c("BACKGROUND"))
        grid.pack(fill=tk.X, padx=4, pady=4)

        locations = store.get_locations(self.active_filter)
        for i, loc in enumerate(locations):
            cell = tk.Frame(grid, bg=c("BACKGROUND"))
            cell.grid(row=i // cols, column=i % cols, padx=8, pady=8, sticky="nsew")
            grid.grid_columnconfigure(i % cols, weight=1)
            self._build_card(cell, loc, card_w)

    def _build_card(self, parent, loc, card_w):
        card = tk.Frame(
            parent,
            bg=c("CARD"),
            highlightbackground=c("BORDER"),
            highlightthickness=1,
            cursor="hand2",
        )
        card.pack(fill=tk.BOTH, expand=True)

        img_h = int(card_w * 0.42)
        img = load_image(loc["image"], size=(card_w, img_h))
        img_lbl = tk.Label(card, image=img, bg=c("CARD"))
        img_lbl.image = img
        img_lbl.pack(fill=tk.X)

        info = tk.Frame(card, bg=c("CARD"), padx=14, pady=12)
        info.pack(fill=tk.X)

        tk.Label(
            info,
            text=loc["name"],
            font=("Segoe UI", 14, "bold"),
            fg=c("TEXT"),
            bg=c("CARD"),
            anchor="w",
        ).pack(fill=tk.X)

        tk.Label(
            info,
            text=loc["city"],
            font=("Segoe UI", 9),
            fg=c("TEXT_LIGHT"),
            bg=c("CARD"),
            anchor="w",
        ).pack(fill=tk.X)

        row = tk.Frame(info, bg=c("CARD"))
        row.pack(fill=tk.X, pady=(6, 0))
        star_rating(row, loc["rating"], c("CARD")).pack(side=tk.LEFT)
        tk.Label(
            row,
            text=f"  ({loc['reviews']} {t('reviews')})  ·  ${loc['price']}",
            font=("Segoe UI", 9),
            fg=c("TEXT_LIGHT"),
            bg=c("CARD"),
        ).pack(side=tk.LEFT)

        fav = "❤" if store.is_favorite(loc["id"]) else "♡"
        fav_btn = tk.Label(row, text=fav, font=("Segoe UI", 14), bg=c("CARD"), cursor="hand2")
        fav_btn.pack(side=tk.RIGHT)

        def open_detail(_=None, lid=loc["id"]):
            self.controller.selected_location_id = lid
            self.controller.show_frame("LocationDetailsFrame")

        def toggle_fav(e, lid=loc["id"]):
            store.toggle_favorite(lid)
            self._refresh_list()

        for widget in (card, img_lbl, info):
            widget.bind("<Button-1>", open_detail)
        fav_btn.bind("<Button-1>", toggle_fav)
