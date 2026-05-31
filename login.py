"""User login page."""

import tkinter as tk
from tkinter import messagebox

from config import BACKGROUND, TEXT
from models import store
from ui_utils import entry_field, get_entry_value, link_label, section_title, styled_button


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.remember_var = tk.BooleanVar(value=False)

        tk.Label(
            self,
            text="← Back",
            fg="#6A00FF",
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        ).pack(anchor="w", padx=20, pady=(16, 0))
        self.children[list(self.children.keys())[0]].bind(
            "<Button-1>", lambda e: controller.show_frame("SplashFrame")
        )

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)

        section_title(body, "Welcome Back").pack(anchor="w", pady=(0, 4))
        tk.Label(
            body,
            text="Login to continue exploring Samarkand",
            fg="#666",
            bg=BACKGROUND,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 24))

        tk.Label(body, text="Email", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.email_entry = entry_field(body, "Enter your email")
        self.email_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Password", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.pass_entry = entry_field(body, "Enter your password", show="•")
        self.pass_entry.pack(fill=tk.X, pady=(4, 8), ipady=6)

        opts = tk.Frame(body, bg=BACKGROUND)
        opts.pack(fill=tk.X, pady=(0, 20))
        tk.Checkbutton(
            opts,
            text="Remember Me",
            variable=self.remember_var,
            bg=BACKGROUND,
            fg=TEXT,
            activebackground=BACKGROUND,
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT)
        link_label(
            opts,
            "Forgot Password?",
            lambda: messagebox.showinfo(
                "LOCSAM", "Password reset will be available with MySQL backend."
            ),
        ).pack(side=tk.RIGHT)

        styled_button(body, "Login", command=self._login).pack(fill=tk.X, pady=(0, 12))
        styled_button(
            body,
            "Register",
            command=lambda: controller.show_frame("RegisterFrame"),
            style="secondary",
        ).pack(fill=tk.X)

    def _login(self):
        email = get_entry_value(self.email_entry, "Enter your email")
        password = get_entry_value(self.pass_entry, "Enter your password")
        if not email or not password:
            messagebox.showerror("Validation", "Please enter email and password.")
            return
        ok, msg = store.login_user(email, password)
        if ok:
            self.controller.show_frame("HomeFrame")
        else:
            messagebox.showerror("Login Failed", msg)
