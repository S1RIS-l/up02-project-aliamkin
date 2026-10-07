"""Главное окно с каталогом"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

from config import APP_TITLE
import db_products as db
from catalog import create_product_card
from error_handler import safe_call

COLOR_SECONDARY_BG = "#D2F6E7"
COLOR_ACCENT = "#70B2AF"
FONT_FAMILY = "Calibri"
FONT_SIZE_TITLE = 18
FONT_SIZE_NORMAL = 12

PATH_LOGO = "resources/logo1.png"
PATH_ICON = "resources/icon.ico"


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает кортеж шрифта."""
    return (FONT_FAMILY, size, "bold" if bold else "normal")


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
                root._icon_photo = icon_img
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
        """Устанавливает иконку приложения."""
        set_app_icon(self.root, PATH_ICON)

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root)

    def build_ui(self):
        """Строит интерфейс главного окна."""
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Кнопка «Заказы» (справа)
        tk.Button(header, text="Заказы",
                  command=self.open_orders,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=10)

        # Логотип (слева)
        logo = None
        if os.path.exists(PATH_LOGO):
            try:
                img = Image.open(PATH_LOGO)
                img.thumbnail((60, 60))
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
                 font=font(FONT_SIZE_TITLE, bold=True),
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
        """Загружает товары с обработкой ошибок."""
        products = safe_call(db.get_all_products) or []
        
        if not products:
            messagebox.showwarning("Нет данных",
                               "Товары не найдены в БД")
            return
        
        for p in products:
            safe_call(create_product_card,
                  self.catalog_frame, p,
                  refresh=self.refresh_catalog)

    def refresh_catalog(self):
        """Обновляет каталог (удаляет все карточки и перезагружает)."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()
    
    def run(self):
        """Запускает главный цикл приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()