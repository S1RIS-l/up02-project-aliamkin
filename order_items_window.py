"""Окно состава заказа"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_FAMILY
)
import order_manager as om

FONT_SIZE_NORMAL = 12
FONT_SIZE_TITLE = 18


def font(size=FONT_SIZE_NORMAL, bold=False):
    """Возвращает кортеж шрифта."""
    return (FONT_FAMILY, size, "bold" if bold else "normal")


class OrderItemsWindow:
    """Окно состава заказа."""

    def __init__(self, parent, order_id):
        """
        Инициализация окна.

        :param parent: родительское окно
        :param order_id: id заказа
        """
        self.order_id = order_id

        self.window = tk.Toplevel(parent)
        self.window.title(f"Состав заказа №{order_id}")
        self.window.geometry("850x500")
        self.window.configure(bg=COLOR_MAIN_BG)
        self.build_ui()
        self.load_items()

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header,
                 text=f"СОСТАВ ЗАКАЗА №{self.order_id}",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Таблица позиций
        # Колонки: тип, адрес, количество, цена, сумма (без размера!)
        columns = ("name", "address", "quantity", "price", "total")
        self.tree = ttk.Treeview(
            self.window,
            columns=columns,
            show="headings",
            height=12
        )

        self.tree.heading("name", text="Тип")
        self.tree.heading("address", text="Адрес")
        self.tree.heading("quantity", text="Кол-во")
        self.tree.heading("price", text="Цена")
        self.tree.heading("total", text="Сумма")

        self.tree.column("name", width=150, anchor="w")
        self.tree.column("address", width=250, anchor="w")
        self.tree.column("quantity", width=80, anchor="center")
        self.tree.column("price", width=120, anchor="e")
        self.tree.column("total", width=130, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Итоговая сумма
        self.total_label = tk.Label(
            self.window,
            text="",
            font=font(FONT_SIZE_NORMAL, bold=True),
            fg=COLOR_ACCENT,
            bg=COLOR_MAIN_BG
        )
        self.total_label.pack(pady=10)

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Обновить",
                  command=self.load_items,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def load_items(self):
        """Загружает позиции заказа из БД."""
        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            items = om.get_order_items(self.order_id)

            for item in items:
                # item = (id, тип, адрес, количество, цена)
                name = item[1]
                address = item[2]
                quantity = item[3]
                price = item[4]
                item_total = quantity * price

                self.tree.insert(
                    "", tk.END,
                    values=(
                        name,
                        address,
                        quantity,
                        f"{price:,.2f}",
                        f"{item_total:,.2f}"
                    )
                )

            # Итоговая сумма
            total = om.get_order_total(self.order_id)
            self.total_label.config(
                text=f"Итого: {total:,.2f} руб."
            )

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось загрузить состав:\n{e}"
            )