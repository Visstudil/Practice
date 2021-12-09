import os, pymorphy2, methods

morph = pymorphy2.MorphAnalyzer()
paths = ("D:\\Mefodii\\dishes.txt", "D:\\Mefodii\\ingredients.txt", "D:\\Mefodii\\out.txt")
ingredients = []
dishes = []
lines = []

# Existing check
for path in paths:
    methods.createifnotexist(os.path.dirname(path))
    methods.createifnotexist(path)
    
# Incline text in files 
methods.incline(paths[0], {"nomn"})
methods.incline(paths[1], {"gent"})

# UI
while True:
    ans = input("<Мефодий>Хотите что-то добавить?\n('Д' = Да; 'Н' = Нет)\n").upper()

    if ans == "Д":
        ans = input("<Мефодий>Энто будет ингредиент или блюдо?\n('И' = Ингредиент; 'Б' = Блюдо)\n").upper()
        w = morph.parse(input("<Мефодий>Тогда введи одно слово\n"))[0]

        if ans == "И":
            ingredients.append(w.inflect({"gent"}).word)
            with open(paths[1], "a") as i:
                i.write(ingredients[len(ingredients)-1] + "\n")

        elif ans == "Б":
            dishes.append(w.normal_form)
            with open(paths[0], "a") as d:
                d.write(dishes[len(dishes)-1] + "\n")

    elif ans == "Н":
        break

print("<Мефодий>Пока...")
lines = methods.formatstr(dishes, ingredients)

methods.appendlines(paths[2], lines)


os.system(r"explorer.exe {0}".format(paths[2]))  # Open out.txt