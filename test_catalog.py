"""Тестирование каталога (вариант 16)."""

import db_products as db


def test_db_available():
    """Проверяет, что БД доступна."""
    try:
        products = db.get_all_products()
        return isinstance(products, list)
    except Exception as e:
        print(f"❌ БД недоступна: {e}")
        return False


def test_products_count():
    """Проверяет, что товары загружены."""
    products = db.get_all_products()
    return len(products) > 0


def test_product_fields():
    """Проверяет, что у всех товаров есть нужные атрибуты."""
    required = ["id", "ptype", "address", "area",
                "price", "quantity", "photo"]
    products = db.get_all_products()

    for p in products:
        for attr in required:
            if not hasattr(p, attr):
                print(f"❌ Товар id={p.id}: нет поля '{attr}'")
                return False
    return True


def test_prices_are_numbers():
    """Проверяет, что все цены — числа."""
    products = db.get_all_products()
    for p in products:
        if not isinstance(p.price, (int, float)):
            print(f"❌ Товар id={p.id}: цена не число ({type(p.price)})")
            return False
    return True


def test_quantity_not_negative():
    """Проверяет, что количество не отрицательное."""
    products = db.get_all_products()
    for p in products:
        if p.quantity < 0:
            print(f"❌ Товар id={p.id}: отрицательное количество")
            return False
    return True


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название (тип)."""
    products = db.get_all_products()
    for p in products:
        if not p.ptype:
            print(f"❌ Товар id={p.id}: пустое название")
            return False
    return True


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("БД доступна", test_db_available),
        ("Товары загружены", test_products_count),
        ("У всех товаров нужные поля", test_product_fields),
        ("Все цены — числа", test_prices_are_numbers),
        ("Количество не отрицательное", test_quantity_not_negative),
        ("Названия не пустые", test_names_not_empty),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        result = func()
        status = "✅" if result else "❌"
        if result:
            passed += 1
        print(f"{status} {name}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")


if __name__ == "__main__":
    run_all_tests()