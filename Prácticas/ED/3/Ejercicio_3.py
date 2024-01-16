from difflib import SequenceMatcher

def corrector(s, W):
    
    W = set(W)
    
    resultados = []
    parecido = 0.6
    
    if s in W:
        print(f"{[s]} es correcta")
    else:
        for palabra in W:
            similitud = SequenceMatcher(None, s, palabra).ratio()
            if similitud >= parecido:
                resultados.append(palabra)
        print(f"Palabra a corregir: {s}")
        print(f"Sugerencias: {resultados}")
            
if __name__ == '__main__':
    
    W = ['manzana', 'banana', 'cereza', 'dulce', 'fruta', 'golosina']
    
    corrector('manana', W)
    corrector('cereza', W)