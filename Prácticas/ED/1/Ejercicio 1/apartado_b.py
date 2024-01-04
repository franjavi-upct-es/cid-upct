from apartado_a import Constructor

class Nuevo_Constructor(Constructor):
    def __init__(self, nombre, apellidos, edad, direccion):
        super().__init__(nombre, apellidos, edad)
        self.__direccion = direccion

    def describir_usuario(self):
        super().describir_usuario()
        print(f"\t Dirección: {self.__direccion}")

if __name__ == "__main__":
    Fran = Nuevo_Constructor("Francisco Javier", "Mercader Martínez", 19, "Calle Orellana, 22")
    Fran.describir_usuario()