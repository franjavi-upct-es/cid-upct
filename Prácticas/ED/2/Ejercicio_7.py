from collections import deque

def patata_caliente(niños):

    cola = deque(niños)
    
    print("Presiona Enter para pasar el item al siguiente niño ('p' para parar el juego): ")
    
    while len(cola) > 1:
        

        accion = input()

        if accion.lower() == "p":
            eliminado = cola.popleft()
            print(f"El niño {eliminado} ha sido eliminado")

        else:
            cola.rotate(-1)
    
    print(f"El niño {cola[0]} ha ganado la patata caliente")

if __name__ == "__main__":

    niños = ['niño1', 'niño2', 'niño3', 'niño4', 'niño5', 'niño6', 'niño7', 'niño8', 'niño9', 'niño10']

    patata_caliente(niños)
