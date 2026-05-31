"""User profile page."""

import tkinter as tk
from tkinter import messagebox

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT, WHITE
from models import store
from ui_utils import bottom_nav


class ProfileFrame(tk.Frame):
    MENU_ITEMS = [
        ("❤", "Saved Places", "FavoritesFrame"),
        ("🎫", "My Tickets", "MyTicketsFrame"),
        ("🌐", "Language", None),
        ("🌙", "Dark Mode", None),
        ("❓", "Help & Support", "ContactFrame"),
        ("ℹ", "About LOCSAM", "AboutFrame"),
        ("🚪", "Logout", "logout"),
    ]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.dark_mode = tk.BooleanVar(value=False)

        header = tk.Frame(self, bg=PRIMARY, padx=20, pady=24)
        header.pack(fill=tk.X)

        user = store.current_user or {"full_name": "Guest User", "email": "guest@locsam.com"}

        avatar = tk.Frame(header, bg=WHITE, width=56, height=56)
        avatar.pack(anchor="w")
        avatar.pack_propagate(False)
        tk.Label(
            avatar,
            text=user["full_name"][0].upper(),
            font=("Segoe UI", 22, "bold"),
            fg=PRIMARY,
            bg=WHITE,
        ).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(header, bg=PRIMARY)
        info.pack(fill=tk.X, pady=(12, 0))
        tk.Label(
            info,
            text=user["full_name"],
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg=PRIMARY,
            anchor="w",
        ).pack(fill=tk.X)
        tk.Label(
            info,
            text=user["email"],
            font=("Segoe UI", 10),
            fg="#E0D4FF",
            bg=PRIMARY,
            anchor="w",
        ).pack(fill=tk.X)

        menu = tk.Frame(self, bg=BACKGROUND, padx=16, pady=12)
        menu.pack(fill=tk.BOTH, expand=True)

        for icon, label, target in self.MENU_ITEMS:
            row = tk.Frame(menu, bg=CARD, cursor="hand2")
            row.pack(fill=tk.X, pady=4)
            inner = tk.Frame(row, bg=CARD, padx=14, pady=12)
            inner.pack(fill=tk.X)
            tk.Label(inner, text=icon, font=("Segoe UI", 14), bg=CARD).pack(side=tk.LEFT)
            tk.Label(
                inner,
                text=label,
                font=("Segoe UI", 11),
                fg=TEXT,
                bg=CARD,
            ).pack(side=tk.LEFT, padx=10)
            tk.Label(inner, text="›", font=("Segoe UI", 14), fg=TEXT_LIGHT, bg=CARD).pack(
                side=tk.RIGHT
            )

            def handler(_=None, t=target, lbl=label):
                self._menu_action(t, lbl)

            for w in (row, inner):
                w.bind("<Button-1>", handler)
            for c in inner.winfo_children():
                c.bind("<Button-1>", handler)

        bottom_nav(
            self,
            [("🏠", "Home"), ("🔍", "Search"), ("🎫", "Tickets"), ("❤", "Saved"), ("👤", "Profile")],
            4,
            self._nav_select,
        )

    def _nav_select(self, idx):
        frames = ["HomeFrame", "SearchFrame", "MyTicketsFrame", "FavoritesFrame", "ProfileFrame"]
        self.controller.show_frame(frames[idx])

    def _menu_action(self, target, label):
        if target == "logout":
            store.logout_user()
            messagebox.showinfo("LOCSAM", "Logged out successfully.")
            self.controller.show_frame("SplashFrame")
        elif label == "Dark Mode":
            self.dark_mode.set(not self.dark_mode.get())
            state = "enabled" if self.dark_mode.get() else "disabled"
            messagebox.showinfo("LOCSAM", f"Dark mode {state} (UI demo).")
        elif label == "Language":
            messagebox.showinfo("LOCSAM", "Language settings coming soon.")
        elif target:
            self.controller.show_frame(target)
