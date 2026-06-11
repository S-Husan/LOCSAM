# LOCSAM — MySQL Migration Complete ✓

Your application has been successfully migrated from JSON to MySQL storage. The app is now ready to use database persistence!

## What Changed

### models.py (Fully Rewritten)
The entire `DataStore` class has been converted from JSON-based to MySQL CRUD operations:

#### ✓ All Methods Implemented with SQL
- **Authentication**: `register_user()`, `login_user()`, `login_admin()`
- **Locations**: `get_locations()`, `get_location()`, `add_location()`, `update_location()`, `delete_location()`
- **Gallery**: `get_gallery()` (linked to locations table)
- **Favorites**: `toggle_favorite()`, `is_favorite()`, `get_favorites()`
- **Tickets**: `book_ticket()`, `get_user_tickets()`, `get_all_bookings()`, `update_booking_status()`
- **Contact**: `save_contact()`
- **Admin**: `delete_user()`, `update_user()`, `get_reports()`

#### ✓ Key Features Preserved
- **Same method signatures** → No UI changes needed
- **Dictionary cursors** → Results work like old dictionaries
- **Session-based memory** → `current_user` and `current_admin` stored in memory
- **Auto-initialization** → Default data inserted on first run
- **Graceful error handling** → App runs even if MySQL is unavailable

#### ✓ Gallery Image Handling
- **Main cover image** → Stored in `locations.image`
- **Gallery images** → Stored in `gallery` table (3 per location recommended)
- **Updates** → Old gallery deleted, new images inserted

## What Wasn't Changed (As Required)
✗ Did NOT delete or modify:
- `persistence.py` — Kept as backup
- `data_store/locsam_data.json` — Kept as backup
- `database.py` — Connection module unchanged
- All UI files — No modifications needed
- Image files — All untouched
- Config files — Unchanged

## How to Enable MySQL Persistence

### Step 1: Set Up MySQL (if not already done)

If you haven't set up MySQL yet, follow [DATABASE_SETUP.md](DATABASE_SETUP.md):

```powershell
# 1. Install MySQL or use XAMPP/WAMP
# 2. Create database by running schema.sql:
mysql -u root -p < schema.sql
# 3. Install Python driver:
pip install mysql-connector-python
```

### Step 2: Configure Database Credentials

Set the MySQL connection environment variables:

**Option A: PowerShell (temporary — for current session only)**
```powershell
$env:LOCSAM_DB_HOST = "localhost"
$env:LOCSAM_DB_USER = "root"
$env:LOCSAM_DB_PASSWORD = "your_mysql_password"
$env:LOCSAM_DB_NAME = "locsam_db"
```

**Option B: PowerShell (permanent — persists after restart)**
```powershell
setx LOCSAM_DB_PASSWORD "your_mysql_password"
setx LOCSAM_DB_HOST "localhost"
setx LOCSAM_DB_USER "root"
setx LOCSAM_DB_NAME "locsam_db"
```
Then restart PowerShell.

**Option C: Edit `database.py` directly**
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_mysql_password",  # Set this!
    "database": "locsam_db",
    "charset": "utf8mb4",
    "autocommit": True,
}
```

### Step 3: Verify Connection

Test the connection:
```powershell
cd "c:\SIUT\INTERNSHIP 2\Application_Demo"
python -c "from database import test_connection; print(test_connection())"
```

You should see:
```
(True, 'Connected to MySQL successfully.')
```

### Step 4: Run the App

```powershell
python main.py
```

The app will:
1. Connect to MySQL
2. Initialize default data if database is empty
3. Save all new data to MySQL instead of JSON

## MySQL Tables Used

| Table | Purpose |
|-------|---------|
| `users` | User accounts for registration/login |
| `admins` | Admin accounts |
| `locations` | Tourist locations with main cover image |
| `gallery` | Gallery images (3+ per location, linked to locations) |
| `tickets` | Ticket bookings (linked to users/locations) |
| `favorites` | User favorites (linked to users/locations) |
| `contact_messages` | Contact form submissions |
| `user_settings` | Optional user preferences |
| `reviews` | Optional location reviews |

## Default Accounts (Created by schema.sql)

| Role | Username / Email | Password |
|------|------------------|----------|
| Admin | `admin` | `admin123` |
| Demo User | `azizbek@example.com` | `password123` |

## What Happens When App Runs

### When MySQL is Available ✓
1. Models connect to database
2. All data reads from/writes to MySQL tables
3. New registrations, locations, tickets save to database
4. Admin can manage data in database

### When MySQL is Unavailable ⚠
1. App starts with warning message
2. All operations return empty lists
3. No data can be saved
4. Set environment variables and restart to enable persistence

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Access denied for user 'root'@'localhost'` | Set `LOCSAM_DB_PASSWORD` environment variable |
| `Can't connect to MySQL server` | Start MySQL service / Check host:port |
| `Unknown database locsam_db` | Run `mysql -u root -p < schema.sql` |
| Data not saving | Check that `store._db_available = True` |

## Testing Checklist

After enabling MySQL, test these features:

- [ ] Register a new user → Check `users` table
- [ ] Login with registered user → Check session restored
- [ ] Add a location (admin) → Check `locations` and `gallery` tables
- [ ] Add gallery images → Check `gallery` table (3 images)
- [ ] Update location → Old gallery deleted, new images inserted
- [ ] Toggle favorite → Check `favorites` table
- [ ] Book ticket → Check `tickets` table
- [ ] Submit contact form → Check `contact_messages` table
- [ ] View admin reports → Should count from database
- [ ] Check "Remember Me" → Should restore session from database

## Important Notes

### Session Memory
`current_user` and `current_admin` are kept in memory during the app session. They are:
- Set by `login_user()` and `login_admin()`
- Restored on app startup if "Remember Me" was checked
- Cleared by `logout_user()` and `logout_admin()`
- NOT stored in the database

### JSON Backup
The original JSON file (`data_store/locsam_data.json`) is kept as a backup. If you need to switch back to JSON temporarily, the old `models.py` code is in your git history.

### Image Files
Gallery images are referenced by filename keys (e.g., `"registan_1"`, `"shah_i_zinda_2"`). The actual image files in the `Images/` folder are not affected by the migration.

## Next Steps

1. **Set MySQL credentials** using one of the options above
2. **Test the connection** with `test_connection()`
3. **Run the app** with `python main.py`
4. **Test each feature** to verify data saves to MySQL
5. **Check the database** to confirm data is being stored

---

**Migration Date**: 2025-06-11  
**Status**: ✓ Complete and Ready  
**Backup**: JSON file preserved at `data_store/locsam_data.json`
