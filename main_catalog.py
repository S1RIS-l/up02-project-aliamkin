"""Главное окно с каталогом."""

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from config import APP_TITLE
import db_products as db
from catalog import create_product_card

# Пути к ресурсам
PATH_LOGO = "resources/logo.png"
PATH_ICON = "resources/icon.ico"

COLOR_SECONDARY_BG = "#D2F6E7"
FONT_FAMILY = "Calibri"
FONT_SIZE_TITLE = 18


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения кроссплатформенно."""
    try:
        if os.name == "nt":  # Windows
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:  # Linux/Mac
            png_path = icon_path.replace(".ico", ".png")
            if os.path.exists(png_path):
                img = Image.open(png_path)
                img.thumbnail((32, 32))
                icon_img = ImageTk.PhotoImage(img)
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img  # сохраняем ссылку
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.set_icon()
        self.build_ui()
        self.load_products()

    def set_icon(self):
        set_app_icon(self.root, PATH_ICON)

    def build_ui(self):
        # Шапка с логотипом и заголовком
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Логотип (слева) — с сохранением пропорций
        logo = None
        if os.path.exists(PATH_LOGO):
            try:
                img = Image.open(PATH_LOGO)
                img.thumbnail((60, 60))  # сохраняет пропорции!
                logo = ImageTk.PhotoImage(img)
            except Exception:
                logo = None

        if logo:
            logo_label = tk.Label(header, image=logo,
                                  bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок (по центру)
        tk.Label(header, text="КАТАЛОГ НЕДВИЖИМОСТИ",
                 font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold"),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg="white",
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_products(self):
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()