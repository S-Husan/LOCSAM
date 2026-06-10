# LOCSAM — MySQL Database Setup

This guide connects LOCSAM to MySQL. The app **currently saves data locally** in `data_store/locsam_data.json`. Use this when you want a real database backend.

---

## Step 1: Install MySQL

1. Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql/) or use XAMPP/WAMP.
2. During setup, set a **root password** and remember it.
3. Start the MySQL service.

---

## Step 2: Create the database

### Option A — MySQL Workbench

1. Open MySQL Workbench → connect to `localhost`.
2. **File → Open SQL Script** → select `schema.sql` in this folder.
3. Click **Execute** (lightning icon).

### Option B — Command line

```powershell
cd "c:\SIUT\INTERNSHIP 2\Application_Demo"
mysql -u root -p < schema.sql
```

Enter your MySQL root password when prompted.

---

## Step 3: Install Python MySQL driver

```powershell
python -m pip install mysql-connector-python
```

---

## Step 4: Configure connection

Edit `database.py` or set environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOCSAM_DB_HOST` | `localhost` | MySQL host |
| `LOCSAM_DB_PORT` | `3306` | Port |
| `LOCSAM_DB_USER` | `root` | Username |
| `LOCSAM_DB_PASSWORD` | *(empty)* | Password |
| `LOCSAM_DB_NAME` | `locsam_db` | Database name |

**PowerShell example:**

```powershell
$env:LOCSAM_DB_PASSWORD = "your_mysql_password"
python -c "from database import test_connection; print(test_connection())"
```

You should see: `(True, 'Connected to MySQL successfully.')`

---

## Step 5: Default accounts (after schema.sql)

| Role | Username / Email | Password |
|------|------------------|----------|
| Admin | `admin` | `admin123` |
| Demo user | `azizbek@example.com` | `password123` |

---

## Step 6: Switch app from JSON to MySQL

Today, `models.py` uses JSON via `persistence.py`. To use MySQL:

1. Implement CRUD in `models.py` using `database.connect()` and SQL queries.
2. Map tables: `users`, `locations`, `gallery`, `tickets`, `favorites`, `contact_messages`.
3. Keep the same method names (`register_user`, `get_locations`, etc.) so the UI does not change.

Until that migration is done, **all user data is stored in:**

```
Application_Demo/data_store/locsam_data.json
```

This file persists registrations, logins (Remember Me), favorites, tickets, locations added in admin, and language/dark mode settings.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `Access denied for user` | Wrong password in `database.py` or env vars |
| `Can't connect to MySQL server` | Start MySQL service; check host/port |
| `Unknown database locsam_db` | Run `schema.sql` again |
| `mysql not recognized` | Use full path to `mysql.exe` or MySQL Workbench |

---

## Security note

For production, **never store plain-text passwords**. Use hashing (e.g. `bcrypt`) in `users` and `admins` tables.
