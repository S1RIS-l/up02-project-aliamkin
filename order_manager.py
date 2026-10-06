"""Работа с заказами"""

import sqlite3
from datetime import datetime

from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, date=None):
    """
    Добавляет новый заказ в БД (без позиций).

    :param client: ФИО клиента
    :param date: дата заказа (по умолчанию — сегодня)
    :return: id заказа или None при ошибке
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
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

def add_order_item(order_id, product_id, size, quantity, price):
    """
    Добавляет позицию в состав заказа.

    :param order_id: id заказа
    :param product_id: id товара
    :param size: «размер» (в варианте 16 — тип объекта)
    :param quantity: количество
    :param price: цена за единицу на момент заказа
    :return: id позиции или None
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO Состав_заказа "
            "(заказ_id, товар_id, количество, цена) "
            "VALUES (?, ?, ?, ?)",
            (order_id, product_id, quantity, price)
        )
        conn.commit()
        item_id = cur.lastrowid
        conn.close()
        return item_id
    except Exception as e:
        print(f"❌ Ошибка добавления позиции: {e}")
        return None


def create_order(client, items):
    """
    Создаёт заказ с несколькими позициями в одной транзакции.

    :param client: ФИО клиента
    :param items: список кортежей (product_id, size, quantity, price)
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Создаём заказ
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid

        # 2. Добавляем позиции
        for product_id, size, quantity, price in items:
            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, количество, цена) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )

        # 3. Фиксируем изменения
        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()


if __name__ == "__main__":
    print("Последний заказ:", get_last_order_id())
    print("Количество товара id=1:", get_product_quantity(1))