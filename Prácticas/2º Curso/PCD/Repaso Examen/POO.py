from enum import Enum
from datetime import date
from typing import List, Dict

class EDieta(Enum):
    HERBIVORO = 1
    CARNIVORO = 2
    INSECTIVORO = 3

class Cuidador:
    def __init__(self, nombre: str, apellido: str, animales: List[Animal]):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__animales = animales

    def solicitar_vacaciones(self, inicio: date, duracion: int):
        pass

    def cuidador(self, animal: Animal):
        pass

    def alimentar(self, animal: Animal):
        pass

class Animal:
    def __init__(self, id: int, dieta: EDieta, especie: str, cuidador_actual: Cuidador):
        self.__id = id
        self.__dieta = dieta
        self.__especie = especie
        self.__cuidador_actual = cuidador_actual

class Comida:
    def __init__(self, dietas: List[EDieta]):
        self.__dietas = dietas

class Stock:
    def __init__(self, stocks: Dict[Comida, int]):
        self.__stocks = stocks

    def sacar(self, comida: Comida, cantidad: int):
        if self.stocks[comida] >= cantidad:
            self.stocks[comida] -= cantidad
        else: 
            raise ValueError("No hay suficiente comida en el stock")

class Vacaciones:
    def __init__(self, inicio: date, duracion: int, empleado: Cuidador):
        self.__inicio = inicio
        self.__duracion = duracion
        self.__empleado = empleado


class Zoo:
    def __inti__(self, cuidadores: List[Cuidador], animales: List[Animal], stock: Stock):
        self.__cuidadores = cuidadores
        self.__animales = animales
        self.__stock = Stock

    def cuidar(self, cuidador: Cuidador, animal: Animal):
        pass

    def coger_vaciones(self, cuidador: Cuidador, inicio: date, duracion: int):
        pass