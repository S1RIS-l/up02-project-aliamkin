"""Работа с заказами"""

import sqlite3
from datetime import datetime

from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, date=None):
    """
    Добавляет новый заказ (без позиций).

    :param client: ФИО клиента
    :param date: дата заказа (по умолчанию — сегодня)
    :return: id заказа или None
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


def add_order_item(order_id, product_id, quantity, price):
    """
    Добавляет позицию в состав заказа.

    :param order_id: id заказа
    :param product_id: id товара
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
    Создаёт заказ с несколькими позициями (одна транзакция).

    :param client: ФИО клиента
    :param items: список кортежей (product_id, quantity, price)
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cur.execute(
            "INSERT INTO Заказ (дата, клиент) VALUES (?, ?)",
            (date, client)
        )
        order_id = cur.lastrowid

        for product_id, quantity, price in items: 
            cur.execute(
                "SELECT количество FROM Товар WHERE id = ?",
                (product_id,)
            )
            row = cur.fetchone()

            if not row or row[0] < quantity:
                raise ValueError(
                    f"Недостаточно товара id={product_id}"
                )

            cur.execute(
                "INSERT INTO Состав_заказа "
                "(заказ_id, товар_id, количество, цена) "
                "VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )

            cur.execute(
                "UPDATE Товар SET количество = количество - ? "
                "WHERE id = ?",
                (quantity, product_id)
            )

        conn.commit()
        return order_id

    except Exception as e:
        conn.rollback()
        print(f"❌ Ошибка создания заказа: {e}")
        return None

    finally:
        conn.close()


def get_product_quantity(product_id):
    """Возвращает количество товара по id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT количество FROM Товар WHERE id = ?",
                (product_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 0


def get_last_order_id():
    """Возвращает id последнего заказа."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(id) FROM Заказ")
    row = cur.fetchone()
    conn.close()
    return row[0] if row and row[0] is not None else None

def get_order_items(order_id):
    """
    Возвращает состав заказа.

    :param order_id: id заказа
    :return: список кортежей (id, название, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Состав_заказа.id, Товар.тип,
               Состав_заказа.количество, Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_order_items(order_id):
    """
    Возвращает состав заказа с полной информацией.

    :param order_id: id заказа
    :return: список кортежей (id, тип, адрес, количество, цена)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            Состав_заказа.id,
            Товар.тип,
            Товар.адрес,
            Состав_заказа.количество,
            Состав_заказа.цена
        FROM Состав_заказа
        JOIN Товар ON Состав_заказа.товар_id = Товар.id
        WHERE Состав_заказа.заказ_id = ?
        ORDER BY Состав_заказа.id
    """, (order_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def get_order_total(order_id):
    """
    Возвращает итоговую сумму заказа.

    :param order_id: id заказа
    :return: сумма (float)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT SUM(количество * цена)
        FROM Состав_заказа
        WHERE заказ_id = ?
    """, (order_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] or 0.0

def get_all_orders():
    """
    Возвращает список всех заказов.

    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, дата, клиент FROM Заказ ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return rows