"""Splash screen — LOCSAM entry point."""

import tkinter as tk

from config import BACKGROUND, PRIMARY, TEXT, WHITE
from ui_utils import link_label, load_image, styled_button


class SplashFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller

        hero = tk.Frame(self, bg=PRIMARY, height=420)
        hero.pack(fill=tk.X)
        hero.pack_propagate(False)

        try:
            bg_img = load_image("splash_bg", size=(420, 420))
            lbl_img = tk.Label(hero, image=bg_img, bg=PRIMARY)
            lbl_img.image = bg_img
            lbl_img.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception:
            pass

        overlay = tk.Frame(hero, bg=PRIMARY)
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)

        tk.Label(
            overlay,
            text="LOCSAM",
            font=("Segoe UI", 42, "bold"),
            fg=WHITE,
            bg=PRIMARY,
        ).pack(pady=(120, 8))

        tk.Label(
            overlay,
            text="Join over 10,000 travelers around the world\nand enjoy your travel.",
            font=("Segoe UI", 12),
            fg=WHITE,
            bg=PRIMARY,
            justify="center",
        ).pack(pady=8)

        body = tk.Frame(self, bg=BACKGROUND)
        body.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        styled_button(
            body,
            "Create Account",
            command=lambda: controller.show_frame("RegisterFrame"),
        ).pack(fill=tk.X, pady=(40, 16))

        row = tk.Frame(body, bg=BACKGROUND)
        row.pack()
        tk.Label(row, text="Already have an account? ", fg=TEXT, bg=BACKGROUND).pack(
            side=tk.LEFT
        )
        link_label(row, "Login", lambda: controller.show_frame("LoginFrame")).pack(
            side=tk.LEFT
        )

        admin_row = tk.Frame(body, bg=BACKGROUND)
        admin_row.pack(pady=20)
        link_label(
            admin_row,
            "Admin Login",
            lambda: controller.show_frame("AdminLoginFrame"),
        ).pack()
