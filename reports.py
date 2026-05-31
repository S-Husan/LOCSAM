"""Admin reports module."""

from models import store


def get_report_data():
    """Return dashboard statistics."""
    return store.get_reports()
