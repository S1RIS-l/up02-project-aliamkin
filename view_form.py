"""Форма просмотра товара"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_FAMILY, COLOR_HIGHLIGHT
)
from error_handler import validate_positive_int
from order_manager import (
    create_order,
    get_product_quantity
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
        :param on_add_to_order: callback для обновления каталога
        """
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product.ptype}")
        self.window.geometry("700x650")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="КАРТОЧКА ТОВАРА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Основная область
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение (слева)
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10, anchor="n")

        photo = self._load_photo()
        if photo:
            img_label = tk.Label(img_frame, image=photo,
                                 bg=COLOR_MAIN_BG)
            img_label.image = photo  # сохраняем ссылку!
            img_label.pack()
        else:
            tk.Label(img_frame, text="[НЕТ ФОТО]", bg=COLOR_MAIN_BG,
                     width=15, height=10).pack()

        # Информация (справа)
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        self._add_field(info_frame, "Тип", self.product.ptype)
        self._add_field(info_frame, "Адрес", self.product.address)
        self._add_field(info_frame, "Категория", self.product.ptype)
        self._add_field(info_frame, "Площадь",
                        f"{self.product.area} кв.м")
        self._add_field(info_frame, "Количество",
                        self.product.quantity)

        # Цена со скидкой 5% при площади > 100
        area = self.product.area if self.product.area is not None else 0
        price = self.product.price if self.product.price is not None else 0

        if area > 100:
            price_text = f"{price * 0.95:,.0f} руб. (скидка 5%)"
        else:
            price_text = f"{price:,.0f} руб."

        self._add_field(info_frame, "Цена", price_text)

        qty_frame = tk.Frame(info_frame, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10)

        tk.Label(qty_frame, text="Количество:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left")

        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(qty_frame, textvariable=self.qty_var,
                 width=10)
        qty_entry.pack(side="left", padx=10)

        # Кнопки внизу
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

        path = (self.product.photo if self.product.photo
                else "resources/picture.png")
        if not os.path.exists(path):
            path = "resources/picture.png"

        try:
            img = Image.open(path).resize((200, 200))
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

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

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if self.product is None:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        ok, result = validate_positive_int(
            self.qty_var.get(), "Количество"
        )
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = result

        current_qty = get_product_quantity(self.product.id)
        if qty > current_qty:
            messagebox.showwarning(
                "Ошибка",
                f"Доступно только {current_qty} шт."
            )
            return

        try:
            client = "Сидоров Сидор Сидорович"
            price = self.product.price or 0

            items = [(self.product.id, qty, price)]
            order_id = create_order(client, items)

            if order_id is None:
                messagebox.showerror(
                    "Ошибка",
                    "Не удалось создать заказ"
                )
                return

            new_qty = get_product_quantity(self.product.id)

            if new_qty <= 3:
                messagebox.showwarning(
                    "Внимание",
                    f"Товар «{self.product.ptype}» заканчивается!\n"
                    f"Осталось {new_qty} шт."
                )

            messagebox.showinfo(
                "Успех",
                f"Заказ №{order_id} оформлен\n"
                f"Товар: {self.product.ptype}\n"
                f"Остаток: {new_qty} шт."
            )

            if self.on_add_to_order is not None:
                self.on_add_to_order()

            self.window.destroy()

        except Exception as e:
            messagebox.showerror(
                "Ошибка заказа",
                f"Не удалось оформить заказ:\n{e}"
            )