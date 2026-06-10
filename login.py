"""User login page."""

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


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.remember_var = tk.BooleanVar(value=True)
        self._build()

    def on_show(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        back_button(self, lambda: self.controller.show_frame("SplashFrame"))

        _, card = form_card(self)

        create_label(card, t("welcome_back"), style="title", bg=c("CARD")).pack(
            anchor="w", pady=(0, 4)
        )
        create_label(card, t("login_sub"), style="small", bg=c("CARD")).pack(
            anchor="w", pady=(0, 20)
        )

        create_label(card, t("email"), style="body", bg=c("CARD")).pack(anchor="w")
        self.email_entry = entry_field(card, "Enter your email")
        self.email_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        create_label(card, t("password"), style="body", bg=c("CARD")).pack(anchor="w")
        self.pass_entry = entry_field(card, "Enter your password", show="•")
        self.pass_entry.pack(fill=tk.X, pady=(4, 8), ipady=6)

        opts = tk.Frame(card, bg=c("CARD"))
        opts.pack(fill=tk.X, pady=(0, 16))
        tk.Checkbutton(
            opts,
            text=t("remember_me"),
            variable=self.remember_var,
            bg=c("CARD"),
            fg=c("TEXT"),
            activebackground=c("CARD"),
            activeforeground=c("TEXT"),
            selectcolor=c("INPUT_BG"),
            font=("Segoe UI", 9),
        ).pack(side=tk.LEFT)
        link_label(
            opts,
            t("forgot_password"),
            lambda: messagebox.showinfo("LOCSAM", "Password reset coming with MySQL."),
            bg=c("CARD"),
        ).pack(side=tk.RIGHT)

        btn_col = button_row(card, max_width=400)
        styled_button(btn_col, t("login"), command=self._login, style="primary", full_width=True).pack(
            fill=tk.X, pady=(0, 8)
        )
        styled_button(
            btn_col,
            t("register"),
            command=lambda: self.controller.show_frame("RegisterFrame"),
            style="outline",
            full_width=True,
        ).pack(fill=tk.X)

    def _login(self):
        email = get_entry_value(self.email_entry, "Enter your email")
        password = get_entry_value(self.pass_entry, "Enter your password")
        if not email or not password:
            messagebox.showerror("Validation", t("validation_email_pass"))
            return
        remember = self.remember_var.get()
        ok, msg = store.login_user(email, password, remember=remember)
        if ok:
            if not remember:
                store.clear_remember_user()
            self.controller.show_frame("HomeFrame")
        else:
            messagebox.showerror("Login Failed", msg)
