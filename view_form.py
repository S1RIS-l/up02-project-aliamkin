"""Форма просмотра товара"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_FAMILY, COLOR_HIGHLIGHT
)

FONT_SIZE_NORMAL = 12
FONT_SIZE_HEADER = 14
FONT_SIZE_TITLE = 18


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает кортеж шрифта."""
    return (FONT_FAMILY, size, "bold" if bold else "normal")


class ViewForm:
    """
    Форма просмотра выбранного товара.
    Открывается при клике на карточку в каталоге.
    """

    def __init__(self, parent, product, on_add_to_order=None):
        """
        Инициализация формы.

        :param parent: родительское окно
        :param product: объект Product из БД
        :param on_add_to_order: callback для добавления в заказ
        """
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.ptype}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка — ГОТОВО
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)

        photo = self._load_photo()
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG,
                     width=15, height=10).pack()

        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Тип", self.product.ptype)
        self._add_field(info_frame, "Адрес", self.product.address)
        self._add_field(info_frame, "Категория", self.product.ptype)
        self._add_field(info_frame, "Площадь",
                        f"{self.product.area} кв.м")
        self._add_field(info_frame, "Количество", self.product.quantity)

        # Цена со скидкой 5% при площади > 100
        area = self.product.area if self.product.area is not None else 0
        price = self.product.price if self.product.price is not None else 0
        if area > 100:
            price_text = f"{price * 0.95:,.0f} руб. (скидка 5%)"
        else:
            price_text = f"{price:,.0f} руб."
        self._add_field(info_frame, "Цена", price_text)

        # Кнопки — ДОПИСАНО
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _load_photo(self):
        """Загружает фото товара или заглушку."""
        import os
        from PIL import Image, ImageTk

        path = self.product.photo if self.product.photo else "resources/picture.png"
        if not os.path.exists(path):
            path = "resources/picture.png"

        try:
            img = Image.open(path).resize((200, 200))
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    # =========================================
    # ЗАДАНИЕ 4.1. Метод _add_field
    # =========================================
    def _add_field(self, parent, label, value):
        """
        Добавляет поле в форму.

        :param parent: родительский фрейм
        :param label: название поля
        :param value: значение
        """
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

        tk.Label(row, text=str(value),
                 font=font(FONT_SIZE_NORMAL),
                 anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

    # =========================================
    # ЗАДАНИЕ 4.4. Метод add_to_order
    # =========================================
    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        # 1. Если callback отсутствует
        if self.on_add_to_order is None:
            messagebox.showinfo("Информация",
                                "Функция в разработке")
            return

        # 2. Если товар пустой
        if self.product is None:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 3-5. Обернуть вызов в try-except
        try:
            self.on_add_to_order(self.product)
            messagebox.showinfo("Успех", "Товар добавлен в заказ")
        except Exception as e:
            messagebox.showerror(
                "Ошибка заказа",
                f"Не удалось добавить товар:\n{e}"
            )