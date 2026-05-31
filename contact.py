"""Contact support page."""

import tkinter as tk
from tkinter import messagebox

from config import BACKGROUND, PRIMARY, TEXT
from models import store
from ui_utils import entry_field, get_entry_value, section_title, styled_button


class ContactFrame(tk.Frame):
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

        body = tk.Frame(self, bg=BACKGROUND, padx=24)
        body.pack(fill=tk.BOTH, expand=True)

        section_title(body, "Help & Support").pack(anchor="w", pady=(0, 4))
        tk.Label(
            body,
            text="Send us a message and we'll get back to you.",
            fg="#666",
            bg=BACKGROUND,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(body, text="Name", fg=TEXT, bg=BACKGROUND).pack(anchor="w")
        self.name_entry = entry_field(body, "Your name")
        self.name_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Email", fg=TEXT, bg=BACKGROUND).pack(anchor="w")
        self.email_entry = entry_field(body, "Your email")
        self.email_entry.pack(fill=tk.X, pady=(4, 12), ipady=6)

        tk.Label(body, text="Message", fg=TEXT, bg=BACKGROUND).pack(anchor="w")
        self.message_text = tk.Text(
            body,
            height=6,
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground="#E0E0E0",
            highlightcolor=PRIMARY,
        )
        self.message_text.pack(fill=tk.X, pady=(4, 20))

        styled_button(body, "Send Message", command=self._send).pack(fill=tk.X)

    def _send(self):
        name = get_entry_value(self.name_entry, "Your name")
        email = get_entry_value(self.email_entry, "Your email")
        message = self.message_text.get("1.0", tk.END).strip()

        if not name or not email or not message:
            messagebox.showerror("Validation", "Please fill in all fields.")
            return
        if "@" not in email:
            messagebox.showerror("Validation", "Please enter a valid email.")
            return

        store.save_contact(name, email, message)
        messagebox.showinfo("LOCSAM", "Message sent successfully!")
        self.message_text.delete("1.0", tk.END)
        self.controller.show_frame("ProfileFrame")
