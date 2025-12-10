## 1. Rutina mental: qué mirar primero

Cuando veas **entrada → salida**, pregúntate en este orden:

1. **¿Cambia el tipo de imagen?**

   * Color → blanco y negro → probablemente **binarización / umbralización**.
   * Mucho color → pocos colores → **K-Means / cuantización de colores**.

2. **¿Cambian las formas de los objetos?**

   * Objetos más gordos/flacos, huecos rellenados, puntos pequeños desaparecen → **morfología (erosión, dilatación, apertura, cierre, remove_small_objects, fill_holes)**.
   * Contornos finitos tipo “esqueleto” → **skeletonize**.
   * Contorno convexo más “relleno” → **convex_hull_image**.

3. **¿El resultado resalta bordes/contornos?**

   * Si la salida son solo líneas/blancos sobre fondo negro → **detectores de bordes** (Sobel, Canny, LoG, etc.).
   * Si son bordes y, además, solo líneas rectas o círculos → **Hough de líneas / círculos**.

4. **¿La salida separa objetos / regiones?**

   * Fondo en un color y objetos en otros (cada objeto etiqueta distinta) → **segmentación por regiones** (umbral + morfología, crecimiento de regiones, watershed, clustering, SLIC…).
   * Objetos pegados que en la salida están separados → huele a **watershed + morfología**.

5. **¿Ha desaparecido el ruido?**

   * Puntos sueltos / “sal y pimienta” eliminados → **apertura** o **closing + remove_small_objects**.
   * Imagen más suave, bordes menos serrados → **filtro gaussiano** u otro suavizado antes de segmentar.

6. **¿Hay “clases” o etiquetas semánticas?**

   * Cada píxel/región tiene un color que representa una clase (cielo, suelo, persona, etc.) o se clasifica una imagen como “camiseta/zapatilla” → **clasificación (KNN, SVM)** o clustering (K-Means, espectral).
   * Resultado numérico (clase de dígito, tipo de prenda) y no imagen → seguro **modelo de ML**.

7. **¿Ves mejor resolución / reconstrucción?**

   * Entrada borrosa/pequeña, salida nítida/grande → **autoencoder / modelo de super-resolución**.

8. **¿Se ha resaltado o encontrado un patrón pequeño concreto?**

   * En la salida solo se ve marcada una parte que coincide con un trozo de la imagen original → **template matching / correlación cruzada**.

---

## 2. Patrones visuales típicos → método que encaja

Piensa en esto como una mini-tabla mental:

### 2.1 Imagen final binaria (solo blanco/negro)

* Objetos claramente blancos y fondo negro (o al revés).
* Posible desalineación de sombras, cambio brusco de iluminación.

👉 **Probable pipeline:**

* `rgb2gray`
* `threshold_otsu` o umbral fijo → `binary_image`
* Morfología:

  * **Ruido pequeño fuera** → `binary_opening` + `remove_small_objects`
  * **Agujeros rellenados** → `binary_closing` o `ndi.binary_fill_holes`

---

### 2.2 Bordes / contornos

**Salida:**

* Se ven solo contornos, finos, sobre fondo negro.

👉 **Detectores de bordes:**

* Bordes suaves pero robustos al ruido → `feature.canny`
* Comparación de varios filtros → `filters.sobel`, `prewitt`, `scharr`, `laplace`
* Bordes a una determinada escala → `gaussian_laplace` o DoG (LoG/DoG).

**Si las líneas son rectas o círculos muy marcados en la salida:**

* Usar bordes (**Canny**) + **Hough** (`hough_line`, `hough_circle`).

---

### 2.3 Objetos más limpios / sin defectos

Mira cambio de forma:

* Entrada: manchas pequeñas, agujeros, rebabas.
* Salida: mismos objetos pero:

  * Bordes suaves
  * Manchas pequeñas desaparecidas
  * Rellenos de huecos

👉 **Morfología:**

* Quitar motas pequeñas → `opening`, `remove_small_objects`
* Rellenar huecos internos → `closing`, `binary_fill_holes`
* Hacerlos un poco más gordos/fuertes → `binary_dilation`
* Hacerlos más finos → `binary_erosion`
* Borde resaltado → gradiente morfológico (`dilation - erosion`).

Si además los objetos pegados pasan a estar **separados**:

* Muy típico de **watershed** sobre mapa de elevación (`sobel`) + marcadores.

---

### 2.4 Colores simplificados / “efecto poster”

Salida:

* Menos colores, aspecto tipo póster, o zonas grandes del mismo color.

👉 Cuadra perfecto con:

* **Cuantización de colores con K-Means**:

  * Vectorizar píxeles → `KMeans(n_clusters=k)` → reconstruir imagen desde `cluster_centers_`.

También puede ser:

* **Clustering para segmentar** (K-Means o espectral)

  * Si el objetivo parece separar regiones (cielo, tierra, objeto) por color/posición.

---

### 2.5 Cada objeto con un color distinto (etiquetado)

Si el resultado tiene **cada objeto en un color plano distinto** (como etiquetas tipo 1, 2, 3…) o se ve una mezcla de colores “random” pero cada mancha homogénea es un objeto:

👉 Eso suele ser:

* `label2rgb` aplicado a una imagen de etiquetas;
* La obtención de esas etiquetas viene de:

  * Segmentación (threshold + morfología),
  * Watershed,
  * Clustering (K-Means / espectral),
  * SLIC + agrupamiento.

---

### 2.6 Puntos o “manchas” circulares detectadas

Salida:

* Círculos/blobs marcados con puntos, pequeños discos, o círculos de contorno sobre la imagen.

👉 **Blob detection**:

* `blob_log`, `blob_dog`, `blob_doh`
* A veces combinado con `circle_perimeter`.

---

### 2.7 Caras ocultas, pixeladas o marcadas

* Entrada: foto normal con caras.
* Salida: caras pixeladas/desenfocadas o cajas alrededor de cada cara.

👉 Dos pasos típicos:

1. **Detección de caras**:

   * Clasificador en cascada: `CascadeClassifier.detectMultiScale`
   * O HoG/SIFT + clasificador (según cuaderno, casi seguro Haar cascade).

2. **Postprocesado**:

   * Dibujar rectángulo (`cv2.rectangle`)
   * O pixelar/desenfocar solo esa región.

---

### 2.8 Imagen clasificada / etiqueta textual

Si lo único que cambia es que te dan una **clase** (número, tipo de prenda, etc.), aunque las imágenes sean iguales visualmente, sabes que estás en:

* **Clasificación supervisada** (S11):

  * KNN (`KNeighborsClassifier`)
  * SVM (`SVC`)
  * Tal vez CNN/autoencoder si lo han metido.

---

### 2.9 Mejora de resolución / reconstrucción

* Entrada: borroso, pequeño, con ruido.
* Salida: más nítido, más grande, reconstruido.

👉 Normalmente:

* **Autoencoder / CNN**

  * Modelo tipo input baja resolución → output alta resolución.
  * Entrenado con `model.fit(low_res, high_res)`.

---

### 2.10 Localizar un patrón concreto dentro de la imagen

* Salida: solo aparece marcado un cuadradito o un mapa de correlación con un pico en el lugar donde está el patrón.

👉 **Template matching / correlación cruzada**:

* Implementación manual (como en el cuaderno) o con `cv2.matchTemplate`.

---

## 3. Combos típicos de técnicas (pipelines “core”)

Cuando veas una salida, piensa en **pipeline**, no en técnica aislada. Algunos combos que seguro están en tu examen:

1. **Segmentar objetos + limpiar + etiquetar**

   * `rgb2gray`
   * `threshold_otsu`
   * `binary_opening` / `closing`
   * `remove_small_objects`
   * `label` + `label2rgb`
     ➜ Salida: objetos limpios y coloreados / contados.

2. **Separar objetos pegados**

   * Suavizado (Gauss)
   * `sobel` → mapa de elevación
   * Marcadores (fondo/objeto)
   * `watershed`
   * Morfología de retoque
     ➜ Monedas/células separadas.

3. **Detectar líneas/círculos**

   * `canny`
   * `hough_line` / `hough_circle`
     ➜ Salida: líneas o círculos marcados.

4. **Detección + clasificación**

   * Extraer características (HoG, SIFT)
   * `KNeighborsClassifier` / `SVC`
     ➜ Salida: clase del objeto o mapa de clases.

5. **Color → regiones / objetos**

   * SLIC (superpíxeles)
   * Clustering (K-Means o espectral) sobre superpíxeles
     ➜ Salida: segmentación por regiones, no por píxel.

---

## 4. Cómo practicar el ojo para el examen

Cuando repases los cuadernos:

* Mira cada **figura antes/después** y pregúntate:

  > “Si yo solo viera estas dos imágenes en el examen, ¿reconocería que esto es un watershed? ¿Que esto es una apertura? ¿Que esto son blobs DoG?”

* Asocia mentalmente:

  * **Aspecto visual** ↔ **nombre de la técnica** ↔ **par de líneas de código clave**.

    * Bordes finos, mapa de contornos → `feature.canny`
    * Objetos limpios, sin puntitos → `binary_opening` + `remove_small_objects`
    * Monedas separadas → `watershed`
    * Pocos colores → `KMeans(n_clusters=k)`
    * Caras marcadas → `CascadeClassifier.detectMultiScale`

Si quieres, en el siguiente mensaje puedo hacerte una **chuleta ultra corta** tipo:

> “Si ves X en la salida → usa Y (con este código mínimo)”

para que la memorices como patrón visual → método.
