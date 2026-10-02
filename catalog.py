"""Каталог товаров"""

import tkinter as tk
from PIL import Image, ImageTk
import os

from config import COLOR_HIGHLIGHT, FONT_FAMILY

_image_refs = []


def create_product_card(parent, product):

    qty = product.quantity
    area = product.area
    price = product.price

    # Подсветка, если количество ≤ 3
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = product.photo if product.photo else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.pack()
        _image_refs.append(photo)  # сохраняем ссылку, иначе исчезнет
    except Exception:
        tk.Label(img_frame, text="[ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Адрес | Тип
    title = f"{product.address} | {product.ptype}"
    tk.Label(text_frame, text=title,
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="w").pack(fill="x")

    # Категория (тип объекта)
    tk.Label(text_frame, text=f"Категория: {product.ptype}",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    # Количество (индикатор много/мало)
    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    # Состав (площадь)
    tk.Label(text_frame, text=f"Площадь: {area} кв.м",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    # Цена со скидкой 5% при площади > 100
    if area > 100:
        final_price = price * 0.95
        price_text = f"{final_price:,.0f} руб. (скидка 5%)"
    else:
        price_text = f"{price:,.0f} руб."

    tk.Label(text_frame, text=price_text,
             font=(FONT_FAMILY, 14, "bold"),
             bg=bg_color, anchor="e").pack(fill="x")

    return card