def ordenada(lista):
    for i in range(len(lista)-1):
        if lista[i] > lista[i+1]:
            return False
    return True

if __name__ == '__main__':
    lista = ['b', 'a', 'c', 'd']

    print(ordenada(lista))