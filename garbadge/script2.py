A = int(input())
B = int(input())
C = int(input())
days = int(input())
first = int(input())
hotcakes = [A, B, C]

summ = 0
for i in range(0, days):
    hotcake = (i + first - 1) % 3
    summ += hotcakes[hotcake]
print(summ)