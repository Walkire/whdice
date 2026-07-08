"""Shared styling constants for consistent look across the application.

Requirements: 1.5
"""

# --- Fonts ---
FONT_TITLE = ("", 18, "bold")        # Page titles
FONT_SECTION = ("", 14, "bold")      # Section headers
FONT_BODY = ("", 13)                 # Normal text
FONT_SMALL = ("", 11)               # Secondary / muted text
FONT_SIDEBAR_TITLE = ("", 16, "bold")

# --- Spacing ---
PAGE_PAD_X = 16                      # Horizontal padding for page content
PAGE_PAD_Y_TOP = 16                  # Top padding for page title
PAGE_PAD_Y_BOTTOM = 16              # Bottom padding for page content
SECTION_GAP = 12                     # Gap between sections
WIDGET_PAD_X = 4                     # Internal widget horizontal padding
WIDGET_PAD_Y = 2                     # Internal widget vertical padding
CARD_PAD_Y = 6                       # Vertical gap between cards

# --- Sizes ---
BUTTON_HEIGHT = 36                   # Standard button height
BUTTON_HEIGHT_SMALL = 28             # Small/action button height
SIDEBAR_WIDTH = 160                  # Fixed sidebar width
NAV_BUTTON_HEIGHT = 36               # Sidebar navigation button height
CORNER_RADIUS = 8                    # Default corner radius for cards/panels

# --- Colors (tuples: light mode, dark mode) ---
COLOR_ACCENT = ("#1f6aa5", "#1f6aa5")
COLOR_ACCENT_HOVER = ("#185a8c", "#2980b9")
COLOR_DANGER = ("#b33333", "#b33333")
COLOR_DANGER_HOVER = ("#d44444", "#d44444")
COLOR_MUTED_TEXT = ("gray50", "gray60")
COLOR_BORDER = ("gray70", "gray30")
COLOR_NAV_ACTIVE = ("gray75", "gray30")
COLOR_NAV_HOVER = ("gray75", "gray30")
COLOR_ABILITY_ACTIVE_BG = ("dodgerblue", "dodgerblue4")
COLOR_ABILITY_ACTIVE_BORDER = ("dodgerblue", "dodgerblue4")
COLOR_ABILITY_INACTIVE_BORDER = ("gray60", "gray40")
