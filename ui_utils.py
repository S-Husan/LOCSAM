"""Shared UI helpers and styled widgets for LOCSAM."""

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk

from config import (
    ACCENT,
    BACKGROUND,
    BORDER,
    CARD,
    DANGER,
    PRIMARY,
    SECONDARY,
    TEXT,
    TEXT_LIGHT,
    WHITE,
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
_image_cache = {}


def ensure_assets():
    """Generate placeholder images if assets folder is empty."""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    colors = {
        "registan": ("#1E3A8A", "#F59E0B"),
        "shah_i_zinda": ("#0D9488", "#5EEAD4"),
        "bibi_khanym": ("#7C3AED", "#C4B5FD"),
        "amir_temur": ("#B45309", "#FCD34D"),
        "ulughbek": ("#1D4ED8", "#93C5FD"),
        "tillya_kori": ("#CA8A04", "#FEF08A"),
        "splash_bg": ("#4C1D95", "#6A00FF"),
        "map": ("#E8F4EA", "#34A853"),
    }
    labels = {
        "registan": "Registan",
        "shah_i_zinda": "Shah-i-Zinda",
        "bibi_khanym": "Bibi-Khanym",
        "amir_temur": "Amir Temur",
        "ulughbek": "Ulughbek",
        "tillya_kori": "Tillya-Kori",
        "splash_bg": "Samarkand",
        "map": "Map View",
    }
    for key, (c1, c2) in colors.items():
        path = os.path.join(ASSETS_DIR, f"{key}.png")
        if not os.path.exists(path):
            _create_gradient_image(path, 400, 260, c1, c2, labels.get(key, key))


def _create_gradient_image(path, w, h, c1, c2, label=""):
    img = Image.new("RGB", (w, h), c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / max(h - 1, 1)
        r = int(int(c1[1:3], 16) * (1 - ratio) + int(c2[1:3], 16) * ratio)
        g = int(int(c1[3:5], 16) * (1 - ratio) + int(c2[3:5], 16) * ratio)
        b = int(int(c1[5:7], 16) * (1 - ratio) + int(c2[5:7], 16) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    if label:
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except OSError:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((w - tw) // 2, (h - th) // 2), label, fill="white", font=font)
    img.save(path)


def load_image(name, size=(360, 200)):
    """Load and cache a Pillow image as PhotoImage."""
    key = (name, size)
    if key in _image_cache:
        return _image_cache[key]
    ensure_assets()
    base = name.rsplit("_", 1)[0] if name.rsplit("_", 1)[-1].isdigit() else name
    path = os.path.join(ASSETS_DIR, f"{base}.png")
    if not os.path.exists(path):
        path = os.path.join(ASSETS_DIR, f"{name}.png")
    if not os.path.exists(path):
        ensure_assets()
        path = os.path.join(ASSETS_DIR, "registan.png")
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    _image_cache[key] = photo
    return photo


def styled_button(parent, text, command=None, style="primary", width=None):
    """Create a styled tk Button."""
    styles = {
        "primary": {"bg": PRIMARY, "fg": WHITE, "activebackground": SECONDARY},
        "secondary": {"bg": CARD, "fg": TEXT, "activebackground": BORDER},
        "accent": {"bg": ACCENT, "fg": TEXT, "activebackground": "#E6AC00"},
        "outline": {"bg": WHITE, "fg": PRIMARY, "activebackground": CARD},
        "danger": {"bg": DANGER, "fg": WHITE, "activebackground": "#C82333"},
    }
    s = styles.get(style, styles["primary"])
    kw = dict(
        text=text,
        command=command,
        bg=s["bg"],
        fg=s["fg"],
        activebackground=s["activebackground"],
        activeforeground=s["fg"],
        font=("Segoe UI", 11, "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=16,
        pady=10,
        bd=0,
    )
    if width:
        kw["width"] = width
    btn = tk.Button(parent, **kw)
    return btn


def link_label(parent, text, command):
    """Clickable link-style label."""
    lbl = tk.Label(
        parent,
        text=text,
        fg=PRIMARY,
        bg=BACKGROUND,
        font=("Segoe UI", 10, "underline"),
        cursor="hand2",
    )
    lbl.bind("<Button-1>", lambda e: command())
    return lbl


def section_title(parent, text, bg=BACKGROUND):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 18, "bold"),
        fg=TEXT,
        bg=bg,
        anchor="w",
    )


def subtitle_label(parent, text, bg=BACKGROUND):
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 10),
        fg=TEXT_LIGHT,
        bg=bg,
        anchor="w",
        wraplength=360,
        justify="left",
    )


def card_frame(parent, bg=CARD, padx=12, pady=12):
    f = tk.Frame(parent, bg=bg, highlightbackground=BORDER, highlightthickness=1)
    return f


def entry_field(parent, placeholder="", show=None, width=32):
    entry = tk.Entry(
        parent,
        font=("Segoe UI", 11),
        fg=TEXT,
        bg=WHITE,
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=PRIMARY,
        width=width,
        show=show,
    )
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=TEXT_LIGHT)

        def on_focus_in(_):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=TEXT)

        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=TEXT_LIGHT)

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    return entry


def get_entry_value(entry, placeholder=""):
    val = entry.get().strip()
    if placeholder and val == placeholder:
        return ""
    return val


def star_rating(parent, rating, bg=CARD):
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    stars = "★" * full + ("½" if half else "") + "☆" * empty
    return tk.Label(
        parent,
        text=f"{stars}  {rating}",
        font=("Segoe UI", 10),
        fg=ACCENT,
        bg=bg,
    )


def bottom_nav(parent, items, active_index, on_select):
    """Bottom navigation bar: list of (icon_char, label)."""
    nav = tk.Frame(parent, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
    nav.pack(side=tk.BOTTOM, fill=tk.X)

    for i, (icon, label) in enumerate(items):
        color = PRIMARY if i == active_index else TEXT_LIGHT
        btn_frame = tk.Frame(nav, bg=WHITE, cursor="hand2")
        btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, pady=6)

        icon_lbl = tk.Label(btn_frame, text=icon, font=("Segoe UI", 14), fg=color, bg=WHITE)
        icon_lbl.pack()
        text_lbl = tk.Label(btn_frame, text=label, font=("Segoe UI", 8), fg=color, bg=WHITE)
        text_lbl.pack()

        def bind_click(idx, frame, il, tl):
            def handler(_=None):
                on_select(idx)

            for w in (frame, il, tl):
                w.bind("<Button-1>", handler)

        bind_click(i, btn_frame, icon_lbl, text_lbl)
    return nav


def scrollable_frame(parent, bg=BACKGROUND):
    """Return (canvas, inner_frame) for scrollable content."""
    container = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    win = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_configure(event):
        canvas.itemconfig(win, width=event.width)

    canvas.bind("<Configure>", _on_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    container.pack(fill=tk.BOTH, expand=True)
    return container, canvas, inner


def show_toast(root, message, is_error=False):
    toast = tk.Toplevel(root)
    toast.overrideredirect(True)
    toast.attributes("-topmost", True)
    color = DANGER if is_error else PRIMARY
    lbl = tk.Label(
        toast,
        text=message,
        bg=color,
        fg=WHITE,
        font=("Segoe UI", 10),
        padx=16,
        pady=10,
    )
    lbl.pack()
    toast.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - toast.winfo_width()) // 2
    y = root.winfo_y() + 60
    toast.geometry(f"+{x}+{y}")
    toast.after(2500, toast.destroy)
