"""My Tickets page with Upcoming and History tabs."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from models import store
from ui_utils import bottom_nav, styled_button


class MyTicketsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.active_tab = "upcoming"
        self.tab_labels = {}

        tk.Label(
            self,
            text="My Tickets",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
        ).pack(anchor="w", padx=16, pady=(16, 8))

        tabs = tk.Frame(self, bg=BACKGROUND, padx=16)
        tabs.pack(fill=tk.X)
        for tab, label in [("upcoming", "Upcoming"), ("history", "History")]:
            lbl = tk.Label(
                tabs,
                text=label,
                font=("Segoe UI", 11, "bold"),
                padx=16,
                pady=8,
                cursor="hand2",
            )
            lbl.pack(side=tk.LEFT, padx=(0, 8))
            lbl.bind("<Button-1>", lambda e, t=tab: self._switch_tab(t))
            self.tab_labels[tab] = lbl

        from ui_utils import scrollable_frame

        scroll_container, _, self.list_frame = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        bottom_nav(
            self,
            [("🏠", "Home"), ("🔍", "Search"), ("🎫", "Tickets"), ("❤", "Saved"), ("👤", "Profile")],
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
                lbl.config(bg=PRIMARY, fg="white")
            else:
                lbl.config(bg=CARD, fg=TEXT)
        self._refresh()

    def _refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        tickets = store.get_user_tickets(self.active_tab)
        if not tickets:
            tk.Label(
                self.list_frame,
                text="No tickets in this section.",
                bg=BACKGROUND,
                fg=TEXT_LIGHT,
                font=("Segoe UI", 11),
            ).pack(pady=40)
            return

        for t in tickets:
            card = tk.Frame(
                self.list_frame,
                bg=CARD,
                highlightbackground="#E0E0E0",
                highlightthickness=1,
                padx=14,
                pady=12,
            )
            card.pack(fill=tk.X, padx=8, pady=6)

            tk.Label(
                card,
                text=t["location"],
                font=("Segoe UI", 13, "bold"),
                fg=TEXT,
                bg=CARD,
                anchor="w",
            ).pack(fill=tk.X)

            tk.Label(
                card,
                text=f"{t['date']}  ·  {t['time']}  ·  {t['detail']}  ·  ${t['price']}",
                font=("Segoe UI", 10),
                fg=TEXT_LIGHT,
                bg=CARD,
                anchor="w",
            ).pack(fill=tk.X, pady=(4, 8))

            qr = tk.Frame(card, bg=WHITE, width=80, height=80, highlightbackground="#CCC", highlightthickness=1)
            qr.pack(anchor="w")
            qr.pack_propagate(False)
            tk.Label(
                qr,
                text="QR",
                font=("Segoe UI", 16, "bold"),
                fg=TEXT_LIGHT,
                bg=WHITE,
            ).place(relx=0.5, rely=0.5, anchor="center")
