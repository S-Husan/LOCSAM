"""Admin dashboard with full CRUD panels."""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from config import BACKGROUND, CARD, DANGER, PRIMARY, SECONDARY, TEXT, TEXT_LIGHT, WHITE
from models import store
from reports import get_report_data
from ui_utils import entry_field, get_entry_value, scrollable_frame, styled_button


class AdminDashboardFrame(tk.Frame):
    SIDEBAR_ITEMS = [
        "Dashboard",
        "Users",
        "Locations",
        "Tickets",
        "Reviews",
        "Contact Messages",
        "Reports",
        "Logout",
    ]

    def __init__(self, parent, controller):
        super().__init__(parent, bg=BACKGROUND)
        self.controller = controller
        self.active_section = "Dashboard"
        self.sidebar_labels = {}

        layout = tk.Frame(self, bg=BACKGROUND)
        layout.pack(fill=tk.BOTH, expand=True)

        self.sidebar = tk.Frame(layout, bg=PRIMARY, width=140)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="LOCSAM\nAdmin",
            font=("Segoe UI", 14, "bold"),
            fg=WHITE,
            bg=PRIMARY,
            pady=16,
        ).pack()

        for item in self.SIDEBAR_ITEMS:
            lbl = tk.Label(
                self.sidebar,
                text=item,
                font=("Segoe UI", 10),
                fg=WHITE,
                bg=PRIMARY,
                anchor="w",
                padx=16,
                pady=10,
                cursor="hand2",
            )
            lbl.pack(fill=tk.X)
            lbl.bind("<Button-1>", lambda e, s=item: self._select_section(s))
            self.sidebar_labels[item] = lbl

        self.main = tk.Frame(layout, bg=BACKGROUND)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.content = tk.Frame(self.main, bg=BACKGROUND)
        self.content.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

    def on_show(self):
        self._select_section(self.active_section)

    def _select_section(self, section):
        if section == "Logout":
            store.logout_admin()
            self.controller.show_frame("SplashFrame")
            return

        self.active_section = section
        for name, lbl in self.sidebar_labels.items():
            lbl.config(bg=SECONDARY if name == section else PRIMARY)

        for w in self.content.winfo_children():
            w.destroy()

        builders = {
            "Dashboard": self._build_dashboard,
            "Users": self._build_users,
            "Locations": self._build_locations,
            "Tickets": self._build_tickets,
            "Reviews": self._build_reviews,
            "Contact Messages": self._build_contact,
            "Reports": self._build_reports,
        }
        builders.get(section, self._build_dashboard)()

    def _title(self, text):
        tk.Label(
            self.content,
            text=text,
            font=("Segoe UI", 18, "bold"),
            fg=TEXT,
            bg=BACKGROUND,
            anchor="w",
        ).pack(fill=tk.X, pady=(0, 12))

    def _build_dashboard(self):
        self._title("Dashboard")
        data = get_report_data()
        grid = tk.Frame(self.content, bg=BACKGROUND)
        grid.pack(fill=tk.X)
        stats = [
            ("Total Users", data["total_users"]),
            ("Total Locations", data["total_locations"]),
            ("Tickets Sold", data["total_tickets"]),
            ("Revenue", f"${data['total_revenue']}"),
        ]
        for i, (label, val) in enumerate(stats):
            card = tk.Frame(grid, bg=CARD, padx=12, pady=12)
            card.grid(row=i // 2, column=i % 2, padx=6, pady=6, sticky="nsew")
            tk.Label(card, text=label, font=("Segoe UI", 9), fg=TEXT_LIGHT, bg=CARD).pack(anchor="w")
            tk.Label(card, text=str(val), font=("Segoe UI", 20, "bold"), fg=PRIMARY, bg=CARD).pack(
                anchor="w"
            )

    def _build_users(self):
        self._title("User Management")
        search_row = tk.Frame(self.content, bg=BACKGROUND)
        search_row.pack(fill=tk.X, pady=(0, 8))
        self.user_search = entry_field(search_row, "Search users...")
        self.user_search.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)
        tk.Button(
            search_row,
            text="Search",
            bg=PRIMARY,
            fg=WHITE,
            relief=tk.FLAT,
            command=self._refresh_users,
        ).pack(side=tk.LEFT, padx=6)

        _, _, self.users_list = scrollable_frame(self.content)
        self._refresh_users()

    def _refresh_users(self):
        for w in self.users_list.winfo_children():
            w.destroy()
        q = get_entry_value(self.user_search, "Search users...").lower()
        users = [u for u in store.users if not q or q in u["email"].lower() or q in u["full_name"].lower()]

        for u in users:
            row = tk.Frame(self.users_list, bg=CARD, padx=10, pady=8)
            row.pack(fill=tk.X, pady=4)
            tk.Label(
                row,
                text=f"{u['full_name']}  ·  {u['email']}",
                font=("Segoe UI", 10),
                fg=TEXT,
                bg=CARD,
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

            tk.Button(
                row,
                text="Edit",
                bg=PRIMARY,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda uid=u["id"], n=u["full_name"], e=u["email"]: self._edit_user(uid, n, e),
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                row,
                text="Delete",
                bg=DANGER,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda uid=u["id"]: self._delete_user(uid),
            ).pack(side=tk.RIGHT)

    def _edit_user(self, uid, name, email):
        new_name = simpledialog.askstring("Edit User", "Full name:", initialvalue=name)
        new_email = simpledialog.askstring("Edit User", "Email:", initialvalue=email)
        if new_name and new_email:
            store.update_user(uid, new_name, new_email)
            self._refresh_users()

    def _delete_user(self, uid):
        if messagebox.askyesno("Confirm", "Delete this user?"):
            store.delete_user(uid)
            self._refresh_users()

    def _build_locations(self):
        self._title("Location Management")
        styled_button(
            self.content,
            "+ Add Location",
            command=self._add_location,
        ).pack(anchor="w", pady=(0, 8))

        _, _, self.loc_list = scrollable_frame(self.content)
        self._refresh_locations()

    def _refresh_locations(self):
        for w in self.loc_list.winfo_children():
            w.destroy()
        for loc in store.locations:
            row = tk.Frame(self.loc_list, bg=CARD, padx=10, pady=8)
            row.pack(fill=tk.X, pady=4)
            tk.Label(
                row,
                text=f"{loc['name']}  ·  {loc['category']}  ·  ${loc['price']}",
                font=("Segoe UI", 10),
                fg=TEXT,
                bg=CARD,
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Button(
                row,
                text="Edit",
                bg=PRIMARY,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda l=loc: self._edit_location(l),
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                row,
                text="Delete",
                bg=DANGER,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda lid=loc["id"]: self._delete_location(lid),
            ).pack(side=tk.RIGHT)

    def _add_location(self):
        name = simpledialog.askstring("Add Location", "Name:")
        if not name:
            return
        store.add_location(
            {
                "name": name,
                "category": "Monument",
                "city": "Samarkand, Uzbekistan",
                "description": "New location",
                "rating": 4.0,
                "reviews": 0,
                "price": 5,
                "open_time": "06:00 AM - 09:00 PM",
                "latitude": 39.65,
                "longitude": 66.97,
                "image": "registan",
            }
        )
        self._refresh_locations()

    def _edit_location(self, loc):
        price = simpledialog.askfloat("Edit Price", "Ticket price:", initialvalue=loc["price"])
        if price is not None:
            store.update_location(loc["id"], {"price": price})
            self._refresh_locations()

    def _delete_location(self, lid):
        if messagebox.askyesno("Confirm", "Delete this location?"):
            store.delete_location(lid)
            self._refresh_locations()

    def _build_tickets(self):
        self._title("Ticket Management")
        _, _, frame = scrollable_frame(self.content)
        bookings = store.get_all_bookings()
        for i, b in enumerate(bookings):
            row = tk.Frame(frame, bg=CARD, padx=10, pady=8)
            row.pack(fill=tk.X, pady=4)
            tk.Label(
                row,
                text=f"{b['location']}  ·  {b['date']}  ·  ${b['price']}  ·  {b.get('status', 'upcoming')}",
                font=("Segoe UI", 10),
                fg=TEXT,
                bg=CARD,
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Button(
                row,
                text="Approve",
                bg=PRIMARY,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda idx=i: self._set_status(idx, "approved"),
            ).pack(side=tk.RIGHT, padx=2)
            tk.Button(
                row,
                text="Cancel",
                bg=DANGER,
                fg=WHITE,
                relief=tk.FLAT,
                command=lambda idx=i: self._set_status(idx, "cancelled"),
            ).pack(side=tk.RIGHT)

    def _set_status(self, idx, status):
        store.update_booking_status(idx, status)
        messagebox.showinfo("LOCSAM", f"Booking marked as {status}.")
        self._select_section("Tickets")

    def _build_reviews(self):
        self._title("Reviews")
        tk.Label(
            self.content,
            text="No user reviews yet. Reviews will appear when MySQL is connected.",
            fg=TEXT_LIGHT,
            bg=BACKGROUND,
            font=("Segoe UI", 11),
        ).pack(pady=20)

    def _build_contact(self):
        self._title("Contact Messages")
        _, _, frame = scrollable_frame(self.content)
        if not store.contact_messages:
            tk.Label(frame, text="No messages yet.", bg=BACKGROUND, fg=TEXT_LIGHT).pack(pady=20)
            return
        for msg in store.contact_messages:
            card = tk.Frame(frame, bg=CARD, padx=10, pady=8)
            card.pack(fill=tk.X, pady=4)
            tk.Label(
                card,
                text=f"{msg['name']}  ·  {msg['email']}  ·  {msg['created_at']}",
                font=("Segoe UI", 10, "bold"),
                fg=TEXT,
                bg=CARD,
                anchor="w",
            ).pack(fill=tk.X)
            tk.Label(
                card,
                text=msg["message"],
                font=("Segoe UI", 9),
                fg=TEXT_LIGHT,
                bg=CARD,
                wraplength=500,
                justify="left",
            ).pack(fill=tk.X, pady=(4, 0))

    def _build_reports(self):
        self._title("Reports")
        data = get_report_data()
        for key, val in data.items():
            row = tk.Frame(self.content, bg=CARD, padx=12, pady=10)
            row.pack(fill=tk.X, pady=4)
            tk.Label(
                row,
                text=key.replace("_", " ").title(),
                font=("Segoe UI", 11),
                fg=TEXT,
                bg=CARD,
            ).pack(side=tk.LEFT)
            tk.Label(
                row,
                text=str(val if key != "total_revenue" else f"${val}"),
                font=("Segoe UI", 14, "bold"),
                fg=PRIMARY,
                bg=CARD,
            ).pack(side=tk.RIGHT)
