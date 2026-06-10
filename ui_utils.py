"""Shared UI components — buttons, cards, forms, navigation."""

import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageDraw, ImageFont, ImageTk

from config import APP_WIDTH
from theme import (
    BUTTON_MAX_WIDTH,
    CONTENT_MAX_WIDTH,
    FONT_BODY,
    FONT_HEADING,
    FONT_LOGO,
    FONT_SMALL,
    FONT_SUBHEADING,
    FONT_TITLE,
    FONT_TINY,
    FORM_MAX_WIDTH,
    NAV_MAX_WIDTH,
    PAD_LG,
    PAD_MD,
    PAD_SM,
    theme_manager,
)

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
_image_cache = {}


def c(key):
    return theme_manager.get(key)


def clear_image_cache():
    global _image_cache
    _image_cache = {}


def configure_ttk_styles():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TScrollbar",
        background=c("CARD"),
        troughcolor=c("BACKGROUND"),
        bordercolor=c("BORDER"),
        arrowcolor=c("TEXT_LIGHT"),
    )


# ---------------------------------------------------------------------------
# Layout helpers
# ---------------------------------------------------------------------------

def create_label(parent, text, style="body", bg=None, fg=None, **kw):
    """Label that inherits parent background — avoids stray color blocks."""
    bg = bg if bg is not None else _parent_bg(parent)
    styles = {
        "title": (FONT_TITLE, c("TEXT")),
        "heading": (FONT_HEADING, c("TEXT")),
        "subheading": (FONT_SUBHEADING, c("TEXT")),
        "body": (FONT_BODY, c("TEXT")),
        "small": (FONT_SMALL, c("TEXT_LIGHT")),
        "tiny": (FONT_TINY, c("TEXT_LIGHT")),
        "inverse": (FONT_BODY, c("HEADER_TEXT")),
        "accent": (FONT_SMALL, c("PRIMARY")),
        "muted": (FONT_SMALL, c("TEXT_LIGHT")),
    }
    font, default_fg = styles.get(style, styles["body"])
    fg = fg or default_fg
    defaults = dict(font=font, fg=fg, bg=bg, anchor="w")
    defaults.update(kw)
    return tk.Label(parent, text=text, **defaults)


def _parent_bg(parent):
    try:
        return parent.cget("bg")
    except tk.TclError:
        return c("BACKGROUND")


def centered_page(parent, max_width=CONTENT_MAX_WIDTH):
    """Full-width wrapper with centered content column."""
    outer = tk.Frame(parent, bg=c("BACKGROUND"))
    outer.pack(fill=tk.BOTH, expand=True)
    outer.grid_columnconfigure(0, weight=1)
    inner = tk.Frame(outer, bg=c("BACKGROUND"))
    inner.grid(row=0, column=0, sticky="n")
    col = tk.Frame(inner, bg=c("BACKGROUND"))
    col.pack(padx=PAD_LG, pady=PAD_MD)
    return col


def centered_column(parent, max_width=FORM_MAX_WIDTH):
    """Center a narrow column (forms, splash actions)."""
    wrapper = tk.Frame(parent, bg=_parent_bg(parent))
    wrapper.pack(fill=tk.X, pady=PAD_SM)
    col = tk.Frame(wrapper, bg=_parent_bg(parent))
    col.pack(anchor="center")
    return col


def form_card(parent, max_width=FORM_MAX_WIDTH):
    """Centered card container for auth / settings forms."""
    outer = tk.Frame(parent, bg=c("BACKGROUND"))
    outer.pack(fill=tk.BOTH, expand=True)
    outer.grid_rowconfigure(0, weight=1)
    outer.grid_columnconfigure(0, weight=1)

    center = tk.Frame(outer, bg=c("BACKGROUND"))
    center.grid(row=0, column=0)

    card = tk.Frame(
        center,
        bg=c("CARD"),
        highlightbackground=c("BORDER"),
        highlightthickness=1,
        padx=PAD_LG + 4,
        pady=PAD_LG + 4,
    )
    card.pack(padx=PAD_LG, pady=PAD_LG)
    return outer, card


def create_card(parent, bg=None, padx=PAD_MD, pady=PAD_MD):
    bg = bg or c("CARD")
    return tk.Frame(
        parent,
        bg=bg,
        highlightbackground=c("BORDER"),
        highlightthickness=1,
        padx=padx,
        pady=pady,
    )


def button_row(parent, max_width=BUTTON_MAX_WIDTH):
    """Centered row for buttons that should not stretch full window."""
    wrapper = tk.Frame(parent, bg=_parent_bg(parent))
    wrapper.pack(fill=tk.X, pady=PAD_SM)
    row = tk.Frame(wrapper, bg=_parent_bg(parent))
    row.pack(anchor="center")
    return row


# ---------------------------------------------------------------------------
# Buttons
# ---------------------------------------------------------------------------

def _bind_hover(btn, normal, hover):
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=normal))


def styled_button(parent, text, command=None, style="primary", width=None, full_width=False):
    """Modern button with hover. Use button_row() parent to avoid full-width stretch."""
    styles = {
        "primary": {
            "bg": c("PRIMARY"),
            "fg": "#FFFFFF",
            "hover": c("PRIMARY_HOVER"),
            "active": c("SECONDARY"),
            "border": 0,
        },
        "secondary": {
            "bg": c("CARD"),
            "fg": c("TEXT"),
            "hover": c("BORDER"),
            "active": c("BORDER"),
            "border": 1,
        },
        "outline": {
            "bg": c("CARD"),
            "fg": c("PRIMARY"),
            "hover": c("BORDER"),
            "active": c("BORDER"),
            "border": 1,
        },
        "ghost": {
            "bg": _parent_bg(parent),
            "fg": c("PRIMARY"),
            "hover": c("CARD"),
            "active": c("CARD"),
            "border": 0,
        },
        "accent": {
            "bg": c("ACCENT"),
            "fg": c("TEXT"),
            "hover": "#E6AC00",
            "active": "#E6AC00",
            "border": 0,
        },
        "danger": {
            "bg": c("DANGER"),
            "fg": "#FFFFFF",
            "hover": "#C82333",
            "active": "#C82333",
            "border": 0,
        },
    }
    s = styles.get(style, styles["primary"])
    kw = dict(
        text=text,
        command=command,
        bg=s["bg"],
        fg=s["fg"],
        activebackground=s["active"],
        activeforeground=s["fg"],
        font=(FONT_BODY[0], FONT_BODY[1], "bold"),
        relief=tk.FLAT,
        cursor="hand2",
        padx=22,
        pady=11,
        bd=s["border"],
        highlightthickness=s["border"],
        highlightbackground=c("BORDER") if s["border"] else s["bg"],
    )
    if width:
        kw["width"] = width
    btn = tk.Button(parent, **kw)
    _bind_hover(btn, s["bg"], s["hover"])
    if full_width:
        btn.pack(fill=tk.X)
    return btn


def back_button(parent, command, text=None):
    from i18n import t

    text = text or t("back")
    btn = styled_button(parent, text, command=command, style="ghost", width=10)
    btn.pack(anchor="w", padx=PAD_LG, pady=(PAD_MD, 0))
    return btn


def page_header(parent, title, subtitle=None):
    hdr = tk.Frame(parent, bg=c("BACKGROUND"))
    hdr.pack(fill=tk.X, padx=PAD_LG, pady=(PAD_MD, PAD_SM))
    create_label(hdr, title, style="heading").pack(anchor="w")
    if subtitle:
        create_label(hdr, subtitle, style="small").pack(anchor="w", pady=(4, 0))
    return hdr


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------

def entry_field(parent, placeholder="", show=None, width=36):
    entry = tk.Entry(
        parent,
        font=FONT_BODY,
        fg=c("TEXT"),
        bg=c("INPUT_BG"),
        insertbackground=c("TEXT"),
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


def section_title(parent, text, bg=None):
    return create_label(parent, text, style="title", bg=bg)


def subtitle_label(parent, text, bg=None, wrap=None):
    bg = bg or _parent_bg(parent)
    wrap = wrap or min(FORM_MAX_WIDTH - 40, 520)
    return tk.Label(
        parent,
        text=text,
        font=FONT_SMALL,
        fg=c("TEXT_LIGHT"),
        bg=bg,
        anchor="w",
        wraplength=wrap,
        justify="left",
    )


def link_label(parent, text, command, bg=None):
    bg = bg if bg is not None else _parent_bg(parent)
    lbl = tk.Label(
        parent,
        text=text,
        fg=c("PRIMARY"),
        bg=bg,
        font=(FONT_SMALL[0], FONT_SMALL[1], "underline"),
        cursor="hand2",
    )
    lbl.bind("<Button-1>", lambda e: command())
    lbl.bind("<Enter>", lambda e: lbl.config(fg=c("SECONDARY")))
    lbl.bind("<Leave>", lambda e: lbl.config(fg=c("PRIMARY")))
    return lbl


# ---------------------------------------------------------------------------
# Ratings, images, grid
# ---------------------------------------------------------------------------

def star_rating(parent, rating, bg=None):
    bg = bg or _parent_bg(parent)
    full = int(rating)
    half = 1 if rating - full >= 0.3 else 0
    empty = 5 - full - half
    stars = "★" * full + ("½" if half else "") + "☆" * empty
    return tk.Label(
        parent,
        text=f"{stars}  {rating}",
        font=FONT_SMALL,
        fg=c("ACCENT"),
        bg=bg,
    )


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
    # Try exact filename first (e.g. registan_2.png for gallery slots)
    path = os.path.join(ASSETS_DIR, f"{name}.png")
    if not os.path.exists(path):
        base = name.rsplit("_", 1)[0] if name.rsplit("_", 1)[-1].isdigit() else name
        path = os.path.join(ASSETS_DIR, f"{base}.png")
    if not os.path.exists(path):
        path = os.path.join(ASSETS_DIR, "registan.png")
    img = Image.open(path).convert("RGB")
    img = img.resize(size, Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    _image_cache[key] = photo
    return photo


def desktop_card_width(parent_width=None):
    w = parent_width or APP_WIDTH
    cols = desktop_columns(w)
    usable = min(w, CONTENT_MAX_WIDTH) - 48
    return max(260, (usable // cols) - 24)


def desktop_columns(parent_width=None):
    w = parent_width or APP_WIDTH
    if w >= 1100:
        return 3
    if w >= 750:
        return 2
    return 1


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

def bottom_nav(parent, items, active_index, on_select):
    """Centered bottom nav bar — does not stretch items on wide screens."""
    bar_bg = c("NAV_BG")
    holder = tk.Frame(parent, bg=c("BACKGROUND"))
    holder.pack(side=tk.BOTTOM, fill=tk.X)

    nav = tk.Frame(
        holder,
        bg=bar_bg,
        highlightbackground=c("BORDER"),
        highlightthickness=1,
    )
    nav.pack(anchor="center", pady=0)

    for i, (icon, label) in enumerate(items):
        active = i == active_index
        color = c("NAV_ACTIVE") if active else c("NAV_INACTIVE")
        bg_item = c("CARD") if active and theme_manager.dark_mode else bar_bg

        btn_frame = tk.Frame(nav, bg=bg_item, cursor="hand2", padx=18, pady=8)
        btn_frame.pack(side=tk.LEFT)

        icon_lbl = tk.Label(btn_frame, text=icon, font=(FONT_BODY[0], 16), fg=color, bg=bg_item)
        icon_lbl.pack()
        text_lbl = tk.Label(btn_frame, text=label, font=FONT_TINY, fg=color, bg=bg_item)
        text_lbl.pack()

        def bind_click(idx, frame, il, tl):
            def handler(_=None):
                on_select(idx)

            for w in (frame, il, tl):
                w.bind("<Button-1>", handler)

        bind_click(i, btn_frame, icon_lbl, text_lbl)
    return holder


def refresh_scroll_region(canvas):
    """Update canvas scrollregion after dynamic content changes."""
    canvas.update_idletasks()
    bbox = canvas.bbox("all")
    if bbox:
        canvas.configure(scrollregion=bbox)


def scrollable_frame(parent, bg=None):
    bg = bg or c("BACKGROUND")
    container = tk.Frame(parent, bg=bg)
    canvas = tk.Canvas(container, bg=bg, highlightthickness=0, bd=0)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=bg)
    win = canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    def _on_inner_configure(_event=None):
        refresh_scroll_region(canvas)

    inner.bind("<Configure>", _on_inner_configure)

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


def setup_optional_background(root):
    """Optional resizable background image behind main content.

    Put your image in assets/background.jpg and set BACKGROUND_IMAGE_PATH in config.py.
    """
    from config import BACKGROUND_IMAGE_PATH

    if not BACKGROUND_IMAGE_PATH:
        return None

    path = BACKGROUND_IMAGE_PATH
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(path):
        return None

    state = {"photo": None, "label": None}

    try:
        from PIL import Image, ImageTk
    except ImportError:
        return None

    bg_label = tk.Label(root, bd=0)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    state["label"] = bg_label

    def _resize(event=None):
        w = root.winfo_width()
        h = root.winfo_height()
        if w < 2 or h < 2:
            return
        try:
            img = Image.open(path).convert("RGB")
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            state["photo"] = ImageTk.PhotoImage(img)
            bg_label.configure(image=state["photo"])
        except OSError:
            bg_label.place_forget()

    root.bind("<Configure>", _resize)
    root.after(100, _resize)
    return bg_label


def show_language_dialog(parent, on_change):
    from i18n import t
    from models import store

    dlg = tk.Toplevel(parent)
    dlg.title(t("language_pick"))
    dlg.geometry("340x260")
    dlg.configure(bg=c("BACKGROUND"))
    dlg.transient(parent)
    dlg.grab_set()

    card = create_card(dlg, padx=PAD_LG, pady=PAD_LG)
    card.pack(padx=PAD_LG, pady=PAD_LG, fill=tk.BOTH, expand=True)

    create_label(card, t("language_pick"), style="subheading", bg=c("CARD")).pack(
        pady=(0, PAD_MD)
    )

    for code, label_key in [("uz", "lang_uz"), ("en", "lang_en"), ("ru", "lang_ru")]:
        active = store.settings.get("language") == code
        styled_button(
            card,
            t(label_key),
            command=lambda lang=code: _pick(lang, dlg, on_change),
            style="primary" if active else "outline",
            full_width=True,
        ).pack(pady=4, fill=tk.X)


def _pick(lang, dlg, on_change):
    from models import store

    store.set_language(lang)
    dlg.destroy()
    if on_change:
        on_change()
