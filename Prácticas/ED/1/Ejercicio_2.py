class Empresa():
    def __init__(self, nombre, cif, facturacion, año_creacion, empleados):
        self._nombre = nombre
        self._cif = cif
        self._facturacion = facturacion
        self._año_creacion = año_creacion
        self._empleados = empleados 

    def __str__(self):
        return f'Nombre: {self._nombre}\nCIF: {self._cif}\nFacturacion: {self._facturacion}\nAño de creacion: {self._año_creacion}\nEmpleados: {self._empleados}\n'

    def mod_facturacion(self, e):
        self._facturacion = e

    def mod_empleados(self, e):
        self._empleados += e

if __name__ == "__main__":
    empresa = Empresa("Merpiel S.L", "12345678A", 100000, 2000, 10)
    print(empresa)
    for i in range(5):
        empresa.mod_empleados(i+1)
        print(f'{empresa}')

        