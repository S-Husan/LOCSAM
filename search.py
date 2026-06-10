"""Search attractions page."""

import tkinter as tk

from data import FILTER_TABS
from i18n import t
from models import store
from theme import PAD_LG, PAD_MD
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    entry_field,
    get_entry_value,
    load_image,
    page_header,
    refresh_scroll_region,
    star_rating,
    styled_button,
)


class SearchFrame(tk.Frame):
    SEARCH_PLACEHOLDER = "Search by name, category, rating..."

    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.active_filter = "All"
        self.filter_buttons = {}
        self._build_shell()

    def _build_shell(self):
        page_header(self, t("search"))

        search_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        search_wrap.pack(fill=tk.X, padx=PAD_LG, pady=(0, 8))
        search_row = tk.Frame(search_wrap, bg=c("BACKGROUND"))
        search_row.pack(anchor="center")
        self.search_entry = entry_field(search_row, self.SEARCH_PLACEHOLDER, width=44)
        self.search_entry.pack(side=tk.LEFT, ipady=6)
        self.search_entry.bind("<Return>", lambda e: self._search())
        styled_button(
            search_row,
            t("search"),
            command=self._search,
            style="primary",
            width=10,
        ).pack(side=tk.LEFT, padx=(10, 0))

        tabs_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        tabs_wrap.pack(fill=tk.X, pady=(0, PAD_MD))
        tabs = tk.Frame(tabs_wrap, bg=c("BACKGROUND"))
        tabs.pack(anchor="center")
        for tab in FILTER_TABS:
            btn = tk.Label(
                tabs,
                text=tab,
                font=("Segoe UI", 9, "bold"),
                padx=14,
                pady=8,
                cursor="hand2",
                bg=c("CARD"),
                fg=c("TEXT"),
            )
            btn.pack(side=tk.LEFT, padx=4)
            btn.bind("<Button-1>", lambda e, tb=tab: self._set_filter(tb))
            self.filter_buttons[tab] = btn

        content = tk.Frame(self, bg=c("BACKGROUND"))
        content.pack(fill=tk.BOTH, expand=True)
        from ui_utils import scrollable_frame

        scroll_container, self.results_canvas, self.results = scrollable_frame(content)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=4)

        bottom_nav(
            self,
            [
                ("🏠", t("home")),
                ("🔍", t("search")),
                ("🎫", t("tickets")),
                ("❤", t("saved")),
                ("👤", t("profile")),
            ],
            1,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _set_filter(self, tab):
        self.active_filter = tab
        self._update_tabs()
        self._search()

    def _update_tabs(self):
        for name, btn in self.filter_buttons.items():
            if name == self.active_filter:
                btn.config(bg=c("PRIMARY"), fg="#FFFFFF")
            else:
                btn.config(bg=c("CARD"), fg=c("TEXT"))

    def on_show(self):
        q = getattr(self.controller, "search_query", "")
        if q:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, q)
            self.search_entry.config(fg=c("TEXT"))
            self.controller.search_query = ""
        self._update_tabs()
        self._search()

    def _search(self):
        for w in self.results.winfo_children():
            w.destroy()

        q = get_entry_value(self.search_entry, self.SEARCH_PLACEHOLDER)
        locations = store.get_locations(self.active_filter, q)

        list_wrap = tk.Frame(self.results, bg=c("BACKGROUND"))
        list_wrap.pack(fill=tk.X, padx=4, pady=4)

        if not locations:
            create_label(
                list_wrap,
                "No places found.",
                style="body",
            ).pack(pady=40, padx=20)
            refresh_scroll_region(self.results_canvas)
            return

        for loc in locations:
            row = create_card(list_wrap, padx=12, pady=10)
            row.pack(fill=tk.X, padx=4, pady=6)
            row.config(cursor="hand2")

            inner = tk.Frame(row, bg=c("CARD"))
            inner.pack(fill=tk.X)

            img = load_image(loc["image"], size=(96, 72))
            img_lbl = tk.Label(inner, image=img, bg=c("CARD"))
            img_lbl.image = img
            img_lbl.pack(side=tk.LEFT, padx=(0, 12))

            info = tk.Frame(inner, bg=c("CARD"))
            info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            create_label(info, loc["name"], style="subheading", bg=c("CARD")).pack(
                fill=tk.X, anchor="w"
            )
            create_label(
                info,
                f"{loc['category']} · {loc['city']}",
                style="tiny",
                bg=c("CARD"),
            ).pack(anchor="w", pady=(2, 0))
            star_rating(info, loc["rating"], c("CARD")).pack(anchor="w", pady=(2, 0))
            create_label(
                info,
                f"{loc['reviews']} {t('reviews')} · ${loc['price']}",
                style="tiny",
                bg=c("CARD"),
            ).pack(anchor="w")

            fav = "❤" if store.is_favorite(loc["id"]) else "♡"
            fav_btn = tk.Label(
                inner,
                text=fav,
                font=("Segoe UI", 18),
                bg=c("CARD"),
                fg=c("PRIMARY"),
                cursor="hand2",
                padx=12,
            )
            fav_btn.pack(side=tk.RIGHT)

            def open_detail(_=None, lid=loc["id"]):
                self.controller.selected_location_id = lid
                self.controller.show_frame("LocationDetailsFrame")

            def toggle_fav(e, lid=loc["id"]):
                store.toggle_favorite(lid)
                self._search()

            for widget in (row, inner, img_lbl, info):
                widget.bind("<Button-1>", open_detail)
            fav_btn.bind("<Button-1>", toggle_fav)

        refresh_scroll_region(self.results_canvas)
