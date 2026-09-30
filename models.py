"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар (объект недвижимости)."""

    def __init__(self, product_id, ptype, adress, area, price, qty, photo):
        """
        Инициализация товара.
        :param product_id: идентификатор
        :param тип: тип жилья
        :param адрес: адрес
        :param площадь: площадь, м²
        :param цена: цена, руб.
        :param количество: количество объектов
        :param фото: имя файла изображения
        """
        self.id = product_id
        self.ptype = ptype
        self.adress = adress
        self.area = area
        self.price = price
        self.qty = qty
        self.photo = photo

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.qty

    def price_with_discount(self, discount):
        """Цена со скидкой в процентах."""
        return self.price * (1 - discount / 100)

    def indicator(self):
        """«много» или «мало» (порог 5)."""
        return "много" if self.qty >= 5 else "мало"

    def info(self):
        """Строка с информацией о товаре."""
        return (f"{self.ptype} ({self.adress}): {self.price} руб. × "
                f"{self.qty} = {self.total()} руб. "
                f"({self.indicator()})")