import math
class Segmento:
    def __init__(self,x1, y1, x2, y2):
        self.x1= x1
        self.x2= x2
        self.y1= y1
        self.y2= y2
    
    def longitud(self):
        return math.sqrt((self.x1-self.x2)**2 + (self.y1-self.y2)**2)

    def segmento(self):
        return [(self.x1, self.y1), (self.x2, self.y2)]
        
    def traslada(self, x_offset, y_offset):
        self.x1 += x_offset
        self.x2 += x_offset
        self.y1 += y_offset
        self.y2 += y_offset

class Forma:
    def __init__ (self,x,y):
        self.x = x
        self.y = y

    def perimetro(self): 
        raise NotImplementedError("No implementado")

    def traslada(self,x,y):
        self.x += x
        self.y += y
        return

class Poligono:
    def __init__ (self,segs):
        self._segs = segs

    def segmentos(self): 
        lista = []
        for s in self._segs:
            lista.append(s.segmento())
        return lista

    def traslada(self,x,y):
        for s in self._segs:
            s.traslada(x,y)
        
        """
        lista=[]
        for s in self._segs:
            lista.append((s[0]+x,s[1]+y))
        self._segs = lista
        """
class Circulo(Forma):
    pi = 3.141592
    def __init__ (self,x,y,radio):
        super().__init__(x,y)
        self.radio = radio

    def perimetro(self): 
        return 2*Circulo.pi*self.radio

class Rectangulo(Forma,Poligono):
    def __init__ (self,segs):
        assert len(segs) == 4
        # Forma.__init__(self,segs[0][0],segs[0][1])
        Forma.__init__(self, segs[0].x1, segs[0].y1)
        Poligono.__init__(self,segs)

        self.altura = segs[1].longitud()    # abs(segs[2][1]-segs[1][1])
        self.anchura = segs[0].longitud()   # abs(segs[0][0]-segs[1][0])

    def perimetro(self): 
        return 2*(self.altura+self.anchura)

    def traslada(self,x,y):
        Forma.traslada(self,x,y)
        Poligono.traslada(self,x,y)
        
class Chucrut: 
    def perimetro(self): 
        return "No tengo perímetro" 


if __name__ == "__main__":
    s1 = Segmento(2,2,6,2)
    s2 = Segmento(6,2,6,5)
    s3 = Segmento(6,5,2,5)
    s4 = Segmento(2,5,2,2)

    r = Rectangulo([s1, s2, s3, s4])
    print(r.segmentos())

    r.traslada(4,2)
    print(r.segmentos())