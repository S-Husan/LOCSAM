"""Theme manager — light and dark mode colors."""

LIGHT = {
    "PRIMARY": "#6A00FF",
    "SECONDARY": "#8E2EFF",
    "BACKGROUND": "#FFFFFF",
    "CARD": "#F8F8F8",
    "TEXT": "#222222",
    "TEXT_LIGHT": "#666666",
    "ACCENT": "#FFC107",
    "BORDER": "#E0E0E0",
    "WHITE": "#FFFFFF",
    "HEADER_TEXT": "#FFFFFF",
    "HEADER_SUB": "#E0D4FF",
}

DARK = {
    "PRIMARY": "#8E2EFF",
    "SECONDARY": "#6A00FF",
    "BACKGROUND": "#1A1A2E",
    "CARD": "#252540",
    "TEXT": "#F0F0F0",
    "TEXT_LIGHT": "#A0A0B8",
    "ACCENT": "#FFC107",
    "BORDER": "#3A3A55",
    "WHITE": "#2D2D44",
    "HEADER_TEXT": "#FFFFFF",
    "HEADER_SUB": "#C4B5FD",
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
        return self.palette()[key]


theme_manager = ThemeManager()
