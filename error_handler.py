"""Обработчик ошибок для проекта"""

from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """
    Безопасный вызов функции с обработкой исключений.

    :param func: вызываемая функция
    :param args: позиционные аргументы
    :param kwargs: именованные аргументы
    :return: результат func или None при ошибке
    """
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Файл не найден", f"{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка подключения", f"{e}")
    except ValueError as e:
        messagebox.showwarning("Некорректное значение", f"{e}")
    except Exception as e:
        messagebox.showerror("Неизвестная ошибка",
                             f"{type(e).__name__}: {e}")
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число.

    :param value: строка для проверки
    :param field_name: название поля
    :return: (True, число) или (False, сообщение)
    """
    try:
        number = int(value)
    except (ValueError, TypeError):
        return (False, f"{field_name} должно быть целым числом")
    if number <= 0:
        return (False, f"{field_name} должно быть больше нуля")
    return (True, number)