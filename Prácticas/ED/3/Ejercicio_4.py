def crear_diccionario():
    entradas = input('Ingrese dos palabras en formato <palabra>:<traducción>, separadas por comas: ')
    traducciones = entradas.split(',') # separa las palabras
    diccionario = {}
    for par in traducciones:
        palabra, traduccion = par.split(':')
        diccionario[palabra.strip()] = traduccion.strip() # elimina los caracteres de inicio y final
    return diccionario

def traductor(diccionario):
    frase = input('Introduce una frase: ')
    palabras = frase.split()
    palabras_traducidas = [diccionario.get(palabra, palabra) for palabra in palabras]
    # "get" devuelve el valor de un elemento específico en un diccionario
    frase_traducida = ' '.join(palabras_traducidas)
    print(f"La frase traducida es: {frase_traducida}")
    
if __name__ == '__main__':
    
    diccionario = crear_diccionario()
    traductor(diccionario)
        