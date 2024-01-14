class Exception(Exception):
    pass

def n_repetidos(lista, n):
    repetidos = {}
    if len(lista) > n:
        for item in lista:
            if lista.count(item) >= n:
                if item not in repetidos:
                    repetidos[item] = lista.count(item)
        return repetidos
    else: 
        raise Exception('Too short list')
    
if __name__ == '__main__':
    lista = ['a', 'b', 'a', 'a']
    print(n_repetidos(lista, 5))  