"""Обработчик ошибок для проекта УП.02."""

from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """Безопасный вызов функции."""
    try:
        return func(*args, **kwargs)

    except FileNotFoundError as e:
        messagebox.showerror(
            "Файл не найден",
            f"Не удалось открыть файл:\n{e}"
        )

    except ConnectionError as e:
        messagebox.showerror(
            "Ошибка подключения",
            f"Нет соединения:\n{e}"
        )

    except ValueError as e:
        messagebox.showwarning(
            "Некорректное значение",
            f"Проверьте ввод:\n{e}"
        )

    except Exception as e:
        messagebox.showerror(
            "Неизвестная ошибка",
            f"{type(e).__name__}: {e}"
        )

    return None


def validate_positive_int(value, field_name="Значение"):
    """Проверяет, что значение — положительное целое число."""
    try:
        number = int(value)

        if number <= 0:
            return (False, f"{field_name} должно быть больше нуля")

        return (True, number)

    except (ValueError, TypeError):
        return (False, f"{field_name} должно быть целым числом")


if __name__ == "__main__":
    print(validate_positive_int("5", "Количество"))
    print(validate_positive_int("-1", "Количество")) 
    print(validate_positive_int("abc", "Количество"))