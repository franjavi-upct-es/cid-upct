from difflib import get_close_matches

def corrector(s, W):
    if s in W:
        print([s])
    else:
        correccion = get_close_matches(s, W)
        print(correccion[0])
    
if __name__ == '__main__':
    W = ['hola', 'fresa', 'cereza', 'banana']
    corrector('frosa', W)