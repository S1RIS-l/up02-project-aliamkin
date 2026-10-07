"""Модуль работы с базой данных

Предоставляет функции для:
- работы с товарами (каталог);
- работы с заказами;
- работы с пользователями (авторизация).
"""

import sqlite3
from config import DB_PATH


def get_connection():
    """Возвращает соединение с БД."""
    return sqlite3.connect(DB_PATH)


def get_all_products():
    """
    Возвращает список всех товаров (объектов недвижимости).

    :return: список кортежей (id, тип, адрес, площадь, цена, количество, фото)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, тип, адрес, площадь, цена, количество, фото "
        "FROM Товар "
        "ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_product_by_id(product_id):
    """
    Возвращает один товар по id.

    :param product_id: id товара
    :return: кортеж (id, тип, адрес, площадь, цена, количество, фото) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, тип, адрес, площадь, цена, количество, фото "
        "FROM Товар WHERE id = ?",
        (product_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row


def get_categories():
    """
    Возвращает список уникальных категорий (типов объектов).

    :return: список строк
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT тип FROM Товар ORDER BY тип")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows


def get_all_orders():
    """
    Возвращает список всех заказов.

    :return: список кортежей (id, дата, клиент)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, дата, клиент FROM Заказ ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_orders_by_product(product_id):
    """Возвращает все заказы конкретного товара."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, дата, клиент, товар_id, количество "
        "FROM Заказ WHERE товар_id = ? ORDER BY дата",
        (product_id,)
    )
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
    """
    Возвращает список всех пользователей (для Админ-панели).

    :return: список кортежей (id, фамилия, имя, логин, роль)
    """
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
    """
    Возвращает список всех ролей.

    :return: список кортежей (id, название)
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, название FROM Роль ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print("Все товары:")
    for p in get_all_products():
        print(" ", p)

    print("\nКатегории:", get_categories())

    print("\nВсе заказы:")
    for o in get_all_orders():
        print(" ", o)

    print("\nВсе пользователи:")
    for u in get_all_users():
        print(" ", u)

    print("\nВсе роли:")
    for r in get_all_roles():
        print(" ", r)

    # Проверка авторизации
    print("\nПроверка get_user_by_login:")
    for login in ("client1", "manager1", "admin1", "unknown"):
        user = get_user_by_login(login)
        print(f"  {login}: {user}")