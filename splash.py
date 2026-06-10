"""Splash screen — LOCSAM entry point."""

import tkinter as tk

from i18n import t
from theme import HERO_HEIGHT
from ui_utils import (
    button_row,
    c,
    centered_column,
    create_label,
    load_image,
    styled_button,
)


class SplashFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self._build()

    def on_show(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        hero = tk.Frame(self, bg=c("OVERLAY"), height=HERO_HEIGHT)
        hero.pack(fill=tk.X)
        hero.pack_propagate(False)

        try:
            bg_img = load_image("splash_bg", size=(1200, HERO_HEIGHT))
            lbl_img = tk.Label(hero, image=bg_img, bg=c("OVERLAY"))
            lbl_img.image = bg_img
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        except Exception:
            pass

        overlay = tk.Frame(hero, bg=c("OVERLAY"))
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        create_label(
            overlay,
            "LOCSAM",
            style="title",
            bg=c("OVERLAY"),
            fg=c("HEADER_TEXT"),
            font=("Segoe UI", 42, "bold"),
        ).pack(pady=(100, 8))

        create_label(
            overlay,
            t("splash_subtitle"),
            style="inverse",
            bg=c("OVERLAY"),
            justify="center",
        ).pack(pady=8)

        body = tk.Frame(self, bg=c("BACKGROUND"))
        body.pack(fill=tk.BOTH, expand=True, pady=32)

        col = centered_column(body)
        btn_col = tk.Frame(col, bg=c("BACKGROUND"))
        btn_col.pack()

        styled_button(
            btn_col,
            t("create_account"),
            command=lambda: self.controller.show_frame("RegisterFrame"),
            style="primary",
            full_width=True,
        ).pack(fill=tk.X, ipadx=40, ipady=2)

        row = tk.Frame(col, bg=c("BACKGROUND"))
        row.pack(pady=16)
        create_label(row, t("already_have") + " ", style="muted", bg=c("BACKGROUND")).pack(
            side=tk.LEFT
        )
        from ui_utils import link_label

        link_label(
            row,
            t("login"),
            lambda: self.controller.show_frame("LoginFrame"),
            bg=c("BACKGROUND"),
        ).pack(side=tk.LEFT)

        admin_row = button_row(col)
        styled_button(
            admin_row,
            t("admin_login"),
            command=lambda: self.controller.show_frame("AdminLoginFrame"),
            style="outline",
            width=22,
        ).pack()
