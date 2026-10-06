"""Работа с заказами"""

import sqlite3
from datetime import datetime

from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в БД.

    :param client: ФИО клиента
    :param product_id: id товара
    :param quantity: количество
    :return: id заказа или None при ошибке
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        date = datetime.now().strftime("%Y-%m-%d")

        cur.execute(
            "INSERT INTO Заказ (дата, клиент, товар_id, количество) "
            "VALUES (?, ?, ?, ?)",
            (date, client, product_id, quantity)
        )
        conn.commit()

        order_id = cur.lastrowid 
        conn.close()
        return order_id
    except Exception as e:
        print(f"❌ Ошибка добавления заказа: {e}")
        return None


def update_product_quantity(product_id, new_quantity):
    """
    Обновляет количество товара в БД.

    :param product_id: id товара
    :param new_quantity: новое количество
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "UPDATE Товар SET количество = ? WHERE id = ?",
            (new_quantity, product_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка обновления количества: {e}")


def get_last_order_id():
    """
    Возвращает id последнего заказа.

    :return: id или None
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT MAX(id) FROM Заказ")
        row = cur.fetchone()
        conn.close()

        return row[0] if row and row[0] is not None else None
    except Exception as e:
        print(f"❌ Ошибка получения id: {e}")
        return None


def get_product_quantity(product_id):
    """
    Возвращает количество товара по id.

    :param product_id: id товара
    :return: количество или 0
    """
    #ГОТОВО
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?",
                (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


if __name__ == "__main__":
    print("Последний заказ:", get_last_order_id())
    print("Количество товара id=1:", get_product_quantity(1))