


N = list(range(1, int(input())+1))
X = int(input())

def is_even(x):
    if x % 2 == 0:
        return True
    else:
        return False

print(N)
while N.index(X) != 0:
    if is_even(N.index(X)+1):
        print(1)
        temp = list(filter(lambda x: x % 2 == 0, list(range(1, len(N) + 1))))
        for i in range(1, len(temp)):
            if not i in temp:
                del N[i - 1]
        print(N, temp)
    else:
        print(2)
        temp = list(filter(lambda x: x % 2 != 0, list(range(1, len(N) + 1))))
        for i in range(1, len(temp)):
            if not i in temp:
                del N[i - 1]
        print(N, temp)
