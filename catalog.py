"""Каталог товаров"""

import tkinter as tk
from PIL import Image, ImageTk
import os

from config import COLOR_HIGHLIGHT, FONT_FAMILY
from config import RESOURCES_DIR

PATH_PICTURE = os.path.join(RESOURCES_DIR, "picture.png")

FONT_SIZE_NORMAL = 11
FONT_SIZE_HEADER = 14



def _get_card_color(qty):
    """Возвращает цвет фона карточки (подсветка ≤3)."""
    return COLOR_HIGHLIGHT if qty <= 3 else "white"


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
    """
    Добавляет изображение товара (или заглушку).

    :param card: карточка (tk.Frame)
    :param product: объект Product
    :param bg_color: цвет фона
    """
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    if product.photo:
        image_path = os.path.join(RESOURCES_DIR, product.photo)
    else:
        image_path = PATH_PICTURE

    if not os.path.exists(image_path):
        image_path = PATH_PICTURE

    if not os.path.exists(image_path):
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()
        return
    
    try:
        img = Image.open(image_path).resize((100, 100))
        photo = ImageTk.PhotoImage(img)

        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo  # сохраняем ссылку, иначе исчезнет!
        img_label.pack()

    except Exception as e:
        print(f"⚠️ Ошибка загрузки {image_path}: {e}")
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()


def _add_text_info(card, product, bg_color, qty):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True,
                    padx=10, pady=10)

    # Крайние случаи: если поле пустое — подставляем заглушку
    ptype = product.ptype if product.ptype else "[Без типа]"
    address = product.address if product.address else "[Без адреса]"
    area = product.area if product.area is not None else 0
    price = product.price if product.price is not None else 0

    # Адрес | Тип
    _add_label(text_frame, f"{address} | {ptype}",
               bg_color, bold=True, size=FONT_SIZE_HEADER)

    # Категория (тип)
    _add_label(text_frame, f"Категория: {ptype}", bg_color)

    # Количество с индикатором
    indicator = _indicator(qty)
    _add_label(text_frame, f"Количество: {indicator} ({qty})", bg_color)

    # Площадь (состав)
    _add_label(text_frame, f"Площадь: {area} кв.м", bg_color)

    # Цена со скидкой 5% при площади > 100
    if area > 100:
        price_text = f"{price * 0.95:,.0f} руб. (скидка 5%)"
    else:
        price_text = f"{price:,.0f} руб."

    _add_label(text_frame, price_text, bg_color,
               bold=True, size=FONT_SIZE_HEADER, align="e")


def _open_view(parent, product, refresh=None):
    """
    Открывает форму просмотра товара.

    :param parent: родительский контейнер
    :param product: объект Product
    """
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку товара по макету."""
    qty = product.quantity
    bg_color = _get_card_color(qty)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color, qty)

    def _on_card_click(event=None):
        _open_view(parent, product, refresh)

    card.bind("<Button-1>", _on_card_click)
    for child in card.winfo_children():
        child.bind("<Button-1>", _on_card_click)
        for subchild in child.winfo_children():
            subchild.bind("<Button-1>", _on_card_click)

    return card