"""Home page — desktop responsive tourism grid."""

import tkinter as tk

from data import FILTER_TABS
from i18n import t
from models import store
from theme import CONTENT_MAX_WIDTH, PAD_LG, PAD_MD
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    desktop_columns,
    entry_field,
    get_entry_value,
    load_image,
    refresh_scroll_region,
    star_rating,
    styled_button,
)

# Gap between cards: padx/pady are per side (13+13 ≈ 26px horizontal, 10+10 ≈ 20px vertical)
CARD_PADX = 13
CARD_PADY = 10
CARD_MIN_WIDTH = 270
CARD_MAX_WIDTH = 340


class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.active_filter = "All"
        self.filter_buttons = {}
        self._last_width = 0
        self._build_shell()

    def _build_shell(self):
        header = tk.Frame(self, bg=c("SURFACE"), padx=PAD_LG, pady=14)
        header.pack(fill=tk.X)

        hdr_inner = tk.Frame(header, bg=c("SURFACE"))
        hdr_inner.pack(anchor="center")

        create_label(
            hdr_inner,
            "LOCSAM",
            style="heading",
            bg=c("SURFACE"),
            fg=c("PRIMARY"),
        ).pack(side=tk.LEFT)

        icons = tk.Frame(hdr_inner, bg=c("SURFACE"))
        icons.pack(side=tk.LEFT, padx=24)
        for sym, frame_name in [("🔍", "SearchFrame"), ("👤", "ProfileFrame")]:
            lbl = tk.Label(
                icons,
                text=sym,
                font=("Segoe UI", 16),
                bg=c("SURFACE"),
                fg=c("TEXT"),
                cursor="hand2",
                padx=6,
            )
            lbl.pack(side=tk.LEFT)
            lbl.bind("<Button-1>", lambda e, f=frame_name: self.controller.show_frame(f))

        search_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        search_wrap.pack(fill=tk.X, pady=(PAD_MD, 8))
        search_row = tk.Frame(search_wrap, bg=c("BACKGROUND"))
        search_row.pack(anchor="center")
        self.search_entry = entry_field(search_row, t("search_placeholder"), width=42)
        self.search_entry.pack(side=tk.LEFT, ipady=6)
        self.search_entry.bind("<Return>", lambda e: self._apply_search())
        styled_button(
            search_row,
            t("go"),
            command=self._apply_search,
            style="primary",
            width=8,
        ).pack(side=tk.LEFT, padx=(10, 0))

        tabs_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        tabs_wrap.pack(fill=tk.X, pady=(0, 8))
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

        content_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        content_wrap.pack(fill=tk.BOTH, expand=True)
        from ui_utils import scrollable_frame

        scroll_container, self.list_canvas, self.list_frame = scrollable_frame(content_wrap)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=PAD_LG, pady=4)

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

    def on_show(self):
        self._update_tabs()
        self._refresh_list()

    def _on_resize(self, event):
        if event.widget != self or event.width < 200:
            return
        if abs(event.width - self._last_width) < 40:
            return
        self._last_width = event.width
        self._refresh_list(event.width)

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _update_tabs(self):
        for name, btn in self.filter_buttons.items():
            if name == self.active_filter:
                btn.config(bg=c("PRIMARY"), fg="#FFFFFF")
            else:
                btn.config(bg=c("CARD"), fg=c("TEXT"))

    def _set_filter(self, tab):
        self.active_filter = tab
        self._update_tabs()
        self._refresh_list()

    def _apply_search(self):
        self._refresh_list()

    def _current_search(self):
        return get_entry_value(self.search_entry, t("search_placeholder"))

    def _refresh_list(self, width=None):
        for w in self.list_frame.winfo_children():
            w.destroy()

        self.update_idletasks()
        w = width or self.winfo_width()
        if w < 200:
            w = CONTENT_MAX_WIDTH
        w = min(w, CONTENT_MAX_WIDTH)
        cols = desktop_columns(w)
        usable = w - 32
        h_gaps = CARD_PADX * 2 * max(cols - 1, 0)
        card_w = max(CARD_MIN_WIDTH, min(CARD_MAX_WIDTH, (usable - h_gaps) // cols))

        grid = tk.Frame(self.list_frame, bg=c("BACKGROUND"))
        grid.pack(anchor="center", pady=8)

        for col in range(cols):
            grid.grid_columnconfigure(col, weight=0)

        locations = store.get_locations(self.active_filter, self._current_search())

        if not locations:
            create_label(
                grid,
                "No places found.",
                style="body",
            ).grid(row=0, column=0, columnspan=cols, pady=40, padx=20)
            refresh_scroll_region(self.list_canvas)
            return

        for i, loc in enumerate(locations):
            cell = tk.Frame(grid, bg=c("BACKGROUND"))
            cell.grid(
                row=i // cols,
                column=i % cols,
                padx=CARD_PADX,
                pady=CARD_PADY,
                sticky="n",
            )
            self._build_card(cell, loc, card_w)

        refresh_scroll_region(self.list_canvas)

    def _build_card(self, parent, loc, card_w):
        card = create_card(parent, padx=0, pady=0)
        card.pack()
        card.config(cursor="hand2", width=card_w)

        img_h = max(140, int(card_w * 0.5))
        img = load_image(loc["image"], size=(card_w - 2, img_h))
        img_lbl = tk.Label(card, image=img, bg=c("CARD"))
        img_lbl.image = img
        img_lbl.pack()

        info = tk.Frame(card, bg=c("CARD"), padx=14, pady=12)
        info.pack(fill=tk.X)

        create_label(info, loc["name"], style="subheading", bg=c("CARD")).pack(fill=tk.X)
        create_label(info, loc["city"], style="tiny", bg=c("CARD")).pack(fill=tk.X, pady=(2, 6))

        row = tk.Frame(info, bg=c("CARD"))
        row.pack(fill=tk.X)
        star_rating(row, loc["rating"], c("CARD")).pack(side=tk.LEFT)
        create_label(
            row,
            f"({loc['reviews']} {t('reviews')}) · ${loc['price']}",
            style="tiny",
            bg=c("CARD"),
        ).pack(side=tk.LEFT, padx=(6, 0))

        fav = "❤" if store.is_favorite(loc["id"]) else "♡"
        fav_btn = tk.Label(
            row,
            text=fav,
            font=("Segoe UI", 15),
            bg=c("CARD"),
            fg=c("PRIMARY"),
            cursor="hand2",
        )
        fav_btn.pack(side=tk.RIGHT)

        def open_detail(_=None, lid=loc["id"]):
            self.controller.selected_location_id = lid
            self.controller.show_frame("LocationDetailsFrame")

        def toggle_fav(e, lid=loc["id"]):
            store.toggle_favorite(lid)
            self._refresh_list()

        for widget in (card, img_lbl, info, row):
            widget.bind("<Button-1>", open_detail)
        fav_btn.bind("<Button-1>", toggle_fav)
