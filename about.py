"""About LOCSAM page."""

import tkinter as tk

from theme import PAD_LG
from ui_utils import (
    back_button,
    c,
    create_card,
    create_label,
    scrollable_frame,
    subtitle_label,
)


class AboutFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=c("BACKGROUND"))
        self.controller = controller
        self._build()

    def on_show(self):
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _build(self):
        back_button(self, lambda: self.controller.show_frame("ProfileFrame"))

        scroll_container, _, inner = scrollable_frame(self)
        scroll_container.pack(fill=tk.BOTH, expand=True)

        col = tk.Frame(inner, bg=c("BACKGROUND"))
        col.pack(anchor="center", padx=PAD_LG, pady=PAD_LG)

        create_label(col, "What is LOCSAM?", style="heading").pack(anchor="w", pady=(0, 8))
        subtitle_label(
            col,
            "LOCSAM means Location Management. It is a platform designed to help users "
            "explore and discover amazing places, monuments, and museums in Samarkand.\n\n"
            "Our goal is to provide high-quality digital tourism experiences with a focus "
            "on design and smooth functionality.",
            wrap=520,
        ).pack(pady=(0, 16))

        create_label(col, "Team Members", style="subheading").pack(anchor="w", pady=(8, 4))
        for member in [
            "Frontend Developer",
            "Backend Developer",
            "UI/UX Designer",
            "Project Manager",
        ]:
            create_label(col, f"• {member}", style="body").pack(fill=tk.X, padx=8)

        create_label(col, "Contact Information", style="subheading").pack(
            anchor="w", pady=(16, 8)
        )
        contact_card = create_card(col, padx=16, pady=14)
        contact_card.pack(fill=tk.X, pady=(0, 24))
        for label, value in [
            ("Email", "info@locsam.com"),
            ("Telegram", "@locsam"),
            ("Location", "Samarkand, Uzbekistan"),
            ("Website", "www.locsam.com"),
        ]:
            row = tk.Frame(contact_card, bg=c("CARD"))
            row.pack(fill=tk.X, pady=4)
            create_label(
                row, f"{label}:", style="body", bg=c("CARD"), width=10
            ).pack(side=tk.LEFT)
            create_label(row, value, style="small", bg=c("CARD")).pack(side=tk.LEFT)
