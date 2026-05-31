"""In-memory data store for LOCSAM UI demo (replaces MySQL for now)."""

from datetime import datetime

from config import ADMIN_PASSWORD, ADMIN_USERNAME, DEMO_USER
from data import LOCATIONS, SAMPLE_TICKETS_UPCOMING


class DataStore:
    """Singleton-style in-memory store mimicking database operations."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        self.users = [
            {
                "id": 1,
                "full_name": DEMO_USER["full_name"],
                "email": DEMO_USER["email"],
                "password": "password123",
                "created_at": "2025-01-15",
            }
        ]
        self.admins = [{"id": 1, "username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}]
        self.locations = [dict(loc) for loc in LOCATIONS]
        self.gallery = self._build_gallery()
        self.tickets = [dict(t) for t in SAMPLE_TICKETS_UPCOMING]
        self.ticket_records = []
        self.favorites = set()
        self.reviews = []
        self.contact_messages = []
        self.current_user = None
        self.current_admin = None
        self._next_ids = {
            "users": 2,
            "locations": 7,
            "tickets": 4,
            "contact": 1,
        }

    def _build_gallery(self):
        gallery = []
        gid = 1
        for loc in LOCATIONS:
            for i in range(1, 4):
                gallery.append(
                    {"id": gid, "location_id": loc["id"], "image_path": f"{loc['image']}_{i}"}
                )
                gid += 1
        return gallery

    # --- Auth ---
    def register_user(self, full_name, email, password):
        if any(u["email"].lower() == email.lower() for u in self.users):
            return False, "Email already registered."
        uid = self._next_ids["users"]
        self._next_ids["users"] += 1
        self.users.append(
            {
                "id": uid,
                "full_name": full_name,
                "email": email,
                "password": password,
                "created_at": datetime.now().strftime("%Y-%m-%d"),
            }
        )
        return True, "Registration successful."

    def login_user(self, email, password):
        for u in self.users:
            if u["email"].lower() == email.lower() and u["password"] == password:
                self.current_user = u
                return True, "Welcome back!"
        return False, "Invalid email or password."

    def login_admin(self, username, password):
        for a in self.admins:
            if a["username"] == username and a["password"] == password:
                self.current_admin = a
                return True, "Admin login successful."
        return False, "Invalid admin credentials."

    def logout_user(self):
        self.current_user = None

    def logout_admin(self):
        self.current_admin = None

    # --- Locations ---
    def get_locations(self, category="All", search=""):
        results = self.locations
        if category and category != "All":
            if category == "Popular":
                results = sorted(results, key=lambda x: x["rating"], reverse=True)
            else:
                results = [l for l in results if l["category"] == category]
        if search:
            q = search.lower()
            results = [
                l
                for l in results
                if q in l["name"].lower() or q in l["category"].lower()
            ]
        return results

    def get_location(self, location_id):
        for loc in self.locations:
            if loc["id"] == location_id:
                return loc
        return None

    def get_gallery(self, location_id):
        return [g for g in self.gallery if g["location_id"] == location_id]

    def add_location(self, data):
        lid = self._next_ids["locations"]
        self._next_ids["locations"] += 1
        data["id"] = lid
        self.locations.append(data)
        return lid

    def update_location(self, location_id, data):
        for i, loc in enumerate(self.locations):
            if loc["id"] == location_id:
                self.locations[i] = {**loc, **data, "id": location_id}
                return True
        return False

    def delete_location(self, location_id):
        self.locations = [l for l in self.locations if l["id"] != location_id]
        self.gallery = [g for g in self.gallery if g["location_id"] != location_id]

    # --- Favorites ---
    def toggle_favorite(self, location_id):
        if location_id in self.favorites:
            self.favorites.discard(location_id)
            return False
        self.favorites.add(location_id)
        return True

    def is_favorite(self, location_id):
        return location_id in self.favorites

    def get_favorites(self):
        return [l for l in self.locations if l["id"] in self.favorites]

    # --- Tickets ---
    def get_user_tickets(self, tab="upcoming"):
        if tab == "upcoming":
            return [t for t in self.tickets if t.get("status") == "upcoming"]
        return [t for t in self.tickets if t.get("status") == "history"]

    def book_ticket(self, location_id, ticket_type, quantity, total_price, visit_date):
        loc = self.get_location(location_id)
        if not loc:
            return False
        record = {
            "id": self._next_ids["tickets"],
            "location": loc["name"],
            "date": visit_date,
            "time": "10:00 AM",
            "detail": f"{quantity} {ticket_type}",
            "price": total_price,
            "status": "upcoming",
        }
        self._next_ids["tickets"] += 1
        self.tickets.append(record)
        self.ticket_records.append(record)
        return True

    def get_all_bookings(self):
        return self.ticket_records + self.tickets

    def update_booking_status(self, index, status):
        bookings = self.get_all_bookings()
        if 0 <= index < len(bookings):
            bookings[index]["status"] = status
            return True
        return False

    # --- Contact ---
    def save_contact(self, name, email, message):
        cid = self._next_ids["contact"]
        self._next_ids["contact"] += 1
        self.contact_messages.append(
            {
                "id": cid,
                "name": name,
                "email": email,
                "message": message,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        return True

    # --- Admin user CRUD ---
    def delete_user(self, user_id):
        self.users = [u for u in self.users if u["id"] != user_id]

    def update_user(self, user_id, full_name, email):
        for u in self.users:
            if u["id"] == user_id:
                u["full_name"] = full_name
                u["email"] = email
                return True
        return False

    # --- Reports ---
    def get_reports(self):
        total_revenue = sum(t.get("price", 0) for t in self.tickets)
        return {
            "total_users": len(self.users),
            "total_locations": len(self.locations),
            "total_tickets": len(self.tickets),
            "total_revenue": total_revenue,
        }


store = DataStore()
