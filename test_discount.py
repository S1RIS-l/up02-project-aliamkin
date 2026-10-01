"""Тестирование алгоритма скидки
Условие: скидка 5% при площади > 100 кв.м"""

from discount import calculate_price_with_discount



def run_tests():
    """Запуск тестов алгоритма расчёта скидки."""

    test_cases = [
        (1, 4500000, 4500000, "Студия 22 кв.м — скидки нет"),
        (2, 6500000, 6500000, "1-комн. 33 кв.м — скидки нет"),
        (3, 9500000, 9500000, "2-комн. 52 кв.м — скидки нет"),
        (4, 14000000, 14000000, "3-комн. 70 кв.м — скидки нет"),
        (5, 18000000, 18000000, "4-комн. 90 кв.м — скидки нет"),
        (6, 32000000, 30400000, "Пентхаус 140 кв.м — скидка 5%"),
        (7, 8000000, 8000000, "Апартаменты 40 кв.м — скидки нет"),

        (6, 32000000, 30400000, "Пентхаус — повтор"),
        (6, 100000000, 95000000, "Цена 100 млн — скидка 5%"),
        (8, 0, 0, "Цена 0 руб. — результат 0"),
    ]

    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("Условие: скидка 5% при площади > 100 кв.м")
    print("=" * 70)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(
            f"{status} Товар {product_id}: {price} → {result} "
            f"(ожидалось {expected}) — {comment}"
        )

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")

    print_test_report(passed, len(test_cases))

def print_test_report(passed, total):
    """Выводит отчёт о тестировании."""
    print("=" * 40)
    print("ОТЧЁТ О ТЕСТИРОВАНИИ")
    print(f"Пройдено: {passed} / {total}")
    if passed == total:
        print("Результат: ✅ УСПЕХ")
    else:
        print("Результат: ❌ ЕСТЬ ОШИБКИ")
    print("=" * 40)


if __name__ == "__main__":
    run_tests()