"""User profile page."""

import tkinter as tk
from tkinter import messagebox

from i18n import t
from models import store
from theme import CONTENT_MAX_WIDTH, PAD_LG, theme_manager
from ui_utils import (
    bottom_nav,
    c,
    create_card,
    create_label,
    show_language_dialog,
)


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

        header = tk.Frame(self.body, bg=c("PRIMARY"), padx=PAD_LG, pady=28)
        header.pack(fill=tk.X)

        hdr_inner = tk.Frame(header, bg=c("PRIMARY"))
        hdr_inner.pack(anchor="center")

        avatar = tk.Frame(hdr_inner, bg=c("INPUT_BG"), width=68, height=68)
        avatar.pack(anchor="w")
        avatar.pack_propagate(False)
        create_label(
            avatar,
            name[0].upper(),
            style="title",
            bg=c("INPUT_BG"),
            fg=c("PRIMARY"),
        ).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(hdr_inner, bg=c("PRIMARY"))
        info.pack(fill=tk.X, pady=(14, 0))
        create_label(info, name, style="heading", bg=c("PRIMARY"), fg=c("HEADER_TEXT")).pack(
            fill=tk.X
        )
        create_label(info, email, style="small", bg=c("PRIMARY"), fg=c("HEADER_SUB")).pack(
            fill=tk.X
        )

        menu_wrap = tk.Frame(self.body, bg=c("BACKGROUND"))
        menu_wrap.pack(fill=tk.BOTH, expand=True, pady=PAD_LG)
        menu = tk.Frame(menu_wrap, bg=c("BACKGROUND"))
        menu.pack(anchor="center")

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
            row = create_card(menu, padx=16, pady=12)
            row.pack(fill=tk.X, pady=5)
            row.config(cursor="hand2")

            inner = tk.Frame(row, bg=c("CARD"))
            inner.pack(fill=tk.X)
            create_label(inner, icon, style="body", bg=c("CARD")).pack(side=tk.LEFT)
            create_label(inner, t(key), style="body", bg=c("CARD")).pack(
                side=tk.LEFT, padx=12
            )
            extra = ""
            if key == "dark_mode" and theme_manager.dark_mode:
                extra = " ✓"
            if key == "language":
                extra = f" ({store.settings.get('language', 'en').upper()})"
            create_label(
                inner,
                f"›{extra}",
                style="muted",
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
            self.controller.apply_theme()
            messagebox.showinfo(
                "LOCSAM",
                t("dark_enabled") if enabled else t("dark_disabled"),
            )
        elif key == "language":
            show_language_dialog(self, lambda: self.controller.apply_theme())
        elif target:
            self.controller.show_frame(target)
