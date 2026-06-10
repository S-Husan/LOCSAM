"""User registration page."""

import tkinter as tk
from tkinter import messagebox

from i18n import t
from models import store
from ui_utils import (
    back_button,
    button_row,
    c,
    create_label,
    entry_field,
    form_card,
    get_entry_value,
    link_label,
    styled_button,
)


class RegisterFrame(tk.Frame):
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

        create_label(card, t("register_title"), style="title", bg=c("CARD")).pack(
            anchor="w", pady=(0, 4)
        )
        create_label(card, t("register_sub"), style="small", bg=c("CARD")).pack(
            anchor="w", pady=(0, 20)
        )

        for label_key, attr, placeholder, show in [
            ("full_name", "name_entry", "Enter your full name", None),
            ("email", "email_entry", "Enter your email", None),
            ("password", "pass_entry", "Minimum 8 characters", "•"),
            ("confirm_password", "confirm_entry", "Repeat password", "•"),
        ]:
            create_label(card, t(label_key), style="body", bg=c("CARD")).pack(anchor="w")
            entry = entry_field(card, placeholder, show=show)
            entry.pack(fill=tk.X, pady=(4, 12), ipady=6)
            setattr(self, attr, entry)

        btn_col = button_row(card, max_width=400)
        styled_button(
            btn_col,
            t("continue_email"),
            command=self._register,
            style="primary",
            full_width=True,
        ).pack(fill=tk.X, pady=(0, 8))
        styled_button(
            btn_col,
            t("continue_google"),
            command=lambda: messagebox.showinfo("LOCSAM", "Google sign-in is UI only."),
            style="outline",
            full_width=True,
        ).pack(fill=tk.X)

        row = tk.Frame(card, bg=c("CARD"))
        row.pack(pady=16)
        create_label(row, t("already_have") + " ", style="muted", bg=c("CARD")).pack(
            side=tk.LEFT
        )
        link_label(
            row,
            t("login"),
            lambda: self.controller.show_frame("LoginFrame"),
            bg=c("CARD"),
        ).pack(side=tk.LEFT)

    def _register(self):
        name = get_entry_value(self.name_entry, "Enter your full name")
        email = get_entry_value(self.email_entry, "Enter your email")
        password = get_entry_value(self.pass_entry, "Minimum 8 characters")
        confirm = get_entry_value(self.confirm_entry, "Repeat password")

        if not name or not email or not password:
            messagebox.showerror("Validation", t("validation_fill"))
            return
        if len(password) < 8:
            messagebox.showerror("Validation", t("validation_password_len"))
            return
        if password != confirm:
            messagebox.showerror("Validation", t("validation_password_match"))
            return

        ok, msg = store.register_user(name, email, password)
        if ok:
            store.login_user(email, password)
            messagebox.showinfo("LOCSAM", msg)
            self.controller.show_frame("HomeFrame")
        else:
            messagebox.showerror("Registration", msg)
