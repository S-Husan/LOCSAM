"""Admin login page."""

import tkinter as tk
from tkinter import messagebox

from config import BACKGROUND, PRIMARY, TEXT
from models import store
from ui_utils import entry_field, get_entry_value, link_label, section_title, styled_button


class AdminLoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller

        back = tk.Label(
            self,
            text="← Back",
            fg=PRIMARY,
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        )
        back.pack(anchor="w", padx=20, pady=(16, 0))
        back.bind("<Button-1>", lambda e: controller.show_frame("SplashFrame"))

        body = tk.Frame(self, bg=BACKGROUND, padx=24)
        body.pack(fill=tk.BOTH, expand=True, pady=40)

        section_title(body, "Admin Login").pack(anchor="w", pady=(0, 4))
        tk.Label(
            body,
            text="Access the LOCSAM admin panel",
            fg="#666",
            bg=BACKGROUND,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 24))

        tk.Label(body, text="Username", fg=TEXT, bg=BACKGROUND).pack(anchor="w")
        self.user_entry = entry_field(body, "Enter admin username")
        self.user_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Password", fg=TEXT, bg=BACKGROUND).pack(anchor="w")
        self.pass_entry = entry_field(body, "Enter admin password", show="•")
        self.pass_entry.pack(fill=tk.X, pady=(4, 20), ipady=6)

        styled_button(body, "Login", command=self._login).pack(fill=tk.X)

        tk.Label(
            body,
            text="Default: admin / admin123",
            fg="#999",
            bg=BACKGROUND,
            font=("Segoe UI", 9),
        ).pack(pady=12)

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
