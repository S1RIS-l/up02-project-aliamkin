"""Проверка вывода полей"""

import db_products as db


def test_fields():
    """Проверяет, что у всех товаров есть нужные поля."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")


    required_attrs = ["id", "ptype", "address", "area",
                      "price", "quantity", "photo"]

    errors = 0
    for p in products:
        for attr in required_attrs:
            if not hasattr(p, attr):
                print(f"❌ Товар id={p.id}: нет поля '{attr}'")
                errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()