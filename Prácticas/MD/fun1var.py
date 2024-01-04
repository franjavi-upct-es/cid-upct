def f1(x):
    return 3 * x**2 + x - 1

# Definición de f2(x) = (2x + 1) / (x^2 + 1)
def f2(x):
    return (2 * x + 1) / (x**2 + 1)


def f3(x):
    if x <= 0:
        return 2 * x
    else:
        return x**2


def f4(x):
    if 0 < x <= -2:
        return (2 * x) / (x + 1)
    else:
        return x**2 + 3

def f5(x):
    if x <= 0:
        return 2 * x
    elif 0 < x < 2:
        return x**2
    else:
        return x**3 + 1


def f6(x):
    if x <= -1:
        return (2 * x + 1) / (x**2)
    elif 0 < x < 2:
        return x**2
    else:
        return 0