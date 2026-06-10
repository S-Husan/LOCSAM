"""Theme manager — colors, fonts, and layout constants."""

# Layout
FORM_MAX_WIDTH = 480
CONTENT_MAX_WIDTH = 1100
NAV_MAX_WIDTH = 720
BUTTON_MAX_WIDTH = 400
HERO_HEIGHT = 380

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 26, "bold")
FONT_HEADING = (FONT_FAMILY, 20, "bold")
FONT_SUBHEADING = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 11)
FONT_SMALL = (FONT_FAMILY, 10)
FONT_TINY = (FONT_FAMILY, 9)
FONT_LOGO = (FONT_FAMILY, 40, "bold")

PAD_SM = 8
PAD_MD = 16
PAD_LG = 24
PAD_XL = 32

LIGHT = {
    "PRIMARY": "#6A00FF",
    "PRIMARY_HOVER": "#5A00D9",
    "SECONDARY": "#8E2EFF",
    "BACKGROUND": "#F4F5F9",
    "CARD": "#FFFFFF",
    "SURFACE": "#FFFFFF",
    "INPUT_BG": "#FFFFFF",
    "TEXT": "#1A1A2E",
    "TEXT_LIGHT": "#6B7280",
    "ACCENT": "#FFC107",
    "BORDER": "#E5E7EB",
    "NAV_BG": "#FFFFFF",
    "NAV_ACTIVE": "#6A00FF",
    "NAV_INACTIVE": "#9CA3AF",
    "HEADER_TEXT": "#FFFFFF",
    "HEADER_SUB": "#E0D4FF",
    "DANGER": "#DC3545",
    "SUCCESS": "#28A745",
    "OVERLAY": "#6A00FF",
}

DARK = {
    "PRIMARY": "#8E2EFF",
    "PRIMARY_HOVER": "#A855FF",
    "SECONDARY": "#6A00FF",
    "BACKGROUND": "#0F0F1A",
    "CARD": "#1C1C32",
    "SURFACE": "#16162B",
    "INPUT_BG": "#252545",
    "TEXT": "#F3F4F6",
    "TEXT_LIGHT": "#9CA3AF",
    "ACCENT": "#FFC107",
    "BORDER": "#2E2E4A",
    "NAV_BG": "#16162B",
    "NAV_ACTIVE": "#8E2EFF",
    "NAV_INACTIVE": "#6B7280",
    "HEADER_TEXT": "#FFFFFF",
    "HEADER_SUB": "#C4B5FD",
    "DANGER": "#EF4444",
    "SUCCESS": "#22C55E",
    "OVERLAY": "#1A1035",
}


class ThemeManager:
    def __init__(self, dark_mode=False):
        self.dark_mode = dark_mode

    def toggle(self):
        self.dark_mode = not self.dark_mode
        return self.dark_mode

    def set_dark(self, value: bool):
        self.dark_mode = value

    def palette(self):
        return DARK if self.dark_mode else LIGHT

    def get(self, key):
        return self.palette().get(key, LIGHT.get(key, "#000000"))


theme_manager = ThemeManager()
