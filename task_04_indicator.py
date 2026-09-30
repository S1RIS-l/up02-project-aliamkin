catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2},
]
many = []
few = []

for product in catalog:
    if product["qty"] > 5:
        many.append(product)
    else:
        few.append(product)
print("Каталог с индикатором:")
i = 1

for product in many:
    print(f"{i}. {product['name']} - {product['qty']} шт. - много")
    i += 1
for product in few:
    print(f"{i}. {product['name']} - {product['qty']} шт. - мало")
    i += 1