class Constructor:
    def __init__(self, nombre, apellidos, edad):
        self.__nombre = nombre
        self.__apellidos = apellidos
        self.__edad = edad

    def describir_usuario(self):
        print("USUARIO")
        print("\t Nombre: " + self.__nombre)
        print("\t Apellidos: " + self.__apellidos)
        print(f"\t Edad: {self.__edad}")

    def saluda_usuario(self):
        print( f"Hola {self.__nombre}")

    def incrementar_edad(self):
        self.__edad += 1

if __name__=="__main__":
    constructor = Constructor("Antonio", "Gutiérrez Mercader", 49)
    constructor.describir_usuario()
    constructor.saluda_usuario()
    constructor.incrementar_edad()
    constructor.describir_usuario()