"""Модуль работы с БД db_variant_16"""

import sqlite3
from config import DB_PATH


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_all_products():
    """Список всех товаров (кортежи)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, тип, адрес, площадь, цена, количество, фото "
        "FROM Товар ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_categories():
    """Уникальные категории (типы объектов)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT тип FROM Товар ORDER BY тип")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def get_all_orders():
    """Список всех заказов."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_user_by_login(login):
    """
    Ищет пользователя по логину.

    :param login: логин
    :return: кортеж (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            Пользователь.id,
            Пользователь.фамилия,
            Пользователь.имя,
            Пользователь.отчество,
            Пользователь.логин,
            Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row


def get_all_users():
    """Список всех пользователей."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            Пользователь.id,
            Пользователь.фамилия,
            Пользователь.имя,
            Пользователь.логин,
            Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        ORDER BY Пользователь.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def get_all_roles():
    """Список всех ролей."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, название FROM Роль ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print("Пользователи:")
    for u in get_all_users():
        print(" ", u)