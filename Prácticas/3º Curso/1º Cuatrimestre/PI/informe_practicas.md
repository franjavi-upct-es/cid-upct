---
title: 1. Sesión 07 – Bordes, formas y umbralización
jupyter: python3
---


### 1.1 Filtros de borde por gradiente (Prewitt, Roberts, Sobel, Scharr, Laplaciano)

**Qué hacen**

Aproximan derivadas de la imagen para resaltar cambios bruscos de intensidad (bordes).

**Código (skimage.filters):**


```python
from skimage.io import imread
from skimage import filters
import numpy as np
import matplotlib.pyplot as plt

image = imread('./Práctica 7/images/goldengate.jpg', as_gray=True)

edges_prewitt   = filters.prewitt(image)
edges_roberts   = filters.roberts(image)
edges_sobel     = filters.sobel(image)
edges_scharr    = filters.scharr(image)
edges_laplacian = filters.laplace(image)

plt.figure(figsize=(15, 8))
plt.subplot(2, 3, 1); plt.imshow(image, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(2, 3, 2); plt.imshow(edges_prewitt, cmap='gray'); plt.title('Prewitt'); plt.axis('off')
plt.subplot(2, 3, 3); plt.imshow(edges_roberts, cmap='gray'); plt.title('Roberts'); plt.axis('off')
plt.subplot(2, 3, 4); plt.imshow(edges_sobel, cmap='gray'); plt.title('Sobel'); plt.axis('off')
plt.subplot(2, 3, 5); plt.imshow(edges_scharr, cmap='gray'); plt.title('Scharr'); plt.axis('off')
plt.subplot(2, 3, 6); plt.imshow(np.clip(edges_laplacian, 0, 1), cmap='gray'); plt.title('Laplaciano'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Si te piden “comparar detectores de bordes” o “ver cómo cambian los bordes con distintos filtros”.
* Para **resaltar contornos** previos a segmentación.
* Sobel/Scharr → más robustos; Laplaciano → detecta bordes en todas direcciones pero más sensible al ruido.

---

### 1.2 LoG y DoG (Laplaciano de Gauss / Diferencia de Gauss)

**Qué hacen**

* Suavizan con Gauss y luego derivan (LoG) o restan dos suavizados (DoG) para detectar **bordes y blobs** a cierta escala.

**Código (LoG + DoG):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.filters import gaussian
from scipy.ndimage import gaussian_laplace

image = imread('./Práctica 7/images/zebra.png', as_gray=True)

sigma_log = 3
log = gaussian_laplace(image, sigma=sigma_log)

sigma1 = 3*np.sqrt(2)
sigma2 = 3/np.sqrt(2)
dog = gaussian(image, sigma1) - gaussian(image, sigma2)

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1); plt.imshow(image, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1, 3, 2); plt.imshow(log, cmap='gray');   plt.title('LoG'); plt.axis('off')
plt.subplot(1, 3, 3); plt.imshow(dog, cmap='gray');   plt.title('DoG'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Cuando te pidan **bordes a una cierta escala** o detección de manchas/blobs.
* Si el ejercicio habla de “bordes de interés”, “estructuras a cierta escala” o “realce de detalles”.

---

### 1.3 Detector de Canny

**Qué hace**

Detector de bordes multietapa: suaviza, calcula gradiente, hace supresión de no-máximos y umbralizado con histéresis.

**Código (skimage.feature.canny):**

```python
from skimage.io import imread
from skimage import feature
import numpy as np
import matplotlib.pyplot as plt

im = imread('./Práctica 7/images/tiger.jpg', as_gray=True)
im2 = im + 0.5*np.random.random(im.shape)  # con ruido

edges1 = feature.canny(im,  sigma=1, low_threshold=0.4, high_threshold=0.8)
edges2 = feature.canny(im2, sigma=2, low_threshold=0.3, high_threshold=0.6)

plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1); plt.imshow(im, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1, 3, 2); plt.imshow(edges1, cmap='gray'); plt.title('Canny limpio'); plt.axis('off')
plt.subplot(1, 3, 3); plt.imshow(edges2, cmap='gray'); plt.title('Canny con ruido'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Si el enunciado dice “usar Canny” (obvio) o “detector de bordes robusto al ruido”.
* Antes de hacer segmentación por bordes o watershed.

---

### 1.4 Transformada de Hough (líneas y círculos)

**Qué hace**

Detecta **líneas rectas** y **círculos** a partir de una imagen binaria (normalmente de bordes).

**Código (líneas y círculos):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.color import gray2rgb
from skimage.transform import hough_line, hough_line_peaks, hough_circle, hough_circle_peaks
from skimage.draw import circle_perimeter

image = imread('./Práctica 7/images/triangle_circle.png', as_gray=True)

h, theta, d = hough_line(image, theta=np.linspace(-np.pi, np.pi, 180))
fig, axes = plt.subplots(2, 2, figsize=(8, 8))
ax = axes.ravel()

ax[0].imshow(image, cmap='gray'); ax[0].set_title('Imagen'); ax[0].axis('off')

# líneas
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
    ax[1].plot((0, image.shape[1]), (y0, y1), '-r')
ax[1].imshow(image, cmap='gray'); ax[1].set_title('Líneas Hough'); ax[1].axis('off')

# círculos
image_rgb = gray2rgb(image)
radii = np.arange(20, 50, 2)
hough_res = hough_circle(image, radii)
accums, cx, cy, radii_found = hough_circle_peaks(hough_res, radii, total_num_peaks=3)
for center_y, center_x, radius in zip(cy, cx, radii_found):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    image_rgb[circy, circx] = (220, 20, 20)

ax[2].imshow(image_rgb); ax[2].set_title('Círculos Hough'); ax[2].axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Ejercicios tipo “detecta líneas”, “detecta círculos” (p.ej. **detectar monedas** o **pelotas**).
* Cuando la forma es paramétrica (líneas rectas, círculos) y los bordes ya están detectados.

---

### 1.5 Umbralización global y Otsu

**Qué hace**

Convierte a binario:

* Global: un umbral fijo.
* Otsu: calcula automáticamente el umbral que maximiza la separabilidad de clases.

**Código (threshold_otsu):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray

image = rgb2gray(imread('./Práctica 7/images/horse.jpg'))
threshold_value = threshold_otsu(image)
binary_image = image > threshold_value

plt.figure(figsize=(8,4))
plt.subplot(1,2,1); plt.imshow(image, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(binary_image, cmap='gray'); plt.title('Otsu'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Cuando te piden “segmentar objeto/fondo” con **un solo umbral**.
* Para iniciar binarización antes de morfología (e.g. detectar sombras, siluetas).

---

## 2. Sesión 08 – Segmentación (bordes, regiones, clustering, movimiento)

### 2.1 Segmentación basada en bordes

**Idea**

Usar bordes (p.ej. Canny) para separar regiones, rellenando contornos cerrados.

**Ejemplo típico (monedas con Canny + relleno):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.feature import canny
from scipy import ndimage as ndi

coins = data.coins()
coins = coins / 255.0

edges = canny(coins, sigma=1)

# Rellenar contornos cerrados
fill_coins = ndi.binary_fill_holes(edges)

plt.figure(figsize=(9,4))
plt.subplot(1,3,1); plt.imshow(coins, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1,3,2); plt.imshow(edges, cmap='gray'); plt.title('Bordes'); plt.axis('off')
plt.subplot(1,3,3); plt.imshow(fill_coins, cmap='gray'); plt.title('Regiones'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Cuando los objetos tienen contornos claros y cerrados (aves, coches, monedas).

---

### 2.2 Crecimiento de regiones

**Qué hace**

Eliges una **semilla** y vas añadiendo píxeles vecinos mientras la diferencia de intensidad sea menor que un umbral.

**Código (simplificado del cuaderno):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, color
from scipy import ndimage as ndi

coins = data.coins()
coins = coins / 255.0
segmentation = np.zeros_like(coins)

seed = (50, 50)         # coordenadas (fila, columna)
threshold = 0.1
to_process = [seed]
segmentation[seed] = 1

def get_neighbors(x, y, shape):
    for nx in [x-1, x, x+1]:
        for ny in [y-1, y, y+1]:
            if 0 <= nx < shape[0] and 0 <= ny < shape[1] and not (nx == x and ny == y):
                yield nx, ny

while to_process:
    x, y = to_process.pop()
    for nx, ny in get_neighbors(x, y, coins.shape):
        if segmentation[nx, ny] == 0 and abs(coins[nx, ny] - coins[x, y]) < threshold:
            segmentation[nx, ny] = 1
            to_process.append((nx, ny))

segmentation = ndi.median_filter(segmentation, size=5)

plt.figure(figsize=(8,4))
plt.subplot(1,2,1); plt.imshow(coins, cmap='gray'); plt.title('Original'); plt.axis('off')
plt.subplot(1,2,2); plt.imshow(segmentation, cmap='gray'); plt.title('Crecimiento de Regiones'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Si el ejercicio habla de “segmentación basada en regiones” y te dejan elegir semillas.
* Útil cuando las regiones son **relativamente homogéneas** en intensidad.

---

### 2.3 Watershed

**Qué hace**

Interpreta la imagen como un mapa de elevación, “inunda” desde marcadores y separa regiones; ideal para separar objetos tocándose.

**Código (monedas + Sobel + watershed):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.filters import sobel
from skimage.segmentation import watershed
from scipy import ndimage as ndi
from skimage.color import label2rgb

coins = data.coins()
elevation_map = sobel(coins)

markers = np.zeros_like(coins)
markers[coins < 30] = 1       # fondo
markers[coins > 150] = 2      # objetos

segmentation = watershed(elevation_map, markers)
segmentation = ndi.binary_fill_holes(segmentation - 1)
image_label_overlay = label2rgb(segmentation, image=coins)

plt.figure(figsize=(10,8))
plt.subplot(2,2,1); plt.imshow(elevation_map, cmap="gray"); plt.title('Mapa de elevación'); plt.axis('off')
plt.subplot(2,2,2); plt.imshow(markers, cmap="nipy_spectral"); plt.title('Marcadores'); plt.axis('off')
plt.subplot(2,2,3); plt.imshow(segmentation, cmap="gray"); plt.title('Segmentación'); plt.axis('off')
plt.subplot(2,2,4); plt.imshow(image_label_overlay); plt.title('Monedas etiquetadas'); plt.axis('off')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Cuando te dicen explícitamente “watershed”.
* Para **separar objetos pegados** (monedas, células, etc.).

---

### 2.4 Segmentación por clustering (SLIC – superpíxeles)

**Qué hace**

Agrupa píxeles en **superpíxeles** (pequeñas regiones más homogéneas) usando clustering en color + posición.

**Código (SLIC):**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, color
from skimage.segmentation import slic, mark_boundaries

coins = data.coins()
coins_rgb = color.gray2rgb(coins)

segments = slic(coins_rgb, n_segments=200, compactness=10, sigma=1, start_label=1)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(coins); axes[0].set_axis_off(); axes[0].set_title('Original')
axes[1].imshow(mark_boundaries(coins_rgb, segments)); axes[1].set_axis_off(); axes[1].set_title('Superpíxeles SLIC')
plt.tight_layout(); plt.show()
```

**Cuándo usarlo**

* Cuando se mencione “superpíxeles” o “segmentación basada en clustering”.
* Buen paso previo antes de clasificar regiones en lugar de píxeles sueltos.

---

### 2.5 Segmentación basada en movimiento (video)

**Qué se hace**

1. Leer vídeo con `cv2.VideoCapture`.
2. Extraer frames (`video_to_frames`).
3. Usar diferencia de frames o background subtraction para obtener máscaras de movimiento.

**Código base (función para extraer frames):**

```python
import numpy as np
import cv2

def video_to_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error al abrir el video")
        return np.array([])

    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    cap.release()
    return np.array(frames)
```

**Cuándo usarlo**

* Ejercicios tipo “segmentar por movimiento” o “detectar objetos en un video”.
* Luego suele combinarse con umbralización y morfología para limpiar la máscara.

---

## 3. Sesión 09 – Morfología matemática

Todas las funciones están en `skimage.morphology`.

### 3.1 Operaciones básicas: erosión, dilatación, apertura, cierre

**Qué hacen**

* **Erosión** (`erosion`, `binary_erosion`): encoge objetos (elimina píxeles del borde).
* **Dilatación** (`dilation`, `binary_dilation`): expande objetos.
* **Apertura** (`opening`): erosión + dilatación (elimina ruido pequeño).
* **Cierre** (`closing`): dilatación + erosión (cierra agujeros).

**Código típico:**

```python
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage.morphology import binary_erosion, binary_dilation, binary_opening, binary_closing, rectangle

image = rgb2gray(imread('./Práctica 9/images/clock2.jpg'))
binary_image = (image > 0.5).astype(int)
selem = rectangle(5, 5)

eroded  = binary_erosion(binary_image, selem)
dilated = binary_dilation(binary_image, selem)
opened  = binary_opening(binary_image, selem)
closed  = binary_closing(binary_image, selem)
```

**Cuándo usarlo**

* Después de umbralizar:

  * Eliminar pequeños puntos → apertura.
  * Rellenar huecos internos → cierre.
  * Refinar el tamaño de los objetos → erosión/dilatación.

---

### 3.2 Esqueletización

**Qué hace**

Reduce objetos binarios a su “esqueleto” de un pixel de grosor.

**Código:**

```python
from skimage.io import imread
from skimage.morphology import skeletonize

im = imread('./Práctica 9/images/dinasaur.png', as_gray=True)
binary_image = (im > 0.5).astype(int)
skeleton = skeletonize(binary_image)
```

**Cuándo usarlo**

* Si piden “esqueletizar” o “extraer esqueleto” de una figura (huesos, ramas, firma).

---

### 3.3 Envolvente convexa

**Qué hace**

Calcula la **envolvente convexa** de un objeto binario.

```python
from skimage.morphology import convex_hull_image

hull = convex_hull_image(binary_image)
```

**Cuándo usarlo**

* Para comparar forma original vs envolvente convexa (p.ej. huellas, firmas).

---

### 3.4 Eliminación de artefactos y objetos pequeños

**Qué hace**

Elimina blobs/objetos menores que un tamaño mínimo.

```python
from skimage.morphology import remove_small_objects

clean = remove_small_objects(binary_image.astype(bool), min_size=50)
```

**Cuándo usarlo**

* Cuando la segmentación te devuelve muchos trozos pequeños que son ruido.

---

### 3.5 Siluetas, contornos y gradiente morfológico

**Gradiente morfológico** = dilatación – erosión → resalta bordes de objetos.

```python
from skimage.morphology import dilation, erosion, disk
import numpy as np

selem = disk(3)
dil = dilation(image, selem)
ero = erosion(image, selem)
gradient = dil - ero
```

**Cuándo usarlo**

* Para **realzar bordes** en imágenes binarizadas o en escala de grises.

---

### 3.6 Sombrero de copa (white_tophat, black_tophat)

**Qué hacen**

* `white_tophat`: resalta detalles **claros** pequeños sobre fondo oscuro.
* `black_tophat`: detalles **oscuros** pequeños sobre fondo claro.

```python
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.morphology import white_tophat, black_tophat, square

im = imread('./Práctica 9/images/tagore.png')[..., 3]  # canal alfa
binary_image = (im > 0.5).astype(int)

im1 = white_tophat(binary_image, square(5))
im2 = black_tophat(binary_image, square(5))
```

**Cuándo usarlo**

* Cuando el enunciado hable de **“realce morfológico”** o “sombrero de copa”.
* Para resaltar detalles finos (letras, puntitos, etc.).

---

### 3.7 Morfología en escala de grises

Se usan las mismas funciones (`erosion`, `dilation`, etc.) sobre imágenes no binarias para suavizar, resaltar máximos/mínimos locales y realzar contraste.

**Cuándo usarlo**

* Si te piden “morfología en escala de grises” o “realce morfológico” sin binarizar.

---

## 4. Sesión 10 – Detección de características y descriptores

### 4.1 Esquinas de Harris

**Qué hace**

Detecta **esquinas/puntos de interés** donde el gradiente cambia mucho en dos direcciones.

**Código (skimage.feature.corner_harris):**

```python
from skimage.feature import corner_harris, corner_peaks, corner_subpix

R = corner_harris(image_gray, k=0.001)
corners = R > 0.01 * R.max()

corner_coordinates = corner_peaks(R, min_distance=5)
coordinates_subpix = corner_subpix(image_gray, corner_coordinates, window_size=11)
```

**Cuándo usarlo**

* Si el ejercicio habla de “detectar esquinas”, “puntos de interés” o “correspondencias entre imágenes”.

---

### 4.2 RANSAC para correspondencias robustas

**Qué hace**

Elimina **correspondencias espurias** y estima una transformación (p.ej. afín) robusta.

**Código (skimage.measure.ransac):**

```python
from skimage.transform import AffineTransform
from skimage.measure import ransac
from scipy.spatial.distance import cdist

# src, dst = coordenadas de puntos emparejados (por ejemplo, esquinas)
model_robust, inliers = ransac(
    (src, dst),
    AffineTransform,
    min_samples=3,
    residual_threshold=2,
    max_trials=1000
)
```

**Cuándo usarlo**

* Si el enunciado habla de **“correspondencias robustas”**, de quitar outliers o de alinear dos imágenes.

---

### 4.3 Detección de blobs (LoG, DoG, DoH)

**Qué hacen**
Detectan regiones aproximadamente circulares o de “mancha” a varias escalas.

**Código:**

```python
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.io import imread
from skimage.color import rgb2gray

image = imread('./images/butterfly.png')[..., :3]
image_gray = rgb2gray(image)

log_blobs = blob_log(image_gray, max_sigma=30, num_sigma=10, threshold=.1)
log_blobs[:, 2] = np.sqrt(2) * log_blobs[:, 2]

dog_blobs = blob_dog(image_gray, max_sigma=30, threshold=0.1)
dog_blobs[:, 2] = np.sqrt(2) * dog_blobs[:, 2]

doh_blobs = blob_doh(image_gray, max_sigma=30, threshold=0.01)
```

**Cuándo usarlo**

* Para detectar **manchas, puntos brillantes u oscuros** (burbujas, células, estrellas, etc.).

---

### 4.4 HoG – Histogram of Oriented Gradients

**Qué hace**

Para cada celda de la imagen, calcula un histograma de orientaciones del gradiente → vector de características.

**Código:**

```python
from skimage import data, exposure
from skimage.color import rgb2gray
from skimage.feature import hog
import matplotlib.pyplot as plt

image = data.astronaut()
image_gray = rgb2gray(image)

fd, hog_image = hog(image_gray,
                    orientations=8,
                    pixels_per_cell=(32, 32),
                    cells_per_block=(1, 1),
                    visualize=True)

hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 0.1))
```

**Cuándo usarlo**

* Cuando haya que **describir textura/formas** y comparar ventanas de imagen.
* En el cuaderno se usa para **comparar descriptores HOG vs SIFT**.

---

### 4.5 SIFT (Scale-Invariant Feature Transform)

**Qué hace**

Detecta puntos de interés y genera descriptores **invariantes a escala/rotación**. Muy útil para emparejar escenas.

**Código (OpenCV):**

```python
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('./images/monalisa.jpg', cv2.IMREAD_COLOR)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT_create()
keypoints, descriptors = sift.detectAndCompute(image_gray, None)
```

**Cuándo usarlo**

* Si quieren **correspondencias entre imágenes** con cambios de escala/punto de vista.
* Cuando comparas HOG vs SIFT en correspondencias (ejercicios del cuaderno).

---

### 4.6 Características de tipo Haar y cascadas (detección de caras)

**Qué hace**

Usa filtros tipo Haar y un **clasificador en cascada** pre-entrenado para detectar rostros.

**Código (OpenCV CascadeClassifier):**

```python
import cv2
import matplotlib.pyplot as plt

image = cv2.imread('./images/lena.jpg')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

haar_cascade = cv2.CascadeClassifier('./images/haarcascade_frontalface_default.xml')

faces = haar_cascade.detectMultiScale(gray_image,
                                      scaleFactor=1.1,
                                      minNeighbors=5,
                                      minSize=(30, 30))

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
```

**Cuándo usarlo**

* Cualquier ejercicio de **detección de rostros** o de **pixelar caras** (ej. “Pixelación de rostros”).

---

## 5. Sesión 11 – Aprendizaje automático con imágenes

### 5.1 Búsqueda de patrones por correlación (Template Matching)

**Qué hace**

Busca una **plantilla** (subimagen) dentro de una imagen por correlación cruzada normalizada.

**Código manual (simplificado):**

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

def normalized_cross_correlation(image, template):
    image_h, image_w = image.shape
    template_h, template_w = template.shape
    result = np.zeros((image_h - template_h + 1, image_w - template_w + 1))

    template_mean = np.mean(template)
    template_std = np.std(template)

    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            patch = image[i:i+template_h, j:j+template_w]
            patch_mean = np.mean(patch)
            patch_std = np.std(patch)
            if patch_std != 0:
                result[i, j] = np.sum((patch - patch_mean) * (template - template_mean)) / \
                               (patch_std * template_std * template_h * template_w)
    return result
```

**Cuándo usarlo**

* Si el enunciado dice “template matching”, “correlación cruzada”, “localizar una plantilla en la imagen”.

(En OpenCV también puedes usar `cv2.matchTemplate`.)

---

### 5.2 PCA – Análisis de Componentes Principales

**Qué hace**

Reduce dimensionalidad proyectando datos en las direcciones de mayor varianza.
En el cuaderno:

* PCA sobre dígitos (`load_digits`).
* PCA sobre una imagen para **compresión** y reconstrucción.

**Código (sobre dígitos):**

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

digits = load_digits()
X = digits.data

X_std = StandardScaler().fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_std)
```

**Cuándo usarlo**

* Ejercicios de **reducción de dimensionalidad** o de **visualizar datos en 2D**.
* Compresión / reconstrucción de imágenes (mostrando componentes principales).

---

### 5.3 K-Means y cuantización de colores

**Qué hace**
Clustering en el espacio de características. En el cuaderno se usa para:

* **Cuantización de colores** (reducir número de colores de una imagen).
* Ver **centroides** de dígitos.

**Código (cuantización de colores):**

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage.io import imread
from skimage import img_as_float
from sklearn.utils import shuffle

pepper = imread("./images/pepper.jpg")
pepper = img_as_float(pepper)

w, h, d = original_shape = tuple(pepper.shape)
image_array = np.reshape(pepper, (w * h, d))

image_array_sample = shuffle(image_array, random_state=0)[:1000]
kmeans = KMeans(n_clusters=32, random_state=42, n_init=10).fit(image_array_sample)

labels = kmeans.predict(image_array)
centers = kmeans.cluster_centers_
quantized = centers[labels].reshape(w, h, d)
```

**Cuándo usarlo**

* Cuando piden **reducir colores** o “cuantización de imagen con K-means”.
* También para explorar clustering en dígitos (visualización de centroides).

---

### 5.4 Clustering espectral para segmentación

**Qué hace**

Construye un grafo de similitud y agrupa nodos (píxeles) según autovectores del laplaciano del grafo. Se usa para **segmentación por clustering espectral**.

**Código (simplificado):**

```python
from sklearn import cluster
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

im = resize(imread('./images/sheldon.jpg'), (100, 100, 3), anti_aliasing=True)

X = np.reshape(im, (-1, im.shape[-1]))
kmeans = cluster.KMeans(n_clusters=2, random_state=0).fit(X)
kmeans_labels = kmeans.labels_.reshape(im.shape[:2])

spectral = cluster.SpectralClustering(n_clusters=2, affinity='nearest_neighbors', random_state=0)
spectral_labels = spectral.fit_predict(X).reshape(im.shape[:2])
```

**Cuándo usarlo**

* Ejercicios que comparen **K-means vs Clustering Espectral** para segmentación.
* Cuando hable de “clustering espectral para segmentación”.

---

### 5.5 Clasificación supervisada: KNN y SVM (Fashion MNIST)

**Qué hacen**

* **KNeighborsClassifier**: clasificador basado en vecinos más cercanos.
* **SVC (SVM)**: clasificador de margen máximo, suele dar mejor rendimiento.

**Código base:**

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from keras.datasets import fashion_mnist

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

# a 0-1 y a vectores
X_train = X_train.reshape((X_train.shape[0], -1)) / 255.0
X_test  = X_test.reshape((X_test.shape[0], -1)) / 255.0

X_train_sub, X_val, y_train_sub, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_sub, y_train_sub)
y_val_pred_knn = knn.predict(X_val)

svm = SVC(kernel='rbf', C=10, gamma=0.001)
svm.fit(X_train_sub, y_train_sub)
y_val_pred_svm = svm.predict(X_val)
```

**Cuándo usarlo**

* Cualquier ejercicio de **clasificar imágenes** (ej. prendas en Fashion MNIST).
* Si te piden comparar modelos (KNN vs SVM) con matriz de confusión y `classification_report`.

---

### 5.6 Regresión de imágenes / Autoencoder de super-resolución

**Qué hace**

Un modelo tipo autoencoder convolucional que recibe imágenes de baja resolución y genera versiones de alta resolución (super-resolución → un caso de regresión de imágenes).

**Código (esquema básico):**

```python
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.layers import Input, Conv2D, UpSampling2D
from keras.models import Model
from keras.datasets import fashion_mnist

(X_train, _), (X_test, _) = fashion_mnist.load_data()
X_train = X_train.astype('float32') / 255.0
X_test  = X_test.astype('float32') / 255.0

X_train = X_train[:1000]
X_train = np.expand_dims(X_train, -1)
X_test  = np.expand_dims(X_test, -1)

input_img = Input(shape=(28, 28, 1))
x = Conv2D(32, (3,3), activation='relu', padding='same')(input_img)
x = Conv2D(32, (3,3), activation='relu', padding='same')(x)
x = UpSampling2D((2,2))(x)
x = Conv2D(1, (3,3), activation='sigmoid', padding='same')(x)

model = Model(input_img, x)
model.compile(optimizer='adam', loss='mse')
model.fit(low_res_train, high_res_train, epochs=10, batch_size=32, validation_split=0.1)
```

*(en el cuaderno se genera `low_res` y `high_res` redimensionando los datos)*

**Cuándo usarlo**

* Ejercicios de **aprendizaje profundo** tipo “mejorar resolución de imágenes” o “reconstruir imágenes” usando CNNs/autoencoders.

