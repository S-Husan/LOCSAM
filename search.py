"""Search attractions page."""

import tkinter as tk

from i18n import t
from models import store
from theme import CONTENT_MAX_WIDTH, PAD_LG, PAD_MD
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    entry_field,
    get_entry_value,
    load_image,
    page_header,
    star_rating,
    styled_button,
)


class SearchFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self._build_shell()

    def _build_shell(self):
        page_header(self, t("search"))

        search_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        search_wrap.pack(fill=tk.X, padx=PAD_LG, pady=(0, PAD_MD))
        search_row = tk.Frame(search_wrap, bg=c("BACKGROUND"))
        search_row.pack(anchor="center")
        self.search_entry = entry_field(
            search_row, "Search by name, category, rating...", width=44
        )
        self.search_entry.pack(side=tk.LEFT, ipady=6)
        styled_button(
            search_row,
            t("search"),
            command=self._search,
            style="primary",
            width=10,
        ).pack(side=tk.LEFT, padx=(10, 0))

        from ui_utils import scrollable_frame

        content = tk.Frame(self, bg=c("BACKGROUND"))
        content.pack(fill=tk.BOTH, expand=True)
        scroll_container, _, self.results = scrollable_frame(content)
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

    def on_show(self):
        q = getattr(self.controller, "search_query", "")
        if q:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, q)
            self.search_entry.config(fg=c("TEXT"))
        self._search()

    def _search(self):
        for w in self.results.winfo_children():
            w.destroy()

        q = get_entry_value(self.search_entry, "Search by name, category, rating...")
        locations = store.get_locations("All", q)

        list_wrap = tk.Frame(self.results, bg=c("BACKGROUND"))
        list_wrap.pack(anchor="center", fill=tk.X)

        if not locations:
            create_label(
                list_wrap,
                "No results found.",
                style="body",
            ).pack(pady=40)
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

            for w in (row, inner, img_lbl, info):
                w.bind("<Button-1>", open_detail)
            fav_btn.bind("<Button-1>", toggle_fav)
