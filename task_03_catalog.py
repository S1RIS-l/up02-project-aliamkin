catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2},
]

print("Каталог товаров:")
summa = 0
for i, product in enumerate(catalog, start=1):
    cost = product["price"] * product["qty"]
    summa += cost
    print(f"{i}. {product['name']} – {product['price']} × {product['qty']} = {cost} руб.")
print(f"Итого: {summa} руб.")