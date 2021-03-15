class Calculator:  # 基本都考虑 80分
    def add_way(self, n: int, m: int):
        sum = (n + m) * (m - n + 1) / 2
        return sum


def add_way1(n: int, m: int):  # 未考虑部分可扩展性 70分
    sum = (n + m) * (m - n + 1) / 2
    return sum


def add_way2(n: int, m: int):  # 未考虑高效，以及考虑部分可扩展性 50分
    i = n
    sum = 0
    while i <= m:
        sum += i
        i += 1
    return sum


def add_way3(n, m):  # 未复用性以及可扩展性 40分
    sum = sum(n, m)
    return sum


def add_way4():  # 未考虑高效，复用性以及可扩展性 10分
    sum = 0
    i = 1
    while i <= 100:
        sum += i
        i += 1
    print(sum)
    return sum
