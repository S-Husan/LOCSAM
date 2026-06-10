"""My Tickets page."""

import tkinter as tk

from i18n import t
from models import store
from theme import PAD_LG
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    page_header,
)


class MyTicketsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.active_tab = "upcoming"
        self.tab_labels = {}

        page_header(self, t("my_tickets"))

        tabs_wrap = tk.Frame(self, bg=c("BACKGROUND"))
        tabs_wrap.pack(fill=tk.X, padx=PAD_LG, pady=(0, 8))
        tabs = tk.Frame(tabs_wrap, bg=c("BACKGROUND"))
        tabs.pack(anchor="w")
        for tab, label in [("upcoming", t("upcoming")), ("history", t("history"))]:
            lbl = tk.Label(
                tabs,
                text=label,
                font=("Segoe UI", 11, "bold"),
                padx=18,
                pady=9,
                cursor="hand2",
                bg=c("CARD"),
                fg=c("TEXT"),
            )
            lbl.pack(side=tk.LEFT, padx=(0, 8))
            lbl.bind("<Button-1>", lambda e, tb=tab: self._switch_tab(tb))
            self.tab_labels[tab] = lbl

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
            2,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def on_show(self):
        self._switch_tab(self.active_tab)

    def _switch_tab(self, tab):
        self.active_tab = tab
        for name, lbl in self.tab_labels.items():
            if name == tab:
                lbl.config(bg=c("PRIMARY"), fg="#FFFFFF")
            else:
                lbl.config(bg=c("CARD"), fg=c("TEXT"))
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        wrap = tk.Frame(self.list_frame, bg=c("BACKGROUND"))
        wrap.pack(fill=tk.X, padx=4)

        tickets = store.get_user_tickets(self.active_tab)
        if not tickets:
            create_label(wrap, "No tickets in this section.", style="body").pack(pady=40)
            return

        for ticket in tickets:
            card = create_card(wrap, padx=16, pady=14)
            card.pack(fill=tk.X, pady=6)

            create_label(
                card,
                ticket["location"],
                style="subheading",
                bg=c("CARD"),
            ).pack(fill=tk.X, anchor="w")

            create_label(
                card,
                f"{ticket['date']} · {ticket['time']} · {ticket['detail']} · ${ticket['price']}",
                style="small",
                bg=c("CARD"),
            ).pack(fill=tk.X, anchor="w", pady=(6, 10))

            qr = tk.Frame(
                card,
                bg=c("INPUT_BG"),
                width=80,
                height=80,
                highlightbackground=c("BORDER"),
                highlightthickness=1,
            )
            qr.pack(anchor="w")
            qr.pack_propagate(False)
            create_label(qr, "QR", style="muted", bg=c("INPUT_BG")).place(
                relx=0.5, rely=0.5, anchor="center"
            )
