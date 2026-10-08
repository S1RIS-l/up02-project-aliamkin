"""Главное окно приложения"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
from PIL import Image, ImageTk

from config import APP_TITLE

import database as db
from db_products import get_all_products

from catalog import create_product_card
from error_handler import safe_call


COLOR_MAIN_BG = "#FFFFFF"
COLOR_SECONDARY_BG = "#D2F6E7"
COLOR_ACCENT = "#70B2AF"
FONT_FAMILY = "Calibri"
FONT_SIZE_NORMAL = 12
FONT_SIZE_TITLE = 18

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
                root._icon_photo = icon_img  # сохраняем ссылку
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class CatalogWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)
        self.set_icon()

        # Текущий пользователь (кортеж или None)
        self.current_user = None
        self.user_label = None

        self.build_ui()
        self.load_products()
        self.require_auth()

    def set_icon(self):
        """Устанавливает иконку приложения."""
        set_app_icon(self.root, PATH_ICON)

    def build_ui(self):
        """Строит интерфейс главного окна."""
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

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
            logo_label.image = logo  # сохраняем ссылку
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        # Заголовок (по центру)
        tk.Label(header, text="КАТАЛОГ НЕДВИЖИМОСТИ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", expand=True)

        # ФИО пользователя (правый верхний угол)
        self.user_label = tk.Label(header,
                                    text="Не авторизован",
                                    font=font(FONT_SIZE_NORMAL),
                                    bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

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

    def require_auth(self):
        """Запрашивает авторизацию."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """
        Обработчик успешной авторизации.

        :param user: кортеж (id, фамилия, имя, отчество, логин, роль)
        """
        self.current_user = user

        # Отображаем ФИО
        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        self.user_label.config(text=f"{fio} ({user[5]})")

        # Добавляем кнопки в зависимости от роли
        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """
        Добавляет кнопки в зависимости от роли.

        :param role: название роли
        """
        header = self.user_label.master

        # Кнопка «Выйти» — для всех авторизованных
        tk.Button(header, text="Выйти",
                  command=self.logout,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=10, pady=5).pack(side="right", padx=10)

        # Менеджер и Администратор видят «Заказы»
        if role in ("Менеджер", "Администратор"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

        # Администратор видит «Админ-панель»
        if role == "Администратор":
            tk.Button(header, text="Админ-панель",
                      command=self.open_admin,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="left", padx=10)

    def logout(self):
        """Выход из системы."""
        self.current_user = None
        self.user_label.config(text="Не авторизован")

        # Удаляем кнопки ролей из шапки
        header = self.user_label.master
        for widget in header.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        self.require_auth()

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Открывает админ-панель."""
        messagebox.showinfo("Информация",
                            "Админ-панель в разработке")

    def load_products(self):
        """Загружает товары в каталог (объекты Product)."""
        products = safe_call(get_all_products) or []

        if not products:
            messagebox.showwarning(
                "Нет данных",
                "Товары не найдены в базе данных"
            )
            return

        for p in products:
            safe_call(
                create_product_card,
                self.catalog_frame, p,
                refresh=self.refresh_catalog
            )

    def refresh_catalog(self):
        """Обновляет каталог (удаляет карточки и грузит заново)."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()


    def run(self):
        """Запускает главный цикл приложения."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("Приложение закрыто (Ctrl+C)")
            self.root.destroy()

if __name__ == "__main__":
    CatalogWindow().run()