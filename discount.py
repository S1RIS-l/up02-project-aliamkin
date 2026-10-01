"""Модуль расчёта скидки.

Условие варианта: скидка 5% при площади > 100 кв.м.
"""

import sqlite3
import os

DB_PATH = r"C:\Users\user\up02_project\databases\db_variant_16.db"


def get_product_area(product_id):
    """
    Возвращает площадь товара по его id.

    :param product_id: id товара
    :return: площадь (float) или None, если товар не найден
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT площадь FROM Товар WHERE id = ?",
        (product_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def calculate_price_with_discount(product_id, price, date=None):
    """
    Рассчитывает цену со скидкой 5% при площади > 100 кв.м.

    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта (не используется в этом варианте, оставлен для совместимости)
    :return: цена со скидкой или без
    """
    area = get_product_area(product_id)

    # Если товар не найден — возвращаем базовую цену
    if area is None:
        return price

    # Скидка 5% при площади > 100 кв.м
    if area > 100:
        return price * 0.95  # 5% скидка

    return price