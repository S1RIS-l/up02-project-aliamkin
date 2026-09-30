"""Загрузка товаров из БД с расширенным выводом."""
import sqlite3
from config import DB_PATH


def get_all_products():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    products = cur.fetchall()
    conn.close()
    return products


def get_products_by_category(category):
    """Товары по категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE тип = ?", (category,))
    products = cur.fetchall()
    conn.close()
    return products


def get_products_low_stock():
    """Товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    products = cur.fetchall()
    conn.close()
    return products


def get_categories():
    """Список всех категорий."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT тип FROM Товар ORDER BY тип")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories


def print_catalog(products):
    """Каталог с индикатором."""
    print(f"\n{'=' * 60}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 60)

    for p in products:
        product_id, ptype, address, area, price, qty, photo = (
            p[0], p[1], p[2], p[3], p[4], p[5], p[6]
        )

        # Индикатор «много/мало» (требование задания 6.3)
        indicator = "⚠️  МАЛО" if qty <= 3 else "✅ МНОГО"

        print(f"\n{indicator}  [{product_id}] {ptype}")
        print(f"   Адрес: {address}")
        print(f"   Площадь: {area} м²")
        print(f"   Цена: {price} руб.")
        print(f"   Количество: {qty} шт.")
        print(f"   Фото: {photo}")


if __name__ == "__main__":
    print_catalog(get_all_products())

    print(f"\n{'=' * 60}")
    print("КАТЕГОРИИ:")
    print("=" * 60)
    for cat in get_categories():
        print(f"  • {cat}")

    print(f"\n{'=' * 60}")
    print("ТОВАРЫ С НИЗКИМ ОСТАТКОМ (≤ 3 шт.):")
    print("=" * 60)
    print_catalog(get_products_low_stock())