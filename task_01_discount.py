price = float(input("Введите цену: "))
discount = float(input("Введите цену (%): "))
discount_price = price * (1 - discount / 100)
print(f"Цена со скидкой: {discount_price:.2f} руб.")