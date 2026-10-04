"""Каталог товаров"""

import tkinter as tk
from PIL import Image, ImageTk
import os

from config import COLOR_HIGHLIGHT, COLOR_MAIN_BG, FONT_FAMILY

PATH_PICTURE = "resources/picture.png"

FONT_SIZE_NORMAL = 11
FONT_SIZE_HEADER = 14


def _get_card_color(qty):
    """
    Возвращает цвет фона карточки.
    
    :param qty: количество товара
    :return: HEX-цвет
    """
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG



def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет метку с текстом."""
    tk.Label(parent, text=text,
             font=(FONT_FAMILY, size, "bold" if bold else "normal"),
             bg=bg_color, anchor=align).pack(fill="x")


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Проверка существования файла
    image_path = product.photo if product.photo else PATH_PICTURE
    if not os.path.exists(image_path):
        image_path = PATH_PICTURE

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # сохраняем ссылку!
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True,
                    padx=10, pady=10)


    ptype = product.ptype if product.ptype else "[Без типа]"
    address = product.address if product.address else "[Без адреса]"
    area = product.area if product.area is not None else 0
    price = product.price if product.price is not None else 0

    _add_label(text_frame, f"{address} | {ptype}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)

    _add_label(text_frame, f"Категория: {ptype}", bg_color)

    indicator = _indicator(qty)
    _add_label(text_frame, f"Количество: {indicator} ({qty})", bg_color)

    _add_label(text_frame, f"Площадь: {area} кв.м", bg_color)


    if area > 100:
        price_text = f"{price * 0.95:,.0f} руб. (скидка 5%)"
    else:
        price_text = f"{price:,.0f} руб."

    _add_label(text_frame, price_text, bg_color,
               bold=True, size=FONT_SIZE_HEADER, align="e")


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    return card