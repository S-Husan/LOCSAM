"""Ticket prices and booking page."""

import tkinter as tk
from tkinter import messagebox, simpledialog

from data import TICKET_TYPES
from i18n import t
from models import store
from theme import PAD_LG
from ui_utils import (
    back_button,
    button_row,
    c,
    create_card,
    create_label,
    scrollable_frame,
    styled_button,
    subtitle_label,
)


class TicketBookingFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.body = tk.Frame(self, bg=c("BACKGROUND"))
        self.body.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()

        loc_id = getattr(self.controller, "selected_location_id", 1)
        loc = store.get_location(loc_id)

        back_button(self.body, lambda: self.controller.show_frame("LocationDetailsFrame"))

        scroll_container, _, inner = scrollable_frame(self.body)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        col = tk.Frame(inner, bg=c("BACKGROUND"))
        col.pack(anchor="center", padx=PAD_LG)

        title = loc["name"] if loc else "Ticket Prices"
        create_label(col, title, style="heading").pack(anchor="w", pady=(0, 4))
        subtitle_label(col, "Select a ticket type", wrap=480).pack(pady=(0, 12))

        base_price = loc["price"] if loc else 10
        types = []
        for tt in TICKET_TYPES:
            ratio = tt["price"] / 10
            price = (
                round(base_price * 2.5)
                if tt["type"] == "Family Ticket"
                else round(base_price * ratio)
            )
            types.append({**tt, "price": price})

        self.selected_type = tk.StringVar(value=types[0]["type"])

        for tt in types:
            card = create_card(col, padx=16, pady=12)
            card.pack(fill=tk.X, pady=6)
            row = tk.Frame(card, bg=c("CARD"))
            row.pack(fill=tk.X)
            tk.Radiobutton(
                row,
                text=tt["type"],
                variable=self.selected_type,
                value=tt["type"],
                bg=c("CARD"),
                fg=c("TEXT"),
                activebackground=c("CARD"),
                selectcolor=c("INPUT_BG"),
                font=("Segoe UI", 11, "bold"),
            ).pack(side=tk.LEFT)
            create_label(
                row,
                f"${tt['price']}",
                style="heading",
                bg=c("CARD"),
                fg=c("PRIMARY"),
            ).pack(side=tk.RIGHT)
            create_label(card, tt["note"], style="tiny", bg=c("CARD")).pack(
                fill=tk.X, pady=(6, 0)
            )

        note_bg = "#2A2540" if store.settings.get("dark_mode") else "#FFF8E1"
        note = tk.Frame(col, bg=note_bg, padx=14, pady=12)
        note.pack(fill=tk.X, pady=16)
        create_label(
            note,
            "Note: Tickets can be purchased online or at the entrance. "
            "Prices may vary during special events.",
            style="tiny",
            bg=note_bg,
            wraplength=460,
        ).pack(anchor="w")

        self._ticket_prices = {tt["type"]: tt["price"] for tt in types}

        btn_col = button_row(col)
        styled_button(
            btn_col,
            t("buy_ticket"),
            command=lambda: self._buy(loc_id),
            style="primary",
            width=22,
        ).pack(pady=(0, 24))

    def _buy(self, loc_id):
        ticket_type = self.selected_type.get()
        price = self._ticket_prices.get(ticket_type, 10)
        visit_date = simpledialog.askstring("Visit Date", "Enter visit date (e.g. 15 Jun):")
        if not visit_date:
            return
        store.book_ticket(loc_id, ticket_type, 1, price, visit_date)
        messagebox.showinfo("LOCSAM", f"Ticket booked! Total: ${price}")
        self.controller.show_frame("MyTicketsFrame")
