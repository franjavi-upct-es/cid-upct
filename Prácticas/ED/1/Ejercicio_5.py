class CustomException(Exception):
    pass

class Fecha:
    def __init__(self, dia, mes, año):
        self._dia = dia
        self._mes = mes
        self._año = año

    def is_correct(self):
        if self._mes < 1 or self._mes > 12:
            raise CustomException("El mes no es válido")
        if self._dia < 1 or self._dia > 31:
            raise CustomException("El día no es válido")
        if self._año < 0:
            raise CustomException("El año no es válido")
        if self._mes == 2 and self._dia > 28:
            raise CustomException("La fecha no es válida")
        if self._mes in [4, 6, 9, 11] and self._dia > 30:
            raise CustomException("La fecha no es válida")

    def __str__(self):
        self.is_correct()
        return f"{self._dia}/{self._mes}/{self._año}"

    def previous_day(self):
        self._dia -= 1
        if self._dia == 0:
            self._mes -= 1
            if self._mes == 0:
                self._año -= 1
                self._mes = 12
            if self._mes == 2:
                self._dia = 28
            if self._mes in [4, 6, 9, 11]:
                self._dia = 30
            else:
                self._dia = 31
            self.is_correct()
        return self.__str__()

    def next_day(self):
        self._dia += 1
        if self._dia == 32:
            self._mes += 1
            self._dia = 1
            if self._mes == 13:
                self._año += 1
                self._mes = 1
            if self._mes == 2:
                self._dia = 28
            if self._mes in [4, 6, 9, 11]:
                self._dia = 30
            self.is_correct()
        return self.__str__()


if __name__ == "__main__":
    fecha = Fecha(1, 1, 2000)
    print(fecha)
    print(fecha.previous_day())
    print(fecha.next_day())
    print(fecha.next_day())
    print(fecha.next_day())
    print(fecha.next_day())
    print(fecha.next_day())
