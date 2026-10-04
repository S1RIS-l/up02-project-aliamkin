"""Каталог товаров"""

import tkinter as tk
from PIL import Image, ImageTk
import os

from styles import COLOR_HIGHLIGHT, FONT_FAMILY

# Пути к ресурсам
PATH_PICTURE = "resources/picture.png"


def create_product_card(parent, product):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    area = product.area
    price = product.price

    # Подсветка, если количество ≤ 3
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else "white"

    # Карточка — рамка со всех сторон
    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)
    tk.Frame(parent, height=1, bg="#cccccc").pack(fill="x", padx=10)

    # === Изображение (слева) ===
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

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
        # Если даже заглушка не открылась — текстовый фолбэк
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    # === Текстовая часть (справа) ===
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(text_frame, text=f"{product.address} | {product.ptype}",
             font=(FONT_FAMILY, 14, "bold"), bg=bg_color,
             anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Категория: {product.ptype}",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Площадь: {area} кв.м",
             font=(FONT_FAMILY, 11), bg=bg_color,
             anchor="w").pack(fill="x")

    if area > 100:
        price_text = f"{price * 0.95:,.0f} руб. (скидка 5%)"
    else:
        price_text = f"{price:,.0f} руб."

    tk.Label(text_frame, text=price_text,
             font=(FONT_FAMILY, 14, "bold"), bg=bg_color,
             anchor="e").pack(fill="x")

    return card