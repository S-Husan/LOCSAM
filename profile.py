"""User profile page."""

import tkinter as tk
from tkinter import messagebox

from i18n import t
from models import store
from theme import theme_manager
from ui_utils import apply_theme_to_widget, bottom_nav, c, show_language_dialog


class ProfileFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self.body = tk.Frame(self, bg=c("BACKGROUND"))
        self.body.pack(fill=tk.BOTH, expand=True)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        user = store.current_user
        if user:
            name = user["full_name"]
            email = user["email"]
        else:
            name = t("guest")
            email = "guest@locsam.com"

        header = tk.Frame(self.body, bg=c("PRIMARY"), padx=24, pady=28)
        header.pack(fill=tk.X)

        avatar = tk.Frame(header, bg=c("WHITE"), width=64, height=64)
        avatar.pack(anchor="w")
        avatar.pack_propagate(False)
        tk.Label(
            avatar,
            text=name[0].upper(),
            font=("Segoe UI", 24, "bold"),
            fg=c("PRIMARY"),
            bg=c("WHITE"),
        ).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(header, bg=c("PRIMARY"))
        info.pack(fill=tk.X, pady=(14, 0))
        self.name_label = tk.Label(
            info,
            text=name,
            font=("Segoe UI", 18, "bold"),
            fg=c("HEADER_TEXT"),
            bg=c("PRIMARY"),
            anchor="w",
        )
        self.name_label.pack(fill=tk.X)
        self.email_label = tk.Label(
            info,
            text=email,
            font=("Segoe UI", 11),
            fg=c("HEADER_SUB"),
            bg=c("PRIMARY"),
            anchor="w",
        )
        self.email_label.pack(fill=tk.X)

        menu = tk.Frame(self.body, bg=c("BACKGROUND"), padx=20, pady=12)
        menu.pack(fill=tk.BOTH, expand=True)

        items = [
            ("❤", "saved_places", "FavoritesFrame"),
            ("🎫", "my_tickets", "MyTicketsFrame"),
            ("🌐", "language", None),
            ("🌙", "dark_mode", None),
            ("❓", "help_support", "ContactFrame"),
            ("ℹ", "about", "AboutFrame"),
            ("🚪", "logout", "logout"),
        ]

        for icon, key, target in items:
            row = tk.Frame(menu, bg=c("CARD"), cursor="hand2")
            row.pack(fill=tk.X, pady=5)
            inner = tk.Frame(row, bg=c("CARD"), padx=16, pady=14)
            inner.pack(fill=tk.X)
            tk.Label(inner, text=icon, font=("Segoe UI", 14), bg=c("CARD")).pack(side=tk.LEFT)
            tk.Label(
                inner,
                text=t(key),
                font=("Segoe UI", 11),
                fg=c("TEXT"),
                bg=c("CARD"),
            ).pack(side=tk.LEFT, padx=12)
            extra = ""
            if key == "dark_mode" and theme_manager.dark_mode:
                extra = " ✓"
            if key == "language":
                extra = f" ({store.settings.get('language', 'en').upper()})"
            tk.Label(
                inner,
                text=f"›{extra}",
                font=("Segoe UI", 14),
                fg=c("TEXT_LIGHT"),
                bg=c("CARD"),
            ).pack(side=tk.RIGHT)

            def handler(_=None, tgt=target, lbl_key=key):
                self._menu_action(tgt, lbl_key)

            for w in (row, inner):
                w.bind("<Button-1>", handler)
            for ch in inner.winfo_children():
                ch.bind("<Button-1>", handler)

        bottom_nav(
            self.body,
            [
                ("🏠", t("home")),
                ("🔍", t("search")),
                ("🎫", t("tickets")),
                ("❤", t("saved")),
                ("👤", t("profile")),
            ],
            4,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _menu_action(self, target, key):
        if target == "logout":
            store.logout_user()
            messagebox.showinfo("LOCSAM", t("logged_out"))
            self.controller.show_frame("SplashFrame")
        elif key == "dark_mode":
            enabled = theme_manager.toggle()
            store.set_dark_mode(enabled)
            messagebox.showinfo(
                "LOCSAM",
                t("dark_enabled") if enabled else t("dark_disabled"),
            )
            self.controller.apply_theme()
        elif key == "language":
            show_language_dialog(self, lambda: self.controller.apply_theme())
        elif target:
            self.controller.show_frame(target)
