"""About LOCSAM page."""

import tkinter as tk

from config import BACKGROUND, CARD, PRIMARY, TEXT, TEXT_LIGHT
from ui_utils import scrollable_frame, section_title, subtitle_label


class AboutFrame(tk.Frame):
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
        back.pack(anchor="w", padx=16, pady=12)
        back.bind("<Button-1>", lambda e: controller.show_frame("ProfileFrame"))

        scroll_container, _, inner = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        section_title(inner, "What is LOCSAM?").pack(anchor="w", padx=16, pady=(0, 8))
        subtitle_label(
            inner,
            "LOCSAM means Location Management. It is a platform designed to help users "
            "explore and discover amazing places, monuments, and museums in Samarkand.\n\n"
            "Our goal is to provide high-quality digital tourism experiences with a focus "
            "on design and smooth functionality.",
        ).pack(padx=16, pady=(0, 16))

        section_title(inner, "Team Members").pack(anchor="w", padx=16, pady=(8, 4))
        for member in [
            "Frontend Developer",
            "Backend Developer",
            "UI/UX Designer",
            "Proje ct Manager",
        ]:
            tk.Label(
                inner,
                text=f"• {member}",
                font=("Segoe UI", 10),
                fg=TEXT,
                bg=BACKGROUND,
                anchor="w",
            ).pack(fill=tk.X, padx=20)

        section_title(inner, "Contact Information").pack(anchor="w", padx=16, pady=(16, 4))
        contact_card = tk.Frame(inner, bg=CARD, padx=14, pady=12)
        contact_card.pack(fill=tk.X, padx=16, pady=(0, 24))
        for label, value in [
            ("Email", "info@locsam.com"),
            ("Telegram", "@locsam"),
            ("Location", "Samarkand, Uzbekistan"),
            ("Website", "www.locsam.com"),
        ]:
            row = tk.Frame(contact_card, bg=CARD)
            row.pack(fill=tk.X, pady=3)
            tk.Label(row, text=f"{label}:", font=("Segoe UI", 10, "bold"), fg=TEXT, bg=CARD, width=10, anchor="w").pack(
                side=tk.LEFT
            )
            tk.Label(row, text=value, font=("Segoe UI", 10), fg=TEXT_LIGHT, bg=CARD, anchor="w").pack(
                side=tk.LEFT
            )
  