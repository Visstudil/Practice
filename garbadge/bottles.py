S_COST = 0.10
L_COST = 0.25

s_count = input("Количество литровых бутылок: ")
l_count = input("Количество бутылок побольше: ")
summ = float(s_count) * S_COST + float(l_count) * L_COST

print("Сумма: ${:.2f}".format(summ))