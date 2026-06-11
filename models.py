"""Data store with MySQL persistence."""

from datetime import datetime
import mysql.connector
from mysql.connector import Error
from config import ADMIN_PASSWORD, ADMIN_USERNAME, DEMO_USER
from data import LOCATIONS, SAMPLE_TICKETS_UPCOMING
from database import DB_CONFIG
from theme import theme_manager


class DataStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        """Initialize the data store and set up session-specific variables."""
        self.current_user = None
        self.current_admin = None
        self.settings = {
            "language": "en",
            "dark_mode": False,
            "remembered_user_id": None,
        }
        self._db_available = False
        
        # Check if database is available
        try:
            test_conn = self._get_connection()
            test_conn.close()
            self._db_available = True
            self._init_defaults_if_needed()
        except Exception as e:
            print(f"⚠ MySQL database unavailable: {e}")
            print("ℹ Set LOCSAM_DB_PASSWORD and start MySQL to enable database persistence.")
            self._db_available = False
        
        theme_manager.set_dark(self.settings.get("dark_mode", False))
        self._restore_session()

    def _get_connection(self):
        """Get a MySQL connection with dictionary cursor."""
        try:
            import mysql.connector
            from mysql.connector import Error
        except ImportError:
            raise ImportError(
                "Install mysql-connector-python: python -m pip install mysql-connector-python"
            )
        
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            return conn
        except Error as e:
            raise ConnectionError(f"MySQL connection failed: {e}") from e

    def _init_defaults_if_needed(self):
        """Initialize default data if database is empty."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Check if users table has any data
            cursor.execute("SELECT COUNT(*) as cnt FROM users")
            result = cursor.fetchone()
            user_count = result["cnt"] if result else 0
            
            cursor.execute("SELECT COUNT(*) as cnt FROM admins")
            result = cursor.fetchone()
            admin_count = result["cnt"] if result else 0
            
            cursor.execute("SELECT COUNT(*) as cnt FROM locations")
            result = cursor.fetchone()
            location_count = result["cnt"] if result else 0
            
            cursor.close()
            conn.close()
            
            # Only initialize if all tables are empty
            if user_count == 0 and admin_count == 0 and location_count == 0:
                self._insert_default_data()
        except ConnectionError as e:
            print(f"MySQL not available: {e}")
            print("Set LOCSAM_DB_PASSWORD environment variable and start MySQL to enable database persistence.")
        except Exception as e:
            print(f"Warning during default data check: {e}")

    def _insert_default_data(self):
        """Insert default demo data into the database."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert default admin
            try:
                cursor.execute(
                    "INSERT INTO admins (username, password) VALUES (%s, %s)",
                    (ADMIN_USERNAME, ADMIN_PASSWORD)
                )
            except:
                pass  # Admin might already exist
            
            # Insert demo user
            try:
                cursor.execute(
                    "INSERT INTO users (full_name, email, password, created_at) VALUES (%s, %s, %s, %s)",
                    (DEMO_USER["full_name"], DEMO_USER["email"], "password123", datetime.now().strftime("%Y-%m-%d"))
                )
            except:
                pass  # Demo user might already exist
            
            # Insert locations and gallery
            for loc in LOCATIONS:
                try:
                    cursor.execute(
                        """INSERT INTO locations 
                           (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (
                            loc["name"], loc["category"], loc.get("city", "Samarkand, Uzbekistan"),
                            loc["description"], loc["rating"], loc["reviews"], loc["price"],
                            loc.get("open_time", "06:00 AM - 09:00 PM"),
                            loc["latitude"], loc["longitude"], loc["image"]
                        )
                    )
                    location_id = cursor.lastrowid
                    
                    # Insert gallery images for this location
                    base = loc.get("image", f"loc_{location_id}")
                    for i in range(1, 4):
                        cursor.execute(
                            "INSERT INTO gallery (location_id, image_path, sort_order) VALUES (%s, %s, %s)",
                            (location_id, f"{base}_{i}", i)
                        )
                except:
                    pass  # Location might already exist
            
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error initializing default data: {e}")

    def _restore_session(self):
        """Restore the current user session if remembered."""
        if not self._db_available:
            return
        uid = self.settings.get("remembered_user_id")
        if uid:
            try:
                conn = self._get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users WHERE id = %s", (uid,))
                self.current_user = cursor.fetchone()
                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Could not restore session: {e}")

    def set_language(self, lang):
        """Set the application language."""
        self.settings["language"] = lang

    def set_dark_mode(self, enabled):
        """Set dark mode for the theme."""
        self.settings["dark_mode"] = enabled
        theme_manager.set_dark(enabled)

    def set_remember_user(self, user_id):
        """Remember a user ID for next session."""
        self.settings["remembered_user_id"] = user_id

    def clear_remember_user(self):
        """Clear the remembered user ID."""
        self.settings["remembered_user_id"] = None

    # --- Auth ---
    def register_user(self, full_name, email, password):
        """Register a new user."""
        if not self._db_available:
            return False, "Database is not available."
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Check if email already exists
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                cursor.close()
                conn.close()
                return False, "Email already registered."
            
            # Insert new user
            cursor.execute(
                "INSERT INTO users (full_name, email, password, created_at) VALUES (%s, %s, %s, %s)",
                (full_name, email, password, datetime.now().strftime("%Y-%m-%d"))
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            # Fetch the new user
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            self.current_user = cursor.fetchone()
            self.set_remember_user(user_id)
            
            cursor.close()
            conn.close()
            return True, "Registration successful."
        except Exception as e:
            return False, f"Registration failed: {e}"

    def login_user(self, email, password, remember=True):
        """Login a user with email and password."""
        if not self._db_available:
            return False, "Database is not available."
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM users WHERE email = %s AND password = %s",
                (email, password)
            )
            user = cursor.fetchone()
            
            if user:
                self.current_user = user
                if remember:
                    self.set_remember_user(user["id"])
                cursor.close()
                conn.close()
                return True, "Welcome back!"
            else:
                cursor.close()
                conn.close()
                return False, "Invalid email or password."
        except Exception as e:
            return False, f"Login failed: {e}"

    def login_admin(self, username, password):
        """Login an admin with username and password."""
        if not self._db_available:
            return False, "Database is not available."
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM admins WHERE username = %s AND password = %s",
                (username, password)
            )
            admin = cursor.fetchone()
            
            if admin:
                self.current_admin = admin
                cursor.close()
                conn.close()
                return True, "Admin login successful."
            else:
                cursor.close()
                conn.close()
                return False, "Invalid admin credentials."
        except Exception as e:
            return False, f"Admin login failed: {e}"

    def logout_user(self):
        """Logout the current user."""
        self.current_user = None
        self.clear_remember_user()

    def logout_admin(self):
        """Logout the current admin."""
        self.current_admin = None

    def get_user_id(self):
        """Get the current user's ID."""
        return self.current_user["id"] if self.current_user else None

    # --- Users (admin view) ---
    def get_users(self):
        """Get all users (admin view)."""
        if not self._db_available:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users ORDER BY id DESC")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return users if users else []
        except Exception as e:
            print(f"Error getting users: {e}")
            return []

    # --- Locations ---
    def get_locations(self, category="All", search=""):
        """Get all locations with optional filtering."""
        if not self._db_available:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM locations"
            params = []
            
            if category and category != "All":
                if category != "Popular":
                    query += " WHERE category = %s"
                    params.append(category)
                else:
                    # For Popular, we'll sort after fetching
                    pass
            
            q = (search or "").strip().lower()
            if q:
                if category and category != "All" and category != "Popular":
                    query += " AND (name LIKE %s OR category LIKE %s OR city LIKE %s OR description LIKE %s OR rating LIKE %s)"
                else:
                    query += " WHERE (name LIKE %s OR category LIKE %s OR city LIKE %s OR description LIKE %s OR rating LIKE %s)"
                search_param = f"%{q}%"
                params.extend([search_param] * 5)
            
            if category == "Popular":
                query += " ORDER BY rating DESC"
            
            cursor.execute(query, params)
            locations = cursor.fetchall()
            cursor.close()
            conn.close()
            return locations if locations else []
        except Exception as e:
            print(f"Error getting locations: {e}")
            return []

    def get_location(self, location_id):
        """Get a single location by ID."""
        if not self._db_available:
            return None
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM locations WHERE id = %s", (location_id,))
            location = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return location
        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    def get_gallery(self, location_id):
        """Get gallery images for a location."""
        if not self._db_available:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT * FROM gallery WHERE location_id = %s ORDER BY sort_order",
                (location_id,)
            )
            gallery = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return gallery if gallery else []
        except Exception as e:
            print(f"Error getting gallery: {e}")
            return []

    def add_location(self, data, gallery_image_keys=None):
        """Add a new location with gallery images."""
        if not self._db_available:
            return None
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Insert location with main cover image
            image_key = data.get("image", "location_image")
            cursor.execute(
                """INSERT INTO locations 
                   (name, category, city, description, rating, reviews, price, open_time, latitude, longitude, image)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    data.get("name"), data.get("category", "Monument"),
                    data.get("city", "Samarkand, Uzbekistan"),
                    data.get("description"), data.get("rating", 4.0),
                    data.get("reviews", 0), data.get("price", 0),
                    data.get("open_time", "06:00 AM - 09:00 PM"),
                    data.get("latitude"), data.get("longitude"),
                    image_key
                )
            )
            location_id = cursor.lastrowid
            
            # Insert gallery images
            if gallery_image_keys:
                for i, image_path in enumerate(gallery_image_keys[:3], 1):
                    cursor.execute(
                        "INSERT INTO gallery (location_id, image_path, sort_order) VALUES (%s, %s, %s)",
                        (location_id, image_path, i)
                    )
            
            conn.commit()
            cursor.close()
            conn.close()
            return location_id
        except Exception as e:
            print(f"Error adding location: {e}")
            return None

    def update_location(self, location_id, data, gallery_image_keys=None):
        """Update a location and optionally update its gallery images."""
        if not self._db_available:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Build update query for location
            update_fields = []
            values = []
            for k, v in data.items():
                if k != "id":
                    update_fields.append(f"{k} = %s")
                    values.append(v)
            
            if update_fields:
                values.append(location_id)
                query = f"UPDATE locations SET {', '.join(update_fields)} WHERE id = %s"
                cursor.execute(query, values)
            
            # Update gallery if image keys are provided
            if gallery_image_keys is not None:
                # Delete old gallery images for this location
                cursor.execute("DELETE FROM gallery WHERE location_id = %s", (location_id,))
                
                # Insert new gallery images
                for i, image_path in enumerate(gallery_image_keys[:3], 1):
                    cursor.execute(
                        "INSERT INTO gallery (location_id, image_path, sort_order) VALUES (%s, %s, %s)",
                        (location_id, image_path, i)
                    )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating location: {e}")
            return False

    def delete_location(self, location_id):
        """Delete a location (cascade deletes gallery and favorites)."""
        if not self._db_available:
            return
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM locations WHERE id = %s", (location_id,))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error deleting location: {e}")

    # --- Favorites (per user) ---
    def toggle_favorite(self, location_id):
        """Toggle favorite status for a location."""
        if not self._db_available:
            return False
        
        uid = self.get_user_id()
        if not uid:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if already favorited
            cursor.execute(
                "SELECT id FROM favorites WHERE user_id = %s AND location_id = %s",
                (uid, location_id)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Remove favorite
                cursor.execute(
                    "DELETE FROM favorites WHERE user_id = %s AND location_id = %s",
                    (uid, location_id)
                )
                conn.commit()
                cursor.close()
                conn.close()
                return False
            else:
                # Add favorite
                cursor.execute(
                    "INSERT INTO favorites (user_id, location_id) VALUES (%s, %s)",
                    (uid, location_id)
                )
                conn.commit()
                cursor.close()
                conn.close()
                return True
        except Exception as e:
            print(f"Error toggling favorite: {e}")
            return False

    def is_favorite(self, location_id):
        """Check if a location is favorited by current user."""
        if not self._db_available:
            return False
        
        uid = self.get_user_id()
        if not uid:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "SELECT id FROM favorites WHERE user_id = %s AND location_id = %s",
                (uid, location_id)
            )
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            return result is not None
        except Exception as e:
            print(f"Error checking favorite: {e}")
            return False

    def get_favorites(self):
        """Get all favorite locations for current user."""
        if not self._db_available:
            return []
        
        uid = self.get_user_id()
        if not uid:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                """SELECT l.* FROM locations l
                   INNER JOIN favorites f ON l.id = f.location_id
                   WHERE f.user_id = %s""",
                (uid,)
            )
            favorites = cursor.fetchall()
            cursor.close()
            conn.close()
            return favorites if favorites else []
        except Exception as e:
            print(f"Error getting favorites: {e}")
            return []

    # --- Tickets (per user) ---
    def get_user_tickets(self, tab="upcoming"):
        """Get user's tickets, filtered by status."""
        if not self._db_available:
            return []
        
        uid = self.get_user_id()
        if not uid:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            if tab == "upcoming":
                cursor.execute(
                    "SELECT * FROM tickets WHERE user_id = %s AND status = 'upcoming' ORDER BY id DESC",
                    (uid,)
                )
            else:
                cursor.execute(
                    "SELECT * FROM tickets WHERE user_id = %s AND status != 'upcoming' ORDER BY id DESC",
                    (uid,)
                )
            
            tickets = cursor.fetchall()
            cursor.close()
            conn.close()
            return tickets if tickets else []
        except Exception as e:
            print(f"Error getting user tickets: {e}")
            return []

    def book_ticket(self, location_id, ticket_type, quantity, total_price, visit_date):
        """Book a ticket for a location."""
        if not self._db_available:
            return False
        
        loc = self.get_location(location_id)
        uid = self.get_user_id()
        if not loc or not uid:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO tickets 
                   (user_id, location_id, ticket_type, quantity, total_price, visit_date, visit_time, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (uid, location_id, ticket_type, quantity, total_price, visit_date, "10:00 AM", "upcoming")
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error booking ticket: {e}")
            return False

    def get_all_bookings(self):
        """Get all ticket bookings (admin view)."""
        if not self._db_available:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
            tickets = cursor.fetchall()
            cursor.close()
            conn.close()
            return tickets if tickets else []
        except Exception as e:
            print(f"Error getting all bookings: {e}")
            return []

    def update_booking_status(self, ticket_id, status):
        """Update the status of a ticket booking."""
        if not self._db_available:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE tickets SET status = %s WHERE id = %s",
                (status, ticket_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating booking status: {e}")
            return False

    # --- Contact ---
    def save_contact(self, name, email, message):
        """Save a contact message."""
        if not self._db_available:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving contact: {e}")
            return False

    def get_contact_messages(self):
        """Get all contact messages (admin view)."""
        if not self._db_available:
            return []
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM contact_messages ORDER BY id DESC")
            messages = cursor.fetchall()
            cursor.close()
            conn.close()
            return messages if messages else []
        except Exception as e:
            print(f"Error getting contact messages: {e}")
            return []

    # --- Admin user CRUD ---
    def delete_user(self, user_id):
        """Delete a user (cascades to favorites and tickets)."""
        if not self._db_available:
            return
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            
            if self.current_user and self.current_user["id"] == user_id:
                self.current_user = None
        except Exception as e:
            print(f"Error deleting user: {e}")

    def update_user(self, user_id, full_name, email):
        """Update user details."""
        if not self._db_available:
            return False
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                "UPDATE users SET full_name = %s, email = %s WHERE id = %s",
                (full_name, email, user_id)
            )
            conn.commit()
            
            # Update current user if it's the same user
            if self.current_user and self.current_user["id"] == user_id:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                self.current_user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return False

    # --- Reports ---
    def get_reports(self):
        """Get admin reports with statistics."""
        if not self._db_available:
            return {
                "total_users": 0,
                "total_locations": 0,
                "total_tickets": 0,
                "total_revenue": 0,
            }
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Count users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()["count"]
            
            # Count locations
            cursor.execute("SELECT COUNT(*) as count FROM locations")
            total_locations = cursor.fetchone()["count"]
            
            # Count tickets
            cursor.execute("SELECT COUNT(*) as count FROM tickets")
            total_tickets = cursor.fetchone()["count"]
            
            # Sum revenue
            cursor.execute("SELECT COALESCE(SUM(total_price), 0) as total FROM tickets")
            total_revenue = cursor.fetchone()["total"]
            
            cursor.close()
            conn.close()
            
            return {
                "total_users": total_users,
                "total_locations": total_locations,
                "total_tickets": total_tickets,
                "total_revenue": float(total_revenue),
            }
        except Exception as e:
            print(f"Error getting reports: {e}")
            return {
                "total_users": 0,
                "total_locations": 0,
                "total_tickets": 0,
                "total_revenue": 0,
            }


store = DataStore()
