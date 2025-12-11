## 1. Imagen de un dado: segmentar los puntos (pips)

### 1.1. Método 1: Umbralización + Morfología Matemática

**Idea**

1. Pasar la imagen a escala de grises.
2. Umbralizar (Otsu) para separar fondo/objeto.
3. Invertir si hace falta para que los puntos sean 1 (True).
4. Limpiar con apertura/cierre.
5. Eliminar objetos pequeños.
6. Etiquetar componentes conectados → cada punto es un objeto.

**Código tipo examen (skimage):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage.morphology import binary_opening, binary_closing, disk
from skimage.measure import label, regionprops

# 1) Umbralización (Otsu)
th = threshold_otsu(dice_gray)
# como los puntos son oscuros:
binary = dice_gray < th     # True = puntos

# 2) Limpieza morfológica
selem = disk(2)  # tamaño ajustable según los puntos
binary_clean = binary_opening(binary, selem)     # eliminar ruido pequeño
binary_clean = binary_closing(binary_clean, selem)  # cerrar pequeños huecos

# 3) Etiquetado de componentes conectados
labels = label(binary_clean)

print(f"Número de puntos detectados: {labels.max()}")

# 4) Visualización rápida
fig, axes = plt.subplots(1, 3, figsize=(10, 4))
axes[0].imshow(dice_gray, cmap='gray'); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(binary_clean, cmap='gray'); axes[1].set_title('Binaria limpia'); axes[1].axis('off')
axes[2].imshow(labels, cmap='nipy_spectral'); axes[2].set_title('Componentes'); axes[2].axis('off')
plt.tight_layout(); plt.show()

# 5) Propiedades opcionales
for region in regionprops(labels):
    print("Área:", region.area, "Centroid:", region.centroid)
```

**Cómo lo explicas en el examen**

> “He segmentado los puntos aplicando umbralización de Otsu sobre la imagen en escala de grises y, después, operaciones morfológicas (apertura, cierre y eliminación de objetos pequeños) para limpiar la máscara binaria. Finalmente, he etiquetado los componentes conectados para obtener cada punto como un objeto separado.”

---

### 1.2. Método 2: Crecimiento de regiones (método de la semilla) + erosión/dilatación

Aquí es donde usas **semillas** y, tal y como te piden, **dilatación/erosión**:

**Idea general**

1. Umbralizar para obtener una máscara aproximada de los puntos.
2. Erosionar la máscara para obtener **semillas seguras** dentro de cada punto (morfología).
3. Aplicar un **crecimiento de regiones** desde esas semillas, añadiendo píxeles mientras sean parecidos a los de la semilla.

**Código tipo (hugely simplificado, estilo cuaderno):**

```python
import numpy as np
from skimage.morphology import binary_erosion, binary_dilation, disk
from skimage.measure import label

# Partimos de la binaria del apartado 1A (puntos = True)
mask = binary  # máscara: posibles puntos

# 1) Semilla por erosión: reduce los puntos
selem_seed = disk(2)  # ajusta según el tamaño de los puntos
seed = binary_erosion(mask, selem_seed)

# 2) Crecimiento por dilatación limitada por la máscara (reconstrucción morfológica manual)
grow = seed.copy()
selem_grow = disk(1)

while True:
    new = binary_dilation(grow, selem_grow) & mask  # dilata pero no sale de la máscara
    if np.array_equal(new, grow):
        break
    grow = new

pips_seed_method = grow

labels_seed = label(pips_seed_method)
print(f"Puntos detectados (método semilla): {labels_seed.max()}")

# Visualización
fig, axes = plt.subplots(1, 3, figsize=(10, 4))
axes[0].imshow(mask, cmap='gray'); axes[0].set_title('Máscara inicial'); axes[0].axis('off')
axes[1].imshow(seed, cmap='gray'); axes[1].set_title('Semilla (erosionada)'); axes[1].axis('off')
axes[2].imshow(labels_seed, cmap='nipy_spectral'); axes[2].set_title('Resultado crecimiento'); axes[2].axis('off')
plt.tight_layout(); plt.show()

```

**Cómo lo justificas**

> “Primero obtengo una máscara de los puntos por umbralización. Después, aplico una erosión morfológica para contraer las regiones y así obtener puntos interiores que sirven como semillas seguras. A partir de esas semillas implemento un algoritmo de crecimiento de regiones, añadiendo píxeles vecinos cuya intensidad sea similar a la de la semilla (por debajo de un umbral de diferencia). De ese modo, reconstruyo las regiones de cada punto.”

Si quieres meter también **dilatación**, puedes decir que dilatas la segmentación final para recuperar el tamaño original de los puntos si la erosión fue muy agresiva.

---

### 1.3. Método 3: Watershed a partir de marcadores (otro método de segmentación)

Es otro método de segmentación claro de los cuadernos.

**Idea**

1. Umbralizar para tener puntos como foreground.
2. Calcular la **transformada de distancia** de la máscara binaria de los puntos.
3. Obtener **máximos locales** como marcadores de cada punto.
4. Aplicar `watershed` para separar los puntos.

**Código tipo:**

```python
from skimage.filters import sobel
from skimage.segmentation import watershed
from scipy import ndimage as ndi

# 1) Mapa de elevación a partir del gradiente (Sobel)
elevation_map = sobel(dice_gray)

# 2) Marcadores: fondo y posible objeto según intensidad
markers = np.zeros_like(dice_gray, dtype=int)
markers[dice_gray > 0.8] = 1   # fondo (muy blanco)
markers[dice_gray < 0.4] = 2   # posibles puntos (oscuros)

# 3) Watershed
segmentation = watershed(elevation_map, markers)

# segmentación == 2 serían las regiones de "puntos"
pips_ws = segmentation == 2

# Limpieza opcional con morfología
pips_ws_clean = binary_opening(pips_ws, disk(1))

labels_ws = label(pips_ws_clean)
print(f"Puntos detectados (watershed): {labels_ws.max()}")

fig, axes = plt.subplots(1, 3, figsize=(10, 4))
axes[0].imshow(dice_gray, cmap='gray'); axes[0].set_title('Original'); axes[0].axis('off')
axes[1].imshow(elevation_map, cmap='gray'); axes[1].set_title('Mapa Sobel'); axes[1].axis('off')
axes[2].imshow(labels_ws, cmap='nipy_spectral'); axes[2].set_title('Puntos (WS)'); axes[2].axis('off')
plt.tight_layout(); plt.show()
```

**Cómo lo explicas**

> “Uso una segmentación por watershed a partir de marcadores: obtengo una máscara binaria de los puntos, calculo la transformada de distancia y localizo los máximos locales para definir marcadores de cada punto. Aplicando watershed sobre la imagen de distancia (negativa) obtengo regiones separadas para cada punto del dado.”

Con estos tres métodos estás cubriendo:

* Morfología matemática
* Método de la semilla (crecimiento de regiones con semillas obtenidas por erosión)
* Otro método de segmentación clásico: watershed con marcadores.

---

## 2. KMeans para clasificar píxeles y generar paletas de color

Te piden algo muy parecido a la **cuantización de colores** del cuaderno.

**Objetivo**

* Tratar cada píxel como un punto en 3D (R,G,B).
* Aplicar KMeans con distintos valores de `k`.
* Usar los centros de los clusters como **paleta de color**.
* Reconstruir la imagen reemplazando cada píxel por el centro de su cluster (paleta).

### 2.1. Código general

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage import img_as_float
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

# 1. Leer imagen y normalizar
img = imread('imagen_color.png')
img = img_as_float(img)

h, w, c = img.shape
pixels = img.reshape(-1, c)     # (N, 3) N = h*w

# Para entrenar más rápido, muestreamos una parte
pixels_sample = shuffle(pixels, random_state=0, n_samples=1000)

def quantize_with_k(k):
    # 2. Entrenar KMeans
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(pixels_sample)

    # 3. Predecir cluster de cada píxel
    labels = kmeans.predict(pixels)

    # 4. Centros de los clusters = paleta de colores
    palette = kmeans.cluster_centers_   # shape (k, 3)

    # 5. Reconstruir imagen usando sólo colores de la paleta
    img_quant = palette[labels].reshape(h, w, c)

    return img_quant, palette

# Probar con varios k
ks = [2, 4, 8, 16]
fig, axes = plt.subplots(1, len(ks) + 1, figsize=(15, 4))
axes[0].imshow(img); axes[0].set_title('Original'); axes[0].axis('off')

for i, k in enumerate(ks, start=1):
    img_k, palette_k = quantize_with_k(k)
    axes[i].imshow(img_k)
    axes[i].set_title(f'k = {k}')
    axes[i].axis('off')

plt.tight_layout(); plt.show()
```

### 2.2. Visualizar la paleta de colores (opcional, queda muy bien en examen)

```python
def show_palette(palette):
    k = palette.shape[0]
    # Creamos una imagen de tamaño k x 50 con cada fila un color
    pal_img = np.zeros((50, 50 * k, 3))
    for i, color in enumerate(palette):
        pal_img[:, i*50:(i+1)*50, :] = color
    plt.imshow(pal_img)
    plt.axis('off')

# Ejemplo para k=8
img_k, palette_k = quantize_with_k(8)
plt.figure(figsize=(8,4))
plt.subplot(1,2,1); plt.imshow(img_k); plt.title('Imagen cuantizada (k=8)'); plt.axis('off')
plt.subplot(1,2,2); show_palette(palette_k); plt.title('Paleta k=8')
plt.tight_layout(); plt.show()
```

### 2.3. Cómo lo explicas

> “Represento cada píxel de la imagen por sus componentes de color (R,G,B) y aplico KMeans para agrupar los píxeles en `k` clusters. Los centroides obtenidos son la paleta de color de tamaño `k`. A continuación, reconstruyo la imagen reemplazando cada píxel por el color de su centroide, generando versiones de la imagen con distintas paletas (para varios valores de `k`).”
