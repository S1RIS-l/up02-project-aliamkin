"""Модуль расчёта скидки.

Условие: скидка 5% при площади > 100 кв.м.
"""

import sqlite3
import os

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "databases", "db_variant_16.db"
)


def get_product_area(product_id):
    """Возвращает площадь товара по id."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT площадь FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def calculate_price_with_discount(product_id, price, date=None):
    """
    Рассчитывает цену со скидкой 5% при площади > 100 кв.м.

    :param product_id: id товара
    :param price: базовая цена
    :param date: дата расчёта (не используется)
    :return: цена со скидкой или без
    """
    area = get_product_area(product_id)
    if area is None:
        return price
    if area > 100:
        return price * 0.95
    return price