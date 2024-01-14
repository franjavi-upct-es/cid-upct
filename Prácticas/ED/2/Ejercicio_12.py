def bisect(sorted_list, target):
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        guess = sorted_list[mid]
        if guess == target:
            return mid
        if guess > target:
            high = mid - 1
        else:
            low = mid + 1
    return "No se encontró la palabra"

if __name__ == '__main__':
    lista = ['adios', 'hola', 'prueba']
    print(bisect(lista, 'hola'))
    print(bisect(lista, 'no_existe'))