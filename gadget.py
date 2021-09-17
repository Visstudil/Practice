SOUVENIR = 75
GADGET = 112

souvenir_count = int(input("Введте кол-во сувениров: "))
gadget_count = int(input("Введте кол-во безделушек: "))

total = souvenir_count * SOUVENIR + gadget_count * GADGET

print("Общая масса посылки: {0}г".format(total))