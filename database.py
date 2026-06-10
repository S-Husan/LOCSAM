"""MySQL connection helper for LOCSAM.

The app currently uses JSON persistence (models.py + persistence.py).
When you are ready for MySQL, follow DATABASE_SETUP.md and switch models to use this module.
"""

import os

# Default connection settings — edit or use environment variables
DB_CONFIG = {
    "host": os.getenv("LOCSAM_DB_HOST", "localhost"),
    "port": int(os.getenv("LOCSAM_DB_PORT", "3306")),
    "user": os.getenv("LOCSAM_DB_USER", "root"),
    "password": os.getenv("LOCSAM_DB_PASSWORD", ""),
    "database": os.getenv("LOCSAM_DB_NAME", "locsam_db"),
    "charset": "utf8mb4",
    "autocommit": True,
}


def connect():
    """Return a MySQL connection using mysql-connector-python."""
    try:
        import mysql.connector
        from mysql.connector import Error
    except ImportError:
        raise ImportError(
            "Install mysql-connector-python: python -m pip install mysql-connector-python"
        )

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error as e:
        raise ConnectionError(f"MySQL connection failed: {e}") from e

    raise ConnectionError("Could not connect to MySQL.")


def test_connection():
    """Test database connectivity. Returns (success, message)."""
    try:
        conn = connect()
        conn.close()
        return True, "Connected to MySQL successfully."
    except Exception as e:
        return False, str(e)
