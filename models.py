"""Модели данных для проекта УП.02"""

from datetime import datetime
from discount import calculate_price_with_discount


class Product:
    """Класс Товар (объект недвижимости)."""

    def __init__(self, product_id, name, category, price, quantity, area=0):
        self.id = product_id
        self.name = name
        self.category = category 
        self.price = price
        self.quantity = quantity
        self.area = area 

    def total(self):
        """Общая стоимость."""
        return self.price * self.quantity

    def discounted_price(self):
        """Цена со скидкой 25% (упрощённо)."""
        return self.price * 0.75   # итоговое значение

    def price_with_discount_auto(self, date=None):
        """Цена со скидкой по алгоритму ДЭ (5% при площади > 100)."""
        if date is None:
            date = datetime.now()
        return calculate_price_with_discount(self.id, self.price, date)

    def indicator(self):
        """Индикатор наличия."""
        return "много" if self.quantity > 5 else "мало"
    
    def is_available(self):
        """Товар доступен для заказа?"""
        return self.quantity > 0
    
    def order_info(self):
        return f"Заказ №{self.id} от {self.date}: {self.client}"

    def info(self):
        """Информация о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"(площадь: {self.area} кв.м)"
        )

    
if __name__ == "__main__":
    p = Product(6, "Пентхаус", "ул. Речная, 1", 32000000, 1, area=140)
    print(f"Базовая цена: {p.price}")
    print(f"Со скидкой: {p.price_with_discount_auto()}")