"Ejemplo de un carrito de la compra para un supermercado"

from enum import Enum
import random

class DireccionPostal:
    def _init_(self, nombre_calle, numero, piso, puerta, codigo_postal):
        self.nombre_calle = nombre_calle
        self.numero = numero
        self.puerta = puerta
        self.codigo_postal = codigo_postal
        self.piso = piso

class Entidad:   # PODRÍA REALIZARSE DE MANERA ABSTRACTA ESTA CLASE
    def _init_(self, nombre, direccion):
        self.nombre = nombre
        self.direccion = direccion

    def actualizar(self, nuevo_nombre, nueva_direccion): # MÉTODO DE CLASE ENTIDAD
        if nuevo_nombre is not None:
            self.nombre= nuevo_nombre
        
        if nueva_direccion is not None:
            self.direccion = nueva_direccion

########################################################################################

class Cliente(Entidad):
    def _init_(self, nombre, direccion, nif):
        super()._init_(self,nombre,direccion)
        self.nif = nif



class Proveedor(Entidad):
    def _init_(self, nombre, direccion, cif): # NO PONEMOS ORDENES COMO PARÁMETRO PORQUE ES PRIVADO
        super()._init_(self,nombre,direccion)
        self.cif = cif
        self._ordenes = set()

# MÉTODOS DE PROVEEDOR:
    def ordenCompra(self, producto):
        self._ordenes.add(producto)
        return f"Añadido producto: {producto.nombre}"
    
    def hacerPedido(self):
        for o in self._ordenes:
            n_pro = random.randint(1, 100)
            return f"Pedido realizado de {n_pro} de {o.nombre}."
        


class PropiedadProducto(Enum):
    FRESCO = 1
    REFRIGERADO = 2
    CONGELADO = 3
    CONSERVA = 4


class Producto:
    def __init__(self, nombre, propiedades, proveedor, precio):
        self.nombre = nombre
        self.propiedades = propiedades
        self.proveedor = proveedor

        # EXCEPCIÓN PARA TRATAR ERRORES POSIBLES, EN ESTA CASO ERROR DE VALOR
        if precio < 0:
            raise ValueError(f"Un producto no puede tener precio menor que 0 ({precio})")
        self.precio = precio


class Almacen:
    def __init__(self, nombre, ubicacion, productos, cantidades, proveedor):    
        # productos = [p1, p2, p3, p4], cantidades = [c1, c2, c3, c4] es raro hacerlo así, mejor hacer un diccionario con
        # productos como claves y cantidades como valores
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.proveedor = proveedor  
        
        # AMBAS EXCEPCIONES SERÍAN VÁLIDAS Y TRATAN EL MISMO ERROR:
        #if len(productos) != len(cantidades):
        #    raise ValueError(f"El listado de productos y cantidades debe ser igual ({len(productos)} != {len(cantidades)})")
        assert len(productos) == len(cantidades) 

        self._productos = productos
        self._cantidades = cantidades

        nombres_productos = [p.nombre for p in self._productos] # Genero una lista con cada uno de los nombres de los productos de self._productos

        self.stock = {pro:cant for pro,cant in zip(nombres_productos,self._cantidades)} 
        # Genero un diccionario con cada uno de los nombres de los productos de nombres_productos asociado a su cantidad correspondiente de stock

    # MÉTODO DE LA CLASE ALMACEN:
    def descontarStock(self,producto, cantidad_a_descontar=1):
        n = producto.nombre
        if n in self.stock:
            self.stock[n] = self.stock[n] - cantidad_a_descontar
        
        if self.stock[n] <= 0:
            self.proveedor.ordenCompra(producto)
        return print(f"Descontamos del stock una cantidad {cantidad_a_descontar} de {producto}")

    

    

    class Cesta:
        def __init__(self):
            self.cliente = None
            self.productos = set()
            self.total = 0
            self._contenido = {}
            self._pagada = False

        # MÉTODOS CESTA:
        def iniciar(self, cliente):
            self.cliente = cliente

        def añadirProducto(self, producto, cantidad):
            self.productos.add(producto)
            cantidad_producto = self._contenido.get(producto.nombre, 0)
            cantidad_producto = cantidad_producto + cantidad
            self._contenido[producto.nombre] = cantidad_producto
            self.total += (cantidad * producto.precio)

            self.almacen.descontarStock(producto, cantidad)
            return print(f"Se ha añadido una cantidad de {cantidad} de {producto}")

        def pagar(self):
            self._pagada = True