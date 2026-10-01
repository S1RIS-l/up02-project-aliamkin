"""Загрузка заказов из БД."""
import sqlite3
from config import DB_PATH
from models import Order, Product


def get_all_orders():
    """Возвращает список объектов Order из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        product = Product(
            product_id=row[3], ptype="", adress="", area=0,
            price=0, qty=0, photo=""
        )
        order = Order(
            order_id=row[0],
            date=row[1],
            client=row[2],
            product=product,
            quantity=row[4]
        )
        orders.append(order)
    return orders


if __name__ == "__main__":
    for o in get_all_orders():
        print(o.info())