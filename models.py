"""Data store with JSON persistence (MySQL-ready structure)."""

from datetime import datetime

from config import ADMIN_PASSWORD, ADMIN_USERNAME, DEMO_USER
from data import LOCATIONS, SAMPLE_TICKETS_UPCOMING
from persistence import load_data, save_data
from theme import theme_manager


class DataStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        saved = load_data()
        if saved:
            self._load_from_dict(saved)
        else:
            self._init_defaults()
            self.save()

        theme_manager.set_dark(self.settings.get("dark_mode", False))
        self._restore_session()

    def _init_defaults(self):
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
        self.gallery = self._build_default_gallery()
        self.tickets = []
        for t in SAMPLE_TICKETS_UPCOMING:
            self.tickets.append({**t, "user_id": 1})
        self.ticket_records = []
        self.favorites = []
        self.reviews = []
        self.contact_messages = []
        self.current_user = None
        self.current_admin = None
        self.settings = {
            "language": "en",
            "dark_mode": False,
            "remembered_user_id": None,
        }
        self._next_ids = {
            "users": 2,
            "locations": 7,
            "tickets": 4,
            "contact": 1,
            "gallery": 19,
        }

    def _build_default_gallery(self):
        gallery = []
        gid = 1
        for loc in LOCATIONS:
            for i in range(1, 4):
                gallery.append(
                    {"id": gid, "location_id": loc["id"], "image_path": f"{loc['image']}_{i}"}
                )
                gid += 1
        return gallery

    def _load_from_dict(self, data):
        self.users = data.get("users", [])
        self.admins = data.get("admins", [])
        self.locations = data.get("locations", [])
        self.gallery = data.get("gallery", [])
        self.tickets = data.get("tickets", [])
        self.ticket_records = data.get("ticket_records", [])
        self.favorites = data.get("favorites", [])
        self.reviews = data.get("reviews", [])
        self.contact_messages = data.get("contact_messages", [])
        self.settings = data.get(
            "settings",
            {"language": "en", "dark_mode": False, "remembered_user_id": None},
        )
        self._next_ids = data.get(
            "_next_ids",
            {"users": 2, "locations": 7, "tickets": 4, "contact": 1, "gallery": 19},
        )
        self.current_user = None
        self.current_admin = None

    def save(self):
        data = {
            "users": self.users,
            "admins": self.admins,
            "locations": self.locations,
            "gallery": self.gallery,
            "tickets": self.tickets,
            "ticket_records": self.ticket_records,
            "favorites": self.favorites,
            "reviews": self.reviews,
            "contact_messages": self.contact_messages,
            "settings": self.settings,
            "_next_ids": self._next_ids,
        }
        save_data(data)

    def _restore_session(self):
        uid = self.settings.get("remembered_user_id")
        if uid:
            for u in self.users:
                if u["id"] == uid:
                    self.current_user = u
                    break

    def set_language(self, lang):
        self.settings["language"] = lang
        self.save()

    def set_dark_mode(self, enabled):
        self.settings["dark_mode"] = enabled
        theme_manager.set_dark(enabled)
        self.save()

    def set_remember_user(self, user_id):
        self.settings["remembered_user_id"] = user_id
        self.save()

    def clear_remember_user(self):
        self.settings["remembered_user_id"] = None
        self.save()

    # --- Auth ---
    def register_user(self, full_name, email, password):
        if any(u["email"].lower() == email.lower() for u in self.users):
            return False, "Email already registered."
        uid = self._next_ids["users"]
        self._next_ids["users"] += 1
        user = {
            "id": uid,
            "full_name": full_name,
            "email": email,
            "password": password,
            "created_at": datetime.now().strftime("%Y-%m-%d"),
        }
        self.users.append(user)
        self.current_user = user
        self.set_remember_user(uid)
        self.save()
        return True, "Registration successful."

    def login_user(self, email, password, remember=True):
        for u in self.users:
            if u["email"].lower() == email.lower() and u["password"] == password:
                self.current_user = u
                if remember:
                    self.set_remember_user(u["id"])
                self.save()
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
        self.clear_remember_user()

    def logout_admin(self):
        self.current_admin = None

    def get_user_id(self):
        return self.current_user["id"] if self.current_user else None

    # --- Locations ---
    def get_locations(self, category="All", search=""):
        results = list(self.locations)
        if category and category != "All":
            if category == "Popular":
                results = sorted(results, key=lambda x: x["rating"], reverse=True)
            else:
                results = [l for l in results if l["category"] == category]
        q = (search or "").strip().lower()
        if q:
            filtered = []
            for loc in results:
                haystack = " ".join(
                    [
                        str(loc.get("name", "")),
                        str(loc.get("category", "")),
                        str(loc.get("city", "")),
                        str(loc.get("description", "")),
                        str(loc.get("rating", "")),
                    ]
                ).lower()
                if q in haystack:
                    filtered.append(loc)
            results = filtered
        return results

    def get_location(self, location_id):
        for loc in self.locations:
            if loc["id"] == location_id:
                return loc
        return None

    def get_gallery(self, location_id):
        return [g for g in self.gallery if g["location_id"] == location_id]

    def add_location(self, data, gallery_image_keys=None):
        lid = self._next_ids["locations"]
        self._next_ids["locations"] += 1
        data["id"] = lid
        self.locations.append(data)

        if gallery_image_keys:
            for i, key in enumerate(gallery_image_keys[:3], start=1):
                gid = self._next_ids["gallery"]
                self._next_ids["gallery"] += 1
                self.gallery.append(
                    {"id": gid, "location_id": lid, "image_path": f"{key}_{i}"}
                )
        else:
            base = data.get("image", f"loc_{lid}")
            for i in range(1, 4):
                gid = self._next_ids["gallery"]
                self._next_ids["gallery"] += 1
                self.gallery.append(
                    {"id": gid, "location_id": lid, "image_path": f"{base}_{i}"}
                )

        self.save()
        return lid

    def update_location(self, location_id, data, gallery_image_keys=None):
        for i, loc in enumerate(self.locations):
            if loc["id"] == location_id:
                self.locations[i] = {**loc, **data, "id": location_id}
                if gallery_image_keys:
                    self.gallery = [g for g in self.gallery if g["location_id"] != location_id]
                    for idx, key in enumerate(gallery_image_keys[:3], start=1):
                        gid = self._next_ids["gallery"]
                        self._next_ids["gallery"] += 1
                        self.gallery.append(
                            {"id": gid, "location_id": location_id, "image_path": f"{key}_{idx}"}
                        )
                self.save()
                return True
        return False

    def delete_location(self, location_id):
        self.locations = [l for l in self.locations if l["id"] != location_id]
        self.gallery = [g for g in self.gallery if g["location_id"] != location_id]
        self.favorites = [f for f in self.favorites if f.get("location_id") != location_id]
        self.save()

    # --- Favorites (per user) ---
    def toggle_favorite(self, location_id):
        uid = self.get_user_id()
        if not uid:
            return False
        existing = next(
            (f for f in self.favorites if f["user_id"] == uid and f["location_id"] == location_id),
            None,
        )
        if existing:
            self.favorites = [
                f
                for f in self.favorites
                if not (f["user_id"] == uid and f["location_id"] == location_id)
            ]
            self.save()
            return False
        self.favorites.append({"user_id": uid, "location_id": location_id})
        self.save()
        return True

    def is_favorite(self, location_id):
        uid = self.get_user_id()
        if not uid:
            return False
        return any(
            f["user_id"] == uid and f["location_id"] == location_id for f in self.favorites
        )

    def get_favorites(self):
        uid = self.get_user_id()
        if not uid:
            return []
        fav_ids = {f["location_id"] for f in self.favorites if f["user_id"] == uid}
        return [l for l in self.locations if l["id"] in fav_ids]

    # --- Tickets (per user) ---
    def get_user_tickets(self, tab="upcoming"):
        uid = self.get_user_id()
        if not uid:
            return []
        user_tickets = [t for t in self.tickets if t.get("user_id") == uid]
        if tab == "upcoming":
            return [t for t in user_tickets if t.get("status") == "upcoming"]
        return [t for t in user_tickets if t.get("status") != "upcoming"]

    def book_ticket(self, location_id, ticket_type, quantity, total_price, visit_date):
        loc = self.get_location(location_id)
        uid = self.get_user_id()
        if not loc or not uid:
            return False
        record = {
            "id": self._next_ids["tickets"],
            "user_id": uid,
            "location_id": location_id,
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
        self.save()
        return True

    def get_all_bookings(self):
        return list(self.tickets)

    def update_booking_status(self, ticket_id, status):
        for t in self.tickets:
            if t.get("id") == ticket_id:
                t["status"] = status
                self.save()
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
        self.save()
        return True

    # --- Admin user CRUD ---
    def delete_user(self, user_id):
        self.users = [u for u in self.users if u["id"] != user_id]
        self.favorites = [f for f in self.favorites if f.get("user_id") != user_id]
        self.tickets = [t for t in self.tickets if t.get("user_id") != user_id]
        if self.current_user and self.current_user["id"] == user_id:
            self.current_user = None
        self.save()

    def update_user(self, user_id, full_name, email):
        for u in self.users:
            if u["id"] == user_id:
                u["full_name"] = full_name
                u["email"] = email
                if self.current_user and self.current_user["id"] == user_id:
                    self.current_user = u
                self.save()
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
