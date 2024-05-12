from enum import Enum

# UML de Zoológico

class TipoAlimentacion(Enum):
    CARNIVORO = 1
    HERBIVORO = 2
    INSECTIVORO = 3

class Cuidador:
    
    lista_cuidadores = {}
    
    def __init__(self, nombre, dni):
        self.nombre = nombre
        self.dni = dni
        Cuidador.lista_cuidadores[dni] = self

    def cuidador_de_vacaciones(self, dni):
        # Verificamos si el dni está en el diccionario antes de eliminarlo
        if dni in Cuidador.lista_cuidadores:
            del Cuidador.lista_cuidadores[dni]
        else:
            raise ValueError("DNI no coincide")


class Animal(TipoAlimentacion, Cuidador):
    def __init__(self, nombre, id, alimentacion, cuidador):
        self.nombre = nombre
        self.__id = id
        self.alimentacion = int(TipoAlimentacion)
        self.cuidador = Cuidador

def Vacaciones(Cuidador):
    def __init__(self, dni):
        Cuidador.__init__(dni)
