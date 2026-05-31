"""Ticket prices and booking page."""

import tkinter as tk
from tkinter import messagebox, simpledialog

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from data import TICKET_TYPES
from models import store
from ui_utils import scrollable_frame, section_title, styled_button, subtitle_label


class TicketBookingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.body = tk.Frame(self, bg=BACKGROUND)
        self.body.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)

        back = tk.Label(
            self.body,
            text="← Back",
            fg=PRIMARY,
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        )
        back.pack(anchor="w", padx=16, pady=12)
        back.bind(
            "<Button-1>",
            lambda e: self.controller.show_frame("LocationDetailsFrame"),
        )

        scroll_container, _, inner = scrollable_frame(self.body)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        title = loc["name"] if loc else "Ticket Prices"
        section_title(inner, title).pack(anchor="w", padx=16, pady=(0, 4))
        subtitle_label(inner, "Select a ticket type").pack(padx=16, pady=(0, 12))

        base_price = loc["price"] if loc else 10
        types = []
        for t in TICKET_TYPES:
            ratio = t["price"] / 10
            types.append({**t, "price": round(base_price * ratio) if t["type"] != "Family Ticket" else round(base_price * 2.5)})

        self.selected_type = tk.StringVar(value=types[0]["type"])

        for t in types:
            card = tk.Frame(inner, bg=CARD, padx=14, pady=12)
            card.pack(fill=tk.X, padx=16, pady=6)
            row = tk.Frame(card, bg=CARD)
            row.pack(fill=tk.X)
            tk.Radiobutton(
                row,
                text=t["type"],
                variable=self.selected_type,
                value=t["type"],
                bg=CARD,
                fg=TEXT,
                activebackground=CARD,
                font=("Segoe UI", 11, "bold"),
            ).pack(side=tk.LEFT)
            tk.Label(
                row,
                text=f"${t['price']}",
                font=("Segoe UI", 14, "bold"),
                fg=PRIMARY,
                bg=CARD,
            ).pack(side=tk.RIGHT)
            tk.Label(
                card,
                text=t["note"],
                font=("Segoe UI", 9),
                fg=TEXT_LIGHT,
                bg=CARD,
                anchor="w",
            ).pack(fill=tk.X, pady=(4, 0))

        note = tk.Frame(inner, bg="#FFF8E1", padx=12, pady=10)
        note.pack(fill=tk.X, padx=16, pady=16)
        tk.Label(
            note,
            text=(
                "Note: Tickets can be purchased online or at the entrance. "
                "Prices may vary during special events."
            ),
            wraplength=360,
            justify="left",
            bg="#FFF8E1",
            fg=TEXT,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        self._ticket_prices = {t["type"]: t["price"] for t in types}

        styled_button(
            inner,
            "Buy Ticket Online",
            command=lambda: self._buy(loc_id),
        ).pack(fill=tk.X, padx=16, pady=(0, 24))

    def _buy(self, loc_id):
        ticket_type = self.selected_type.get()
        price = self._ticket_prices.get(ticket_type, 10)
        visit_date = simpledialog.askstring("Visit Date", "Enter visit date (e.g. 15 Jun):")
        if not visit_date:
            return
        store.book_ticket(loc_id, ticket_type, 1, price, visit_date)
        messagebox.showinfo("LOCSAM", f"Ticket booked! Total: ${price}")
        self.controller.show_frame("MyTicketsFrame")
