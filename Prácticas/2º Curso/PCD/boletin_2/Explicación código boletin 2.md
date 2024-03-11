# Zoo Management System

Este código es un sistema de gestión de un zoológico. El sistema permite manejar diferentes aspectos de un zoológico, incluyendo los animales, los cuidadores, la comida y el stock de comida.

## Clases

El sistema se compone de varias clases:

### EDieta

Esta es una enumeración que define las diferentes dietas que pueden tener los animales: Herbívoro, Carnívoro, Insectívoro y Omnívoro.

```python
class EDieta(Enum):
        HERBIVORO = 1
        CARNIVORO = 2
        INSECTIVORO = 3
        OMNIVORO = 4
```

### Comida

Esta clase representa la comida que se puede dar a los animales. Tiene un nombre y una dieta asociada.

```python
class Comida:
        
    def __init__ (self,nombre, dieta):
        self.nombre = nombre
        self.dieta = dieta
            
    def __str__(self):
        return "Comida: " + self.nombre + ", " + str(self.dieta)
```

### Stock

Esta clase gestiona el stock de comida del zoológico. Permite comprar comida, sacar comida del stock y obtener la cantidad de comida disponible.

```python
class Stock:
        
    def __init__ (self):
        self.stock = dict() # La cantidad de cada comida
        self.dietas = dict() # las comidas de cada dieta
        
    def compra(self, comida, cantidad):
        if comida.nombre in self.stock:
           self.stock[comida.nombre] += cantidad
        else:
           self.stock[comida.nombre] = cantidad
           if comida.dieta in self.dietas:
               self.dietas[comida.dieta].append(comida)
           else:
               self.dietas[comida.dieta] = list([comida])
```

### Animal

Esta clase representa a un animal en el zoológico. Cada animal tiene un id, una especie, una dieta y un cuidador asignado.

```python
class Animal:

    def __init__ (self, id, especie, dieta):
        self.id = id        
        self.especie=especie
        self.dieta = dieta
        self.cuidador = None         
```

### Vacaciones

Esta clase representa las vacaciones de un cuidador. Tiene un inicio y una duración.

```python
class Vacaciones:
       
    def __init__(self, inicio, duracion): 
        self.inicio=inicio
        self.duracion=duracion
```

### Cuidador

Esta clase representa a un cuidador en el zoológico. Cada cuidador tiene un nombre, apellidos, una lista de animales a su cargo y una lista de sus vacaciones.

```python
class Cuidador:
        
    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.animales = list()
        self.vacaciones = list()
```

### Zoo

Esta es la clase principal que representa al zoológico. Gestiona la contratación de cuidadores, la adquisición de animales y el stock de comida.

```python
class Zoo:
        
    def __init__(self):
        self.cuidadores = list()
        self.animales = list()
        self.stock = Stock()
        self.idCont = 0
```

## Ejemplo de uso

El código final en el archivo `Zoo.py` muestra un ejemplo de cómo usar estas clases para crear un zoológico, comprar comida, adquirir animales, contratar cuidadores y asignar animales a cuidadores.

```python
if __name__ == "__main__":

    # Creamos el objeto Zoo
    zoo = Zoo()

    # Creamos algunos alimentos
    carneVacuno = Comida("Vacuno", EDieta.CARNIVORO)
    carneCaza   = Comida("Caza",  EDieta.CARNIVORO)
    manzanas    = Comida("Manzanas", EDieta.HERBIVORO)
    platanos    = Comida("Platanos", EDieta.HERBIVORO)
    larvas      = Comida("Larvas", EDieta.INSECTIVORO)

    # El zoo compra cantidades de estos alimentos
    zoo.stock.compra(carneVacuno, 50)
    zoo.stock.compra(manzanas, 10)
    zoo.stock.compra(platanos, 10)
    zoo.stock.compra(larvas, 5)

    # El zoo adquiere algunos animales
    tigre = zoo.adquirir("Tigre", EDieta.CARNIVORO)
    leon = zoo.adquirir("Leon", EDieta.CARNIVORO)
    elefante = zoo.adquirir("Elefante", EDieta.HERBIVORO)
    hipopotamo = zoo.adquirir("Hipopotamo", EDieta.HERBIVORO)
    cebra = zoo.adquirir("Cebra", EDieta.HERBIVORO)
    cocodrilo = zoo.adquirir("Cocodrilo", EDieta.CARNIVORO)

    # El zoo contrata a algunos cuidadores
    juan = zoo.contratar("Juan", "Abellan Lopez")
    pepe = zoo.contratar("Pepe", "Garcia Sanchez")
    laura = zoo.contratar("Laura", "Perez Ramirez")

    # Asignar animales a cuidadores
    juan.asignarAnimal(tigre)
    juan.asignarAnimal(leon)
    pepe.asignarAnimal(elefante)
    pepe.asignarAnimal(cebra)
    laura.asignarAnimal(hipopotamo)
    laura.asignarAnimal(cocodrilo)

    # mostrar el estado actual del zoo
    
    print(str(zoo))
```