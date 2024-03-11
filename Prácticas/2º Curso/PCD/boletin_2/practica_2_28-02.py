from enum import Enum
from datetime import date

class EDieta(Enum):
    CARNIVORO = 1
    HERBIVORO = 2
    OMNIVORO = 3

class Comida:
    def __init__(self, nombre:str, dietas:list(EDieta)):
        self._nombre = nombre
        self._dietas = dietas
    

    def __str__(self) -> str:
        return f"{self._nombre} son parte de la dieta de los animales {self._dietas}"

class Stock:
    def __init__(self) -> None:
        self.dict = {}

    def comprar(self, comida: Comida, cantidad: int) -> None:
        pass

    def sacar(self, comida:Comida, cantidad:int) -> None:
        pass

class Vacaciones(Cuidador):
    def __init__(self, inicio:date, duracion:int, empleado:str):
        self._inicio = inicio
        self._duracion = duracion
        self._empleado = empleado

class Cuidador:
    def __init__(self, nombre:str, apellido:str, animales):
        self._nombre = nombre
        self._apellido = apellido
        self._animales = []
        self._vaciones = []

    def listaAnimales(self):
        return self._animales

    def asignarAnimal(slef, animal):
        if animal.tieneCuidador():
            animal.suCuidador().quitarAnimal(animal)

        self.animales.append(animal)
        animal.asignarCuidador(self)

    def quitarAnimal(self, animal):
        self._animales.remove(animal)

    def solicitar_vacaciones(self, inicio:date, duracion:int):
        v = Vacaciones(inicio, duracion)
        self.vacaciones.append(v)
        print(f'{self.nombre} ha solicitado vacaciones desde {inicio} hasta {fin}.')

class Animal:
    def __init__(self, id:int, dieta:EDieta, especie:str, cuidador_actual:str):
        self._id = id
        self._dieta = Comida.dietas
        self._especie = especie
        self._cuidador = cuidador_actual
    
c1 = Comida("manzana", [EDieta.HERBIVORO])

s = Stock()

s.comprar(c1, 50)