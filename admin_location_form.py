"""Full location add/edit form for admin panel."""

import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from models import store
from theme import theme_manager
from ui_utils import ASSETS_DIR, clear_image_cache, ensure_assets, get_entry_value, scrollable_frame


def _slug(name):
    s = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return s or "location"


def _copy_image_to_assets(src_path, dest_key):
    ensure_assets()
    dest = os.path.join(ASSETS_DIR, f"{dest_key}.png")
    try:
        from PIL import Image

        img = Image.open(src_path).convert("RGB")
        img = img.resize((800, 500), Image.Resampling.LANCZOS)
        img.save(dest, "PNG")
        clear_image_cache()
        return True
    except Exception as e:
        messagebox.showerror("Image Error", f"Could not save image: {e}")
        return False


class LocationFormDialog(tk.Toplevel):
    CATEGORIES = ["Monument", "Museum", "Mosque", "Popular"]

    def __init__(self, parent, on_save, location=None):
        super().__init__(parent)
        self.on_save = on_save
        self.location = location
        self.image_paths = [None, None, None]
        self.main_image_path = None

        c = theme_manager.get
        self.title("Add Location" if not location else "Edit Location")
        self.geometry("720x680")
        self.configure(bg=c("BACKGROUND"))
        self.transient(parent)
        self.grab_set()

        container = tk.Frame(self, bg=c("BACKGROUND"))
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=12)

        scroll_container, _, inner = scrollable_frame(container, bg=c("BACKGROUND"))
        scroll_container.pack(fill=tk.BOTH, expand=True)

        self._field(inner, "Name *", "name")
        self._field(inner, "City *", "city", default="Samarkand, Uzbekistan")
        self._combo(inner, "Category", "category", self.CATEGORIES)
        self._text_field(inner, "Description *", "description")
        self._field(inner, "Rating (0-5)", "rating", default="4.5")
        self._field(inner, "Reviews count", "reviews", default="0")
        self._field(inner, "Ticket price ($)", "price", default="5")
        self._field(inner, "Open time", "open_time", default="06:00 AM - 09:00 PM")
        self._field(inner, "Latitude", "latitude", default="39.65")
        self._field(inner, "Longitude", "longitude", default="66.97")

        tk.Label(
            inner,
            text="Main cover image *",
            font=("Segoe UI", 10, "bold"),
            fg=c("TEXT"),
            bg=c("BACKGROUND"),
            anchor="w",
        ).pack(fill=tk.X, pady=(12, 4))
        self.main_img_label = tk.Label(inner, text="No file selected", bg=c("CARD"), fg=c("TEXT_LIGHT"))
        self.main_img_label.pack(fill=tk.X, pady=2)
        tk.Button(
            inner,
            text="Choose main image",
            command=self._pick_main_image,
            bg=c("PRIMARY"),
            fg="white",
            relief=tk.FLAT,
            cursor="hand2",
        ).pack(anchor="w", pady=4)

        tk.Label(
            inner,
            text="Gallery images (3)",
            font=("Segoe UI", 10, "bold"),
            fg=c("TEXT"),
            bg=c("BACKGROUND"),
            anchor="w",
        ).pack(fill=tk.X, pady=(12, 4))
        self.gallery_labels = []
        for i in range(3):
            lbl = tk.Label(
                inner,
                text=f"Gallery {i + 1}: No file selected",
                bg=c("CARD"),
                fg=c("TEXT_LIGHT"),
            )
            lbl.pack(fill=tk.X, pady=2)
            self.gallery_labels.append(lbl)
            tk.Button(
                inner,
                text=f"Choose gallery image {i + 1}",
                command=lambda idx=i: self._pick_gallery_image(idx),
                bg=c("SECONDARY"),
                fg="white",
                relief=tk.FLAT,
                cursor="hand2",
            ).pack(anchor="w", pady=2)

        btn_row = tk.Frame(self, bg=c("BACKGROUND"), pady=12)
        btn_row.pack(fill=tk.X, padx=16)
        tk.Button(
            btn_row,
            text="Cancel",
            command=self.destroy,
            bg=c("CARD"),
            fg=c("TEXT"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT, padx=4)
        tk.Button(
            btn_row,
            text="Save Location",
            command=self._save,
            bg=c("PRIMARY"),
            fg="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
        ).pack(side=tk.RIGHT)

        if location:
            self._prefill(location)

    def _field(self, parent, label, key, default=""):
        c = theme_manager.get
        tk.Label(parent, text=label, fg=c("TEXT"), bg=c("BACKGROUND"), anchor="w").pack(
            fill=tk.X, pady=(8, 2)
        )
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg=c("WHITE"),
            fg=c("TEXT"),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=c("BORDER"),
        )
        entry.pack(fill=tk.X, ipady=6)
        entry.insert(0, default)
        setattr(self, f"entry_{key}", entry)

    def _text_field(self, parent, label, key):
        c = theme_manager.get
        tk.Label(parent, text=label, fg=c("TEXT"), bg=c("BACKGROUND"), anchor="w").pack(
            fill=tk.X, pady=(8, 2)
        )
        text = tk.Text(
            parent,
            height=4,
            font=("Segoe UI", 11),
            bg=c("WHITE"),
            fg=c("TEXT"),
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=c("BORDER"),
        )
        text.pack(fill=tk.X)
        setattr(self, f"text_{key}", text)

    def _combo(self, parent, label, key, values):
        c = theme_manager.get
        tk.Label(parent, text=label, fg=c("TEXT"), bg=c("BACKGROUND"), anchor="w").pack(
            fill=tk.X, pady=(8, 2)
        )
        var = tk.StringVar(value=values[0])
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly")
        combo.pack(fill=tk.X)
        setattr(self, f"var_{key}", var)

    def _prefill(self, loc):
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, loc["name"])
        self.entry_city.delete(0, tk.END)
        self.entry_city.insert(0, loc["city"])
        self.var_category.set(loc["category"])
        self.text_description.delete("1.0", tk.END)
        self.text_description.insert("1.0", loc["description"])
        self.entry_rating.delete(0, tk.END)
        self.entry_rating.insert(0, str(loc["rating"]))
        self.entry_reviews.delete(0, tk.END)
        self.entry_reviews.insert(0, str(loc["reviews"]))
        self.entry_price.delete(0, tk.END)
        self.entry_price.insert(0, str(loc["price"]))
        self.entry_open_time.delete(0, tk.END)
        self.entry_open_time.insert(0, loc["open_time"])
        self.entry_latitude.delete(0, tk.END)
        self.entry_latitude.insert(0, str(loc["latitude"]))
        self.entry_longitude.delete(0, tk.END)
        self.entry_longitude.insert(0, str(loc["longitude"]))
        self.main_img_label.config(text=f"Current: {loc.get('image', 'default')}.png")

    def _pick_main_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        if path:
            self.main_image_path = path
            self.main_img_label.config(text=os.path.basename(path))

    def _pick_gallery_image(self, idx):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        if path:
            self.image_paths[idx] = path
            self.gallery_labels[idx].config(text=os.path.basename(path))

    def _save(self):
        name = self.entry_name.get().strip()
        city = self.entry_city.get().strip()
        description = self.text_description.get("1.0", tk.END).strip()
        if not name or not city or not description:
            messagebox.showerror("Validation", "Name, city, and description are required.")
            return

        try:
            rating = float(self.entry_rating.get().strip())
            reviews = int(self.entry_reviews.get().strip())
            price = float(self.entry_price.get().strip())
            latitude = float(self.entry_latitude.get().strip())
            longitude = float(self.entry_longitude.get().strip())
        except ValueError:
            messagebox.showerror("Validation", "Check numeric fields (rating, price, coordinates).")
            return

        slug = _slug(name)
        if self.location:
            slug = self.location.get("image", slug)

        if self.main_image_path:
            if not _copy_image_to_assets(self.main_image_path, slug):
                return

        gallery_keys = []
        for i, path in enumerate(self.image_paths):
            if path:
                key = f"{slug}"
                dest_key = f"{key}_{i + 1}"
                if _copy_image_to_assets(path, dest_key):
                    gallery_keys.append(key)
            elif self.location:
                gallery_keys.append(slug)

        if not self.location and not self.main_image_path:
            messagebox.showerror("Validation", "Please select a main cover image.")
            return

        data = {
            "name": name,
            "category": self.var_category.get(),
            "city": city,
            "description": description,
            "rating": rating,
            "reviews": reviews,
            "price": price,
            "open_time": self.entry_open_time.get().strip(),
            "latitude": latitude,
            "longitude": longitude,
            "image": slug,
        }

        if self.location:
            store.update_location(
                self.location["id"],
                data,
                gallery_image_keys=gallery_keys if gallery_keys else None,
            )
        else:
            store.add_location(data, gallery_image_keys=gallery_keys or [slug])

        self.on_save()
        self.destroy()
