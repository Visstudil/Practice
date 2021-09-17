import random

dishes = []
ingredients = []
bundle = "из"

while True:
    input_string = input("[Мефодий] Введите название блюда: ")
    if input_string != "выход":
        dishes.append(input_string)
    else:
        break
    print("[Мефодий] Можете выбрать еще; чтобы выйти, введите 'выход'")

while True:
    input_string2 = input("[Мефодий] Введите название ингредиента в РОДИТЕЛЬНОМ падеже: ")
    if input_string2 != "выход":
        ingredients.append(input_string2)
    else:
        break
    print("[Мефодий] Можете выбрать еще; чтобы выйти, введите 'выход'")

for dish in dishes:
    for ingredient in ingredients:
        print("{0} {1} {2};".format(dish, bundle, ingredient))