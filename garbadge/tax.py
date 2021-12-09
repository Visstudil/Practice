summ = float(input("Введите сумму заказа: "))

tax = summ * 0.04
tips = summ * 0.18
result = summ + tax + tips

print("Налог: ${:.2f}".format(tax))
print("Чаевые: ${:.2f}".format(tips))
print("Итог: ${:.2f}".format(result))