"""Contact support page."""

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
    styled_button,
)


class ContactFrame(tk.Frame):
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

        _, card = form_card(self)

        create_label(card, t("help_support"), style="title", bg=c("CARD")).pack(
            anchor="w", pady=(0, 4)
        )
        create_label(
            card,
            "Send us a message and we'll get back to you.",
            style="small",
            bg=c("CARD"),
        ).pack(anchor="w", pady=(0, 20))

        create_label(card, "Name", style="body", bg=c("CARD")).pack(anchor="w")
        self.name_entry = entry_field(card, "Your name")
        self.name_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        create_label(card, "Email", style="body", bg=c("CARD")).pack(anchor="w")
        self.email_entry = entry_field(card, "Your email")
        self.email_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        create_label(card, "Message", style="body", bg=c("CARD")).pack(anchor="w")
        self.message_text = tk.Text(
            card,
            height=6,
            font=("Segoe UI", 11),
            bg=c("INPUT_BG"),
            fg=c("TEXT"),
            insertbackground=c("TEXT"),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=c("BORDER"),
            highlightcolor=c("PRIMARY"),
        )
        self.message_text.pack(fill=tk.X, pady=(4, 20))

        btn_col = button_row(card)
        styled_button(
            btn_col,
            t("send_message"),
            command=self._send,
            style="primary",
            width=20,
        ).pack()

    def _send(self):
        name = get_entry_value(self.name_entry, "Your name")
        email = get_entry_value(self.email_entry, "Your email")
        message = self.message_text.get("1.0", tk.END).strip()

        if not name or not email or not message:
            messagebox.showerror("Validation", t("validation_fill"))
            return
        if "@" not in email:
            messagebox.showerror("Validation", "Please enter a valid email.")
            return

        store.save_contact(name, email, message)
        messagebox.showinfo("LOCSAM", "Message sent successfully!")
        self.controller.show_frame("ProfileFrame")
