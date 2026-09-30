"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            ptype=row[1],
            adress=row[2],
            area=row[3],
            price=row[4], 
            qty=row[5],
            photo=row[6]
        )
        products.append(product)
    return products


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)

def get_products_by_category(category):
    """Возвращает список объектов Product по типу жилья."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE тип = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
                product_id=row[0],
                ptype=row[1],
                adress=row[2],
                area=row[3],
                price=row[4], 
                qty=row[5],
                photo=row[6]
            )
        products.append(product)
    return products


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
                product_id=row[0],
                ptype=row[1],
                adress=row[2],
                area=row[3],
                price=row[4], 
                qty=row[5],
                photo=row[6]
            )
        products.append(product)
    return products


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой (псевдо)."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        mark = "★" if p.qty <= 3 else " "
        print(f"{mark} {p.info()}")
        print("-" * 60)

if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары типа «Студия»:")
    print_catalog_with_highlight(get_products_by_category("Студия"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())