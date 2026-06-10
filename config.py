"""LOCSAM application configuration."""

# Default admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# Default demo user profile
DEMO_USER = {
    "full_name": "Azizbek Abdurahmonov",
    "email": "azizbek@example.com",
}

# Optional full-window background image.
# Put your image in assets/background.jpg and set BACKGROUND_IMAGE_PATH to that path.
# Example: BACKGROUND_IMAGE_PATH = "assets/background.jpg"
# Leave as None to use the normal theme background color.
BACKGROUND_IMAGE_PATH = None

# Desktop layout defaults
APP_WIDTH = 1200
APP_HEIGHT = 800
MIN_WIDTH = 900
MIN_HEIGHT = 650
CARD_RADIUS = 12

# Legacy color aliases (theme.py is preferred at runtime)
PRIMARY = "#6A00FF"
SECONDARY = "#8E2EFF"
BACKGROUND = "#FFFFFF"
CARD = "#F8F8F8"
TEXT = "#222222"
TEXT_LIGHT = "#666666"
ACCENT = "#FFC107"
BORDER = "#E0E0E0"
SUCCESS = "#28A745"
DANGER = "#DC3545"
WHITE = "#FFFFFF"
