"""Модели данных для проекта УП.02"""

from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (объект недвижимости)."""

    def __init__(self, product_id, ptype, address, area, price,
                 quantity, photo=None):
        """
        :param product_id: id
        :param ptype: тип (Студия, Пентхаус, …)
        :param address: адрес
        :param area: площадь, кв.м
        :param price: цена
        :param quantity: количество
        :param photo: имя файла изображения
        """
        self.id = product_id
        self.ptype = ptype          # ← добавили, чтобы совпадало с db_products
        self.address = address
        self.area = area
        self.price = price
        self.quantity = quantity
        self.photo = photo

    def total(self):
        """Общая стоимость."""
        return self.price * self.quantity

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой 5% при площади > 100."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        """Индикатор наличия: много/мало."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """Товар доступен для заказа?"""
        return self.quantity > 0

    def info(self):
        """Информация о товаре."""
        return (
            f"{self.ptype} ({self.address}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"(площадь: {self.area} кв.м)"
        )


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product_id, quantity):
        self.id = order_id
        self.date = date
        self.client = client
        self.product_id = product_id
        self.quantity = quantity

    def order_info(self):
        return f"Заказ №{self.id} от {self.date}: {self.client}"