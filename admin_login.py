"""Admin login page."""

import tkinter as tk
from tkinter import messagebox

from models import store
from ui_utils import (
    back_button,
    button_row,
    c,
    create_label,
    entry_field,
    form_card,
    get_entry_value,
    styled_button,
)


class AdminLoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self._build()

    def on_show(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        back_button(self, lambda: self.controller.show_frame("SplashFrame"))

        _, card = form_card(self)

        create_label(card, "Admin Login", style="title", bg=c("CARD")).pack(
            anchor="w", pady=(0, 4)
        )
        create_label( card, "Access the LOCSAM admin panel", style="small", bg=c("CARD"), ).pack(anchor="w", pady=(0, 24))

        create_label(card, "Username", style="body", bg=c("CARD")).pack(anchor="w")
        self.user_entry = entry_field(card, "Enter admin username")
        self.user_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        create_label(card, "Password", style="body", bg=c("CARD")).pack(anchor="w")
        self.pass_entry = entry_field(card, "Enter admin password", show="•")
        self.pass_entry.pack(fill=tk.X, pady=(4, 20), ipady=6)

        btn_col = button_row(card)
        styled_button(
            btn_col,
            "Login to Admin Panel",
            command=self._login,
            style="primary",
            width=24,
        ).pack()

        # create_label(card, "Default: admin / admin123", style="tiny", bg=c("CARD"),).pack(pady=14)

    def _login(self):
        username = get_entry_value(self.user_entry, "Enter admin username")
        password = get_entry_value(self.pass_entry, "Enter admin password")
        if not username or not password:
            messagebox.showerror("Validation", "Enter username and password.")
            return
        ok, msg = store.login_admin(username, password)
        if ok:
            self.controller.show_frame("AdminDashboardFrame")
        else:
            messagebox.showerror("Admin Login", msg)
