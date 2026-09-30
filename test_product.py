"""Проверка класса Product."""
from models import Product

# Создаём один товар вручную
p = Product(
    product_id=1,
    ptype="Студия",
    adress="ул. Мира, 5",
    area=22,
    price=4_500_000,
    qty=4,
    photo="flat1.png"
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):,.2f} руб.")