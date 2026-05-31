"""User registration page."""

import tkinter as tk
from tkinter import messagebox

from config import BACKGROUND, TEXT
from models import store
from ui_utils import entry_field, get_entry_value, link_label, section_title, styled_button


class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller

        tk.Label(
            self,
            text="← Back",
            fg="#6A00FF",
            bg=BACKGROUND,
            font=("Segoe UI", 10, "underline"),
            cursor="hand2",
        ).pack(anchor="w", padx=20, pady=(16, 0))
        self.bind_back()

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=16)

        section_title(body, "Create Account").pack(anchor="w", pady=(0, 4))
        tk.Label(
            body,
            text="Sign up to explore Samarkand",
            fg="#666",
            bg=BACKGROUND,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(body, text="Full Name", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.name_entry = entry_field(body, "Enter your full name")
        self.name_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Email Address", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.email_entry = entry_field(body, "Enter your email")
        self.email_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Password", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.pass_entry = entry_field(body, "Minimum 8 characters", show="•")
        self.pass_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Confirm Password", fg=TEXT, bg=BACKGROUND, font=("Segoe UI", 10)).pack(
            anchor="w"
        )
        self.confirm_entry = entry_field(body, "Repeat password", show="•")
        self.confirm_entry.pack(fill=tk.X, pady=(4, 20), ipady=6)

        styled_button(body, "Continue with Email", command=self._register).pack(
            fill=tk.X, pady=(0, 12)
        )
        styled_button(
            body,
            "Continue with Google",
            command=lambda: messagebox.showinfo("LOCSAM", "Google sign-in is UI only."),
            style="secondary",
        ).pack(fill=tk.X)

        row = tk.Frame(body, bg=BACKGROUND)
        row.pack(pady=16)
        tk.Label(row, text="Already have an account? ", bg=BACKGROUND).pack(side=tk.LEFT)
        link_label(row, "Login", lambda: controller.show_frame("LoginFrame")).pack(side=tk.LEFT)

    def bind_back(self):
        for w in self.winfo_children():
            if isinstance(w, tk.Label) and w.cget("text") == "← Back":
                w.bind("<Button-1>", lambda e: self.controller.show_frame("SplashFrame"))

    def _register(self):
        name = get_entry_value(self.name_entry, "Enter your full name")
        email = get_entry_value(self.email_entry, "Enter your email")
        password = get_entry_value(self.pass_entry, "Minimum 8 characters")
        confirm = get_entry_value(self.confirm_entry, "Repeat password")

        if not name or not email or not password:
            messagebox.showerror("Validation", "Please fill in all fields.")
            return
        if len(password) < 8:
            messagebox.showerror("Validation", "Password must be at least 8 characters.")
            return
        if password != confirm:
            messagebox.showerror("Validation", "Passwords do not match.")
            return

        ok, msg = store.register_user(name, email, password)
        if ok:
            store.login_user(email, password)
            messagebox.showinfo("LOCSAM", msg)
            self.controller.show_frame("HomeFrame")
        else:
            messagebox.showerror("Registration", msg)
