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


def test_prices():
    """Проверяет, что у всех товаров есть цена."""
    products = db.get_all_products()
    for p in products:
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            return
    print("✅ У всех товаров есть цена")


def test_quantity():
    """Проверяет, что у всех товаров количество ≥ 0."""
    products = db.get_all_products()
    for p in products:
        if p.quantity is None or p.quantity < 0:
            print(f"❌ Товар id={p.id}: некорректное количество ({p.quantity})")
            return
    print("✅ У всех товаров количество ≥ 0")


def test_images():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    has_image = any(p.photo for p in products)
    if has_image:
        print("✅ Есть товары с изображением")
    else:
        print("❌ Ни у одного товара нет изображения")


if __name__ == "__main__":
    test_fields()
    test_prices()
    test_quantity()
    test_images()