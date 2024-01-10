import math

class Empty(Exception):
    pass

class Fraccion:

    def __init__(self, numerador, denominador):
        self.numerador = numerador
        self.denominador = denominador

        if self.denominador == 0:
            raise Empty('El denominador no puede ser 0')

    def __add__(self, other):
        numerador = self.numerador * other.denominador + other.numerador * self.denominador
        denominador = self.denominador * other.denominador
        return Fraccion(numerador, denominador)

    def __sub__(self, other):
        numerador = self.numerador * other.denominador - other.numerador * self.denominador
        denominador = self.denominador * other.denominador
        return Fraccion(numerador, denominador)

    def __mul__(self, other):
        numerador = self.numerador * other.numerador
        denominador = self.denominador * other.denominador
        return Fraccion(numerador, denominador)

    def __truediv__(self, other):
        numerador = self.numerador * other.denominador
        denominador = self.denominador * other.numerador
        return Fraccion(numerador, denominador)

    def __str__(self):
        return f'{self.numerador}/{self.denominador}'

    def __eq__(self, other):
        return self.numerador * other.denominador == other.numerador * self.denominador

    def __lt__(self, other):
        return self.numerador * other.denominador < other.numerador * self.denominador
    
    def __gt__(self, other):
        return self.numerador * other.denominador > other.numerador * self.denominador

    def __le__(self, other):
        return self.numerador * other.denominador <= other.numerador * self.denominador
    
    def __ge__(self, other):
        return self.numerador * other.denominador >= other.numerador * self.denominador

    def __ne__(self, other):
        return self.numerador * other.denominador != other.numerador * self.denominador

if __name__ == '__main__':
    fraccion1 = Fraccion(4, 5)
    fraccion2 = Fraccion(2, 6)
    print(fraccion1.__add__(fraccion2))
    fraccion3 = Fraccion(1, 2)
    fraccion4 = Fraccion(1, 2)
    fraccion5 = Fraccion(5, 4)
    print(fraccion3.__mul__(fraccion4).__sub__(fraccion5))
    fraccion6 = Fraccion(2, 3)
    fraccion7 = Fraccion(3, 4)
    print(fraccion6.__truediv__(fraccion7))
    print(fraccion1.__eq__(fraccion2))
    print(fraccion1.__lt__(fraccion4))
    print(fraccion2.__gt__(fraccion6))
    print(fraccion3.__le__(fraccion1))
    print(fraccion5.__ge__(fraccion2))
    print(fraccion2.__ne__(fraccion7))
