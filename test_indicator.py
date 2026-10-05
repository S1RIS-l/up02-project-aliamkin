"""Тестирование индикатора «много/мало» (вариант 16)."""

from catalog import _indicator


def test_indicator():
    """Прогон базовых тестов для индикатора."""
    test_cases = [
        (10, "много", "10 > 5"),
        (6, "много", "6 > 5"),
        (5, "мало", "5 ≤ 5 (граница!)"),
        (4, "мало", "4 ≤ 5"),
        (0, "мало", "0 ≤ 5"),

        (100, "много", "большое число"),
        (1, "мало", "минимальное > 0"),
        (-1, "мало", "отрицательное (крайний случай)"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ИНДИКАТОРА")
    print("=" * 60)

    passed = 0
    for qty, expected, comment in test_cases:
        result = _indicator(qty)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} qty={qty}: {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")
    print("=" * 60)


def test_indicator_edge_cases():
    """Проверяет поведение _indicator на некорректных данных (ДЗ).

    Цель: убедиться, что функция не падает с необработанным исключением
    или корректно обрабатывает «плохие» данные.
    """
    edge_cases = [
        (None, "мало", "_indicator(None) — None не сравнивается с 5"),
        ("10", "мало", "_indicator('10') — строка вместо числа"),
        (0.5, "мало", "_indicator(0.5) — дробное число"),
    ]

    print()
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КРАЙНИХ СЛУЧАЕВ ИНДИКАТОРА")
    print("=" * 60)

    for qty, expected, comment in edge_cases:
        try:
            result = _indicator(qty)
            status = "✅" if result == expected else "⚠️"
            print(f"{status} _indicator({qty!r}) = {result!r} "
                  f"(ожидалось {expected!r}) — {comment}")
        except Exception as e:
            print(f"❌ _indicator({qty!r}) бросил исключение: "
                  f"{type(e).__name__}: {e} — {comment}")

    print("=" * 60)


if __name__ == "__main__":
    test_indicator()
    test_indicator_edge_cases()