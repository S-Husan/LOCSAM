"""Shared UI helpers and styled widgets for LOCSAM."""

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk

from config import APP_WIDTH
from theme import theme_manager

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
_image_cache = {}


def clear_image_cache():
    global _image_cache
    _image_cache = {}


def c(key):
    return theme_manager.get(key)


def ensure_assets():
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
    key = (name, size)
    if key in _image_cache:
        return _image_cache[key]
    ensure_assets()
    base = name.rsplit("_", 1)[0] if name.rsplit("_", 1)[-1].isdigit() else name
    path = os.path.join(ASSETS_DIR, f"{base}.png")
    if not os.path.exists(path):
        path = os.path.join(ASSETS_DIR, f"{name}.png")
    if not os.path.exists(path):
        path = os.path.join(ASSETS_DIR, "registan.png")
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    _image_cache[key] = photo
    return photo


def desktop_card_width(parent_width=None):
    """Compute card image width for responsive desktop grid."""
    w = parent_width or APP_WIDTH
    if w >= 1100:
        return 340
    if w >= 800:
        return 360
    return min(w - 48, 420)


def desktop_columns(parent_width=None):
    w = parent_width or APP_WIDTH
    if w >= 1100:
        return 3
    if w >= 800:
        return 2
    return 1


def styled_button(parent, text, command=None, style="primary", width=None):
    styles = {
        "primary": {"bg": c("PRIMARY"), "fg": "#FFFFFF", "activebackground": c("SECONDARY")},
        "secondary": {"bg": c("CARD"), "fg": c("TEXT"), "activebackground": c("BORDER")},
        "accent": {"bg": c("ACCENT"), "fg": c("TEXT"), "activebackground": "#E6AC00"},
        "outline": {"bg": c("WHITE"), "fg": c("PRIMARY"), "activebackground": c("CARD")},
        "danger": {"bg": "#DC3545", "fg": "#FFFFFF", "activebackground": "#C82333"},
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
    return tk.Button(parent, **kw)


def link_label(parent, text, command, bg=None):
    bg = bg or c("BACKGROUND")
    lbl = tk.Label(
        parent,
        text=text,
        fg=c("PRIMARY"),
        bg=bg,
        font=("Segoe UI", 10, "underline"),
        cursor="hand2",
    )
    lbl.bind("<Button-1>", lambda e: command())
    return lbl


def section_title(parent, text, bg=None):
    bg = bg or c("BACKGROUND")
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 18, "bold"),
        fg=c("TEXT"),
        bg=bg,
        anchor="w",
    )


def subtitle_label(parent, text, bg=None, wrap=None):
    bg = bg or c("BACKGROUND")
    wrap = wrap or min(APP_WIDTH - 80, 600)
    return tk.Label(
        parent,
        text=text,
        font=("Segoe UI", 10),
        fg=c("TEXT_LIGHT"),
        bg=bg,
        anchor="w",
        wraplength=wrap,
        justify="left",
    )


def entry_field(parent, placeholder="", show=None, width=32):
    entry = tk.Entry(
        parent,
        font=("Segoe UI", 11),
        fg=c("TEXT"),
        bg=c("WHITE"),
        relief=tk.FLAT,
        highlightthickness=1,
        highlightbackground=c("BORDER"),
        highlightcolor=c("PRIMARY"),
        width=width,
        show=show,
    )
    if placeholder:
        entry.insert(0, placeholder)
        entry.config(fg=c("TEXT_LIGHT"))

        def on_focus_in(_):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=c("TEXT"))

        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=c("TEXT_LIGHT"))

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
    return entry


def get_entry_value(entry, placeholder=""):
    val = entry.get().strip()
    if placeholder and val == placeholder:
        return ""
    return val


def star_rating(parent, rating, bg=None):
    bg = bg or c("CARD")
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    stars = "★" * full + ("½" if half else "") + "☆" * empty
    return tk.Label(
        parent,
        text=f"{stars}  {rating}",
        font=("Segoe UI", 10),
        fg=c("ACCENT"),
        bg=bg,
    )


def bottom_nav(parent, items, active_index, on_select):
    nav = tk.Frame(parent, bg=c("WHITE"), highlightbackground=c("BORDER"), highlightthickness=1)
    nav.pack(side=tk.BOTTOM, fill=tk.X)

    for i, (icon, label) in enumerate(items):
        color = c("PRIMARY") if i == active_index else c("TEXT_LIGHT")
        btn_frame = tk.Frame(nav, bg=c("WHITE"), cursor="hand2")
        btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, pady=6)

        icon_lbl = tk.Label(btn_frame, text=icon, font=("Segoe UI", 14), fg=color, bg=c("WHITE"))
        icon_lbl.pack()
        text_lbl = tk.Label(btn_frame, text=label, font=("Segoe UI", 8), fg=color, bg=c("WHITE"))
        text_lbl.pack()

        def bind_click(idx, frame, il, tl):
            def handler(_=None):
                on_select(idx)

            for w in (frame, il, tl):
                w.bind("<Button-1>", handler)

        bind_click(i, btn_frame, icon_lbl, text_lbl)
    return nav


def scrollable_frame(parent, bg=None):
    bg = bg or c("BACKGROUND")
    container = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
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


def apply_theme_to_widget(widget, depth=0):
    """Recursively apply current theme colors to tk widgets."""
    if depth > 25:
        return
    try:
        cls = widget.winfo_class()
        if cls in ("Frame", "Toplevel"):
            try:
                widget.configure(bg=c("BACKGROUND"))
            except tk.TclError:
                pass
        elif cls == "Label":
            try:
                cur_bg = widget.cget("bg")
                if cur_bg in ("#6A00FF", "#8E2EFF", theme_manager.palette()["PRIMARY"]):
                    pass
                elif cur_bg in ("#FFFFFF", "#F8F8F8", "#252540", "#2D2D44"):
                    widget.configure(bg=c("CARD"), fg=c("TEXT"))
                else:
                    widget.configure(bg=c("BACKGROUND"), fg=c("TEXT"))
            except tk.TclError:
                pass
        elif cls == "Button":
            try:
                widget.configure(bg=c("PRIMARY"), fg="#FFFFFF")
            except tk.TclError:
                pass
        elif cls == "Entry":
            try:
                widget.configure(bg=c("WHITE"), fg=c("TEXT"))
            except tk.TclError:
                pass
        elif cls == "Text":
            try:
                widget.configure(bg=c("WHITE"), fg=c("TEXT"))
            except tk.TclError:
                pass
        elif cls == "Checkbutton":
            try:
                widget.configure(bg=c("BACKGROUND"), fg=c("TEXT"))
            except tk.TclError:
                pass
    except tk.TclError:
        pass
    for child in widget.winfo_children():
        apply_theme_to_widget(child, depth + 1)


def show_language_dialog(parent, on_change):
    from i18n import t

    dlg = tk.Toplevel(parent)
    dlg.title(t("language_pick"))
    dlg.geometry("320x220")
    dlg.configure(bg=c("BACKGROUND"))
    dlg.transient(parent)
    dlg.grab_set()

    tk.Label(
        dlg,
        text=t("language_pick"),
        font=("Segoe UI", 14, "bold"),
        bg=c("BACKGROUND"),
        fg=c("TEXT"),
    ).pack(pady=16)

    from models import store

    for code, label_key in [("uz", "lang_uz"), ("en", "lang_en"), ("ru", "lang_ru")]:
        tk.Button(
            dlg,
            text=t(label_key),
            width=24,
            command=lambda lang=code: _pick(lang, dlg, on_change),
            bg=c("PRIMARY") if store.settings.get("language") == code else c("CARD"),
            fg=c("TEXT"),
            relief=tk.FLAT,
            pady=8,
        ).pack(pady=4)


def _pick(lang, dlg, on_change):
    from models import store

    store.set_language(lang)
    dlg.destroy()
    if on_change:
        on_change()
