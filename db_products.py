"""Работа с товарами из БД"""

import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """
    Возвращает список объектов Product.

    :return: list[Product]
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, тип, адрес, площадь, цена, количество, фото "
        "FROM Товар ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            ptype=row[1],
            address=row[2],
            area=row[3],
            price=row[4],
            quantity=row[5],
            photo=row[6],
        )
        products.append(product)
    return products


def get_product_by_id(product_id):
    """Возвращает Product по id или None."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, тип, адрес, площадь, цена, количество, фото "
        "FROM Товар WHERE id = ?",
        (product_id,)
    )
    row = cur.fetchone()
    conn.close()
    if row is None:
        return None
    return Product(
        product_id=row[0],
        ptype=row[1],
        address=row[2],
        area=row[3],
        price=row[4],
        quantity=row[5],
        photo=row[6],
    )


def get_product_sizes(product_id):
    """
    Возвращает список «размеров» для товара.

    :param product_id: id товара
    :return: список типов
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT тип FROM Товар WHERE тип IS NOT NULL")
    rows = cur.fetchall()
    conn.close()
    return [row[0] for row in rows if row[0]]


if __name__ == "__main__":
    for p in get_all_products():
        print(p.info())