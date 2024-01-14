def n_busqueda(lista):
    lista = input('Introduce una lista de números separados por espacios: ')
    lista = lista.split(' ')
    lista = [int(i) for i in lista]
    n = int(input('Introduce un número: '))
    for i in lista:
        if i == n:
            if lista.count(i) == 1:
                return f'{i}: {lista.count(i)} vez'
            else:                
                return f'{i}: {lista.count(i)} veces'

if __name__ == '__main__':
    print(n_busqueda(lista))