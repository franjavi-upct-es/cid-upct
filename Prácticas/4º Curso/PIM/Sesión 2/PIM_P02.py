# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: pim
#     language: python
#     name: python3
# ---

# %% [markdown]
# <style>
#     pre {
#         white-space: pre-wrap;
#         word-wrap: break-word;
#     }
# </style>
#
# <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
#     <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 600;">Procesamiento de Imagen en Medicina</h1>
#     <h3 style="color: rgba(255,255,255,0.95); margin: 12px 0 0 0; font-size: 16px; font-weight: 400;">Grado en Ciencia e Ingeniería de Datos | UMU - UPCT</h3>
# </div>

# %% [markdown]
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
#
# ### <span style="color: #667eea;">**Práctica 02**</span>
# ## Reconstrucción de Imagen Médica
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
#
# ### Objetivos
# - Comprender el proceso de reconstrucción de imagen por Tomografía Computarizada y Resonancia Magnética.
# - Implementar algoritmos básicos de reconstrucción en Python.
# - Analizar el impacto del muestreo, el ruido y el filtrado en la calidad de la reconstrucción.
#
# ### Contenidos
#
# - [Entorno de Trabajo](#entorno01)
# - [Fantoma para reconstrucción](#phantom01)
# - [Reconstrucción de imagen CT](#CTrecon01)
# - [Ejercicios prácticos: CT](#CTejercicios01)
# - [Reconstrucción MRI](#MRIrecon01)
# - [Ejercicios prácticos: MRI](#CTejercicios01)

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='entorno01'></a>
#
# ## <span style="color: #667eea;">Entorno de Trabajo</span>
#
# ### *Kaggle Notebooks*
#
# 1. Descarga este notebook desde el Aula Virtual.
# 2. Accede a [kaggle.com](https://www.kaggle.com) con tu cuenta.
# 3. Ve a **"Create"** → **"Import Notebook"**.
# 4. En **"Advanced Settings"** selecciona la opción **"Quick Save"**.
# 5. Sube el archivo `.ipynb` descargado.
# 6. Pulsa el botón **"Edit"** para acceder al notebook.
# 7. ¡Listo! Ejecuta las celdas secuencialmente con `Shift + Enter`.

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='dicom01'></a>
#
# ## <span style="color: #667eea;">1. Fantoma para reconstrucción</span>
#
# En el desarrollo de la práctica utilizaremos el fantoma de Shepp-Logan, una imagen sintética estándar de referencia, creada por Larry Shepp y Benjamin F. Logan en 1974, que modela una sección transversal del cerebro humano. Esta imagen se suele utilizar para evaluar algoritmos de reconstrucción en tomografía computarizada (CT) y resonancia magnética (MRI). 
#
# ### *Características Principales:*
#
# - **Diseño:** consiste en una elipse exterior principal, que representa el cráneo, con varias elipses interiores más pequeñas con diferentes intensidades,que simulan las estructuras cerebrales.
# - **Propósito:** sirve como un estándar para evaluar la calidad, resolución y artefactos en la reconstrucción de imágenes.
#
# - **Dimensiones:** 2D o 3D.

# %% [markdown]
# ### *Carga del fantoma de Shepp-Logan*
#
# En primer lugar, cargamos y visualizamos la imagen de prueba que consideraremos como anatomía de referencia.

# %%
import matplotlib.pyplot as plt
from skimage.data import shepp_logan_phantom

# Cargar la imagen de prueba (Shepp-Logan phantom)
image = shepp_logan_phantom()

#Visualización del fantoma
plt.figure(figsize=(6, 6))
plt.title("Fantoma de Shepp-Logan (imagen original)")
plt.imshow(image, cmap='gray')
plt.axis('off')
plt.show()

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='dicom01'></a>
#
# ## <span style="color: #667eea;">2. Reconstrucción de Imagen CT</span>
#
# La reconstrucción de imágenes por tomografía computarizada (CT, Computed Tomography) es un proceso matemático avanzado que convierte los datos crudos de múltiples proyecciones de rayos X (adquiridos desde diversos ángulos) en imágenes transversales o cortes detallados del interior del cuerpo, donde la intensidad de los píxeles representa el coeficiente de atenuación de los diferentes tejidos. 
#

# %% [markdown]
# ### *2.1. Simulación de datos tomográficos:*
#
# La imagen de prueba representa la anatomía real. En este caso, el mapa de atenuación de los tejidos $\mu(x,y)$.
#
# Como primer paso, partiendo de la imagen de prueba, debemos simular la adquisición de proyecciones CT.
# El conjunto de proyecciones CT se organiza en el **sinograma**, un mapa ordenado en función del ángulo de proyección y la posición del detector. Por definición, el sinograma es la Transformada de Radon de $\mu(x,y)$. 
#
# A continuación, generamos el sinograma a partir del fantoma de Shepp-Logan mediante la función `radon` y visualizamos el resultado.

# %%
import numpy as np
from skimage.transform import radon

# Simulación de las proyecciones CT usando la transformada de Radon (sinograma)
theta = np.linspace(0., 180., max(image.shape), endpoint=False)
sinogram = radon(image, theta=theta)
dx, dy = 0.5 * 180.0 / max(image.shape), 0.5 / sinogram.shape[0]

# Visualización del sinogramna
plt.figure(figsize=(8, 6))
plt.title("Sinograma (Transformada de Radon)")
plt.xlabel("Ángulo de proyección (grados)")
plt.ylabel("Posición del detector")
plt.imshow(sinogram, cmap='gray', extent=(-dx, 180.0 + dx, -dy, sinogram.shape[0] + dy), aspect='auto')
plt.show()

# %% [markdown]
# ### *2.2. Retroproyección directa:*
#
# El proceso de reconstrucción de imagen corresponde al problema inverso. El objetivo es determinar el mapa de atenuación $\mu(x,y)$ a partir de las proyecciones CT adquiridas (sinograma).
#
# El proceso implica la inversión de la Transformada de Radon. Sin embargo, como comprobaremos a continuación, una retropropagación directa de las proyecciones no es suficiente para reconstruir la imagen CT. 
#
# A continuación, analizamos la aplicación de la transformada inversa de Radon sobre el sinograma, es decir, la reconstrucción por retroproyección directa (back projection, BP). Utilizamos la función `iradon`, con el parámetro `filter_name=None` para que no se aplique ningún filtrado a los datos.

# %%
from skimage.transform import iradon

# Aplicación de la transformada inversa de Radon (sin filtrado)
recon_bp = iradon(sinogram, theta=theta, filter_name=None)

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
# Imagen de referencia
im0 = axes[0].imshow(image, cmap='gray')
axes[0].set_title("Referencia")
axes[0].axis('off')
# Retroproyección directa
im1 = axes[1].imshow(recon_bp, cmap='gray')
axes[1].set_title("Retroproyección directa (sin filtrado)")
axes[1].axis('off')
plt.tight_layout()
plt.show()

# %% [markdown]
# La imagen aparece borrosa. La retroproyección directa introduce un suavizado que debe compensarse mediante filtrado.

# %% [markdown]
# ### *2.3. Retroproyección filtrada (FBP):*
#
# La reconstrucción por Retroproyección Filtrada (Filtered Back Projection - FBP) es el método analítico clásico utilizado en reconstrucción de imagen CT. 
#
# Para corregir el desenfoque de la retroproyección directa (transformada inversa de Radon), se aplica un filtro matemático (en el dominio de la frecuencia, típicamente un filtro "ramp") antes de la retroproyección final. 
#
# Este filtro acentúa los bordes de alta frecuencia y elimina la borrosidad, mejorando la nitidez de la imagen. El resultado final es la suma de todas las retroproyecciones filtradas, creando una imagen con buena resolución espacial y un contraste adecuado. 
#
# **Ventajas:**
# - Velocidad: Es extremadamente rápida en comparación con los métodos iterativos, lo que permite la visualización casi instantánea de la imagen.
# - Eficiencia Computacional: Es un algoritmo directo y sencillo.
# - Alta Resolución: Proporciona imágenes con bordes definidos y alta resolución espacial.
#
# **Limitaciones:**
# - Ruido e Imágenes de Baja Dosis: La FBP no gestiona bien el ruido en los datos, por lo que las imágenes de baja dosis pueden tener mucho "ruido" o granulosidad.
# - Artefactos: Es propensa a generar artefactos, especialmente en pacientes grandes o cuando hay metales, lo que degrada la calidad de la imagen.

# %%
from skimage.transform.radon_transform import _get_fourier_filter

# Respuesta en frecuencia del filtro rampa
filtro = 'ramp'
h = _get_fourier_filter(2000, filtro)

plt.figure(figsize=(4, 4))
plt.title("Respuesta del filtro")
plt.plot(h)
plt.xlim([0, 1000])
plt.xlabel('frecuencia')
plt.show()

# Realizamos una reconstrucción FBP (filtered back projection) del sinograma: 
# Filtrado en el dominio frecuencial + transformada inversa de Radon
recon_fbp = iradon(sinogram, theta=theta, filter_name=filtro)

# Evaluación del error con respecto a la referencia
error = recon_fbp - image

# Visualización
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Imagen de referencia
im0 = axes[0].imshow(image, cmap='gray')
axes[0].set_title("Referencia")
axes[0].axis('off')
# Retroproyección filtrada
im1 = axes[1].imshow(recon_fbp, cmap='gray')
axes[1].set_title("Reconstrucción FBP (Filtro Ramp)")
axes[1].axis('off')
# Error de reconstrucción
im2 = axes[2].imshow(error, cmap='gray')
axes[2].set_title("Error de reconstrucción")
axes[2].axis('off')
plt.tight_layout()
plt.show()

print(f'Error de reconstrucción FBP (RMSE): {np.sqrt(np.mean(error**2)):.3g}')

# %% [markdown]
# El filtro ramp compensa el efecto de desenfoque de la retroproyección mediante un realce de altas frecuencias.

# %% [markdown]
# ### *2.4. Efecto del ruido en la reconstrucción:*
#
# El ruido dominante en CT es el ruido cuántico. Es una distorsión aleatoria que aparece como un granulado o "moteado" en la imagen. 
#
# Es un proceso aleatorio por naturaleza debido a las fluctuaciones en el número de fotones que llegan al detector después de atravesar al paciente.
#
# El conteo de fotones en el detector se modela con una distribución de Poisson. En este modelo estadístico, la varianza es igual a la media, lo que significa que el ruido ($\sigma$) es proporcional a la raíz cuadrada del número medio de fotones detectados ($SNR=\sqrt{N}$). 
#
# Cuando el flujo de fotones es muy alto (dosis estándar), la distribución de Poisson se asemeja tanto a una distribución Gaussiana que a menudo se modela de esa forma para simplificar.
#
# En condiciones de dosis extremadamente bajas, el ruido total se considera una mezcla de Poisson (cuántico) y Gaussiano (ruido electrónico del sistema).

# %% [markdown]
# **Ruido electrónico:**
#
# A continuación, simularemos el efecto del ruido electrónico (ruido aditivo gaussiano) en la reconstrucción.

# %%
# Simulación de ruido electrónico del sistema

# Sinograma con ruido aditivo gaussiano 
# Definimos la desviación típica del ruido como el 1% del máximo de la señal
noise_std =  0.01 * np.max(np.abs(sinogram))
noise = np.random.normal(0, noise_std, sinogram.shape)
sinogram_noisy = sinogram + noise

# Reconstrucción de imagen por retroproyección filtrada
recon_fbp = iradon(sinogram_noisy, theta=theta, filter_name='ramp')

# Evaluación del error con respecto a la referencia
error = recon_fbp - image

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Imagen de referencia
im0 = axes[0].imshow(image, cmap=plt.cm.Greys_r)
axes[0].set_title("Referencia")
axes[0].axis('off')
# Retroproyección filtrada
im1 = axes[1].imshow(recon_fbp, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción FBP (ruido electrónico)")
axes[1].axis('off')
# Error de reconstrucción
im2 = axes[2].imshow(error, cmap=plt.cm.Greys_r)
axes[2].set_title("Error de reconstrucción")
axes[2].axis('off')
plt.tight_layout()
plt.show()

print(f'Error de reconstrucción (RMSE): {np.sqrt(np.mean(error**2)):.3g}')

# %% [markdown]
# **Ruido cuántico:**
#
# A continuación, simularemos el efecto del ruido cuántico en el detector. Partiendo del modelo de la señal transmitida (Ley de Beer–Lambert), la señal detectada idealmente está definida como:
#
# $I = I_0 e^{{-\int{\mu(x,y)}}ds}$
#
# En el detector, se digitaliza la señal y se calcula el sinograma aplicando logaritmo:
#
# $\rho(\theta,\rho) = \ln{(\frac{I_0}{I})}$
#
# El ruido cuántico afecta al conteo de fotones en el detector siguiendo una distribución de Poisson. Por tanto, la señal que llega al detector es realmente: $I_{meas}$ ~ Poisson($I$)
#
# Con estas consideraciones, podemos simular el sinograma ruidoso como: 
#
# $\rho_{noisy}(\theta,\rho) = \ln{(\frac{I_0}{I_{meas}})}$

# %%
# Definimos la intensidad incidente (controla la dosis)
I0 = 1e5

# Escalado del sinograma de referencia para que exista correspondencia con unidades físicas
sinogram_scaled = sinogram / sinogram.max() * 2.0

# Intensidad ideal en el detector (a partir del sinograma escalado)
I = I0 * np.exp(-sinogram_scaled)

# Ruido cuántico (Poison)
I_noisy = np.random.poisson(I)

# Sinograma ruidoso tras linealización aplicando logaritmo
I_noisy[I_noisy == 0] = 1    # Evitar ceros antes del logaritmo
sinogram_poisson = -np.log(I_noisy / I0)

# Reconstrucción FBP ideal
recon_ideal = iradon(sinogram_scaled, theta=theta, filter_name='ramp')

# Reconstrucción FBP con ruido cuántico
recon_poisson = iradon(sinogram_poisson, theta=theta, filter_name='ramp')

# Evaluación del error con respecto a la referencia
error = recon_poisson - recon_ideal

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Imagen de referencia
im0 = axes[0].imshow(recon_ideal, cmap=plt.cm.Greys_r)
axes[0].set_title("Reconstrucción FBP (ideal)")
axes[0].axis('off')
# Retroproyección filtrada
im1 = axes[1].imshow(recon_poisson, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción FBP (ruido cuántico)")
axes[1].axis('off')
# Error de reconstrucción
im2 = axes[2].imshow(error, cmap=plt.cm.Greys_r)
axes[2].set_title("Error de reconstrucción")
axes[2].axis('off')
plt.tight_layout()
plt.show()

print(f'Error de reconstrucción (RMSE): {np.sqrt(np.mean(error**2)):.3g}')

# %% [markdown]
# ### *2.5. Reconstrucción iterativa:*
#
# Los métodos de reconstrucción iterativa son un tipo de técnicas que se utilizan para reconstruir imágenes a partir de datos de proyección de forma iterativa. A diferencia de métodos analíticos como la retroproyección filtrada (FBP), que proporcionan una solución matemática directa, los métodos iterativos refinan la estimación de la imagen mediante múltiples iteraciones para minimizar errores y mejorar la calidad de la imagen. Estos métodos son especialmente útiles en situaciones con datos ruidosos o incompletos.

# %% [markdown]
# **Técnica de Reconstrucción Algebraica Simultánea (SART, Simultaneous Algebraic Reconstruction Technique)**
#
# Uno de los métodos de reconstrucción iterativa más sencillos es la **Técnica de Reconstrucción Algebraica (ART)**. 
# ART actualiza la estimación de la imagen iterativamente considerando cada proyección y ajustándola para reducir la discrepancia entre las proyecciones medidas y estimadas. Pasos de la ART:
#
# 1. Inicializar: Se parte de una estimación inicial para la imagen (p. ej., solo ceros).
#
# 2. Iterar hasta que la solución converja o se alcance un número máximo de iteraciones:
#
#     2.1. Para proyección, se calcula la proyección estimada a partir de la estimación actual de la imagen.
#
#     2.2. Actualizar la estimación de la imagen para reducir la diferencia entre las proyecciones estimadas y las reales.
#
#
# **SART** es una variante optimizada del ART diseñada para mejorar la calidad de la imagen y reducir el ruido.
# La diferencia fundamental es cuándo se actualiza la imagen: mientras que ART actualiza la imagen rayo por rayo, SART procesa todos los rayos de un mismo ángulo de proyección a la vez y aplica el promedio de las correcciones.
#
# A continuación, se muestra el código de una reconstrucción iterativa con SART. 

# %%
from skimage.transform import iradon_sart

recon_sart = iradon_sart(sinogram, theta=theta)

error_sart1 = recon_sart - image
print(f'SART (1 iteración) Error de reconstrucción (RMSE): ' f'{np.sqrt(np.mean(error_sart1**2)):.3g}')

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Imagen de referencia
im0 = axes[0].imshow(image, cmap=plt.cm.Greys_r)
axes[0].set_title("Referencia")
axes[0].axis('off')
# Reconstrucción SART (1 iteración)
im1 = axes[1].imshow(recon_sart, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción SART\n(1 iteración)")
axes[1].axis('off')
# Error de reconstrucción (SART, 1 iter.)
im2 = axes[2].imshow(error_sart1, cmap=plt.cm.Greys_r)
axes[2].set_title("Error SART\n(1 iteración)")
axes[2].axis('off')

# Ejecutamos una segunda iteración de SART, con el resultado de la primera iteración como estimación inicial
recon_sart2 = iradon_sart(sinogram, theta=theta, image=recon_sart)

error_sart2 = recon_sart2 - image
print(f'SART (2 iteraciones) Error de reconstrucción (RMSE): ' f'{np.sqrt(np.mean(error_sart2**2)):.3g}')

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# Imagen de referencia
im0 = axes[0].imshow(recon_sart, cmap=plt.cm.Greys_r)
axes[0].set_title("Estimación inicial\n(SART, 1 iter.)")
axes[0].axis('off')
# Reconstrucción SART (2 iteraciones)
im1 = axes[1].imshow(recon_sart2, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción SART\n(2 iteraciones)")
axes[1].axis('off')
# Error de reconstrucción (SART, 2 iter.)
im2 = axes[2].imshow(error_sart2, cmap=plt.cm.Greys_r)
axes[2].set_title("Error SART\n(2 iter.)")
axes[2].axis('off')

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='dicom01'></a>
#
# ## <span style="color: #667eea;">3. Ejercicios prácticos: CT</span>

# %% [markdown]
# ### *Ejercicio 1. Efecto del nivel de dosis en el ruido*
#
# Analizar cómo la reducción de dosis afecta a la calidad de la reconstrucción de imagen CT en presencia de ruido cuántico.
#
# En el bloque de reconstrucción FBP con ruido cuántico, repetir el experimento para distintos valores del número medio de fotones incidentes ($I_0 = 10^4, 5·10^4, 10^5$) 
#
# Comparar visualmente las reconstrucciones obtenidas y analizar la diferencia con respecto a la reconstrucción ideal (sin ruido). Se recomienda utilizar una misma ventana de visualización para todas las imágenes. Visualice tanto la imagen completa como una región de interés que contenga alguna elipse de bajo contraste.

# %%
# SOLUCIÓN DEL EJERCICIO 1

import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon

# Escalado del sinograma de referencia
sinogram_scaled = sinogram / sinogram.max() * 2.0

# Reconstrucción FBP ideal (sin ruido)
recon_ideal = iradon(sinogram_scaled, theta=theta, filter_name='ramp')

# Valores de IO a analizar
IO_values = [1e4, 5e4, 1e5]
labels = [r"$I_0 = 10^4$", r"$I_1 = 5\cdot 10^4$", r"$I_2 = 10^5$"]

# Almacenar reconstrucciones
recons = []
errors = []

for IO in IO_values:
    # Intensidad ideal en el detector
    I = IO * np.exp(-sinogram_scaled)
    # Ruido cuántico (Poisson)
    I_noisy = np.random.poisson(I)
    I_noisy[I_noisy == 0] = 1   # Evitar ceros antes del logaritmo
    # Sinograma ruidoso
    recon = iradon(sinogram_poisson, theta=theta, filter_name='ramp')
    recons.append(recon)
    errors.append(recon - recon_ideal)

# --- Ventana de visualización común ---
vmin = recon_ideal.min()
vmax = recon_ideal.max()

# --- Visualización: imagen completa ---
fig, axes = plt.subplots(2, 4, figsize=(20, 10))

# Fila 1: Reconstrucciones
axes[0, 0].imshow(recon_ideal, cmap="gray", vmin=vmin, vmax=vmax)
axes[0, 0].set_title("Ideal (sin ruido)")
axes[0, 0].axis('off')

for i in range(3):
    axes[0, i+1].imshow(recons[i], cmap="gray", vmin=vmin, vmax=vmax)
    axes[0, i+1].set_title(f"FBP con {labels[i]}")
    axes[0, i+1].axis('off')

# Fila 2: Errores
axes[1, 0].axis('off')  # Sin error para la ideal
axes[1, 0].set_title("—")

err_vmax = max(np.abs(e).max() for e in errors)
for i in range(3):
    rmse = np.sqrt(np.mean(errors[i]**2))
    axes[1, i+1].imshow(errors[i], cmap='gray', vmin=-err_vmax, vmax=err_vmax)
    axes[1, i+1].set_title(f"Error {labels[i]}\nRMSE = {rmse:.4f}")
    axes[1, i+1].axis('off')

plt.suptitle("Efecto del nivel de dosis en la reconstrucción FBP (imagen completa)", fontsize=15)
plt.tight_layout()
plt.show()

# --- Región de interés (ROI) con elipse de bajo contraste ---
# Selección de una ROI que contenga estructuras de bajo contraste
# (zona inferior del fantoma, aprox.)
roi_row = slice(150, 200)
roi_col = slice(150, 250)

fig, axes = plt.subplots(2, 4, figsize=(20, 10))

axes[0, 0].imshow(recon_ideal[roi_row, roi_col], cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 0].set_title("Ideal (ROI)")
axes[0, 0].axis('off')

for i in range(3):
    axes[0, i+1].imshow(recons[i][roi_row, roi_col], cmap='gray', vmin=vmin, vmax=vmax)
    axes[0, i+1].set_title(f"FBP {labels[i]} (ROI)")
    axes[0, i+1].axis('off')

axes[1, 0].axis('off')
axes[1, 0].set_title("—")

for i in range(3):
    rmse = np.sqrt(np.mean(errors[i][roi_row, roi_col]**2))
    axes[1, i+1].imshow(errors[i][roi_row, roi_col], cmap='gray', vmin=-err_vmax, vmax=err_vmax)
    axes[1, i+1].set_title(f"Error {labels[i]} (ROI)\nRMSE = {rmse:.4f}")
    axes[1, i+1].axis('off')

plt.suptitle("Efecto del nivel de dosis - Región de interés (bajo contraste)", fontsize=15)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### *Ejercicio 2. Comparativa de filtros en reconstrucción FBP*
#
# Estudiar el compromiso entre resolución y ruido en la reconstrucción FBP utilizando los distintos filtros disponibles. Comparar los resultados obtenidos con el filtro Ram-Lak (`ramp`) y filtros suavizados o apodizados (`shepp-logan`, `hann` y `hamming`) en un escenario de baja dosis ($I_0 = 10^4$) con ruido cuántico. Representar la respuesta en frecuencia de los diferentes filtros.

# %%
# SOLUCIÓN DEL EJERCICIO 2
import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon
from skimage.transform.radon_transform import _get_fourier_filter

# --- 1. Respuesta en frecuencia de los filtros ---
filter_names = ['ramp', 'shepp-logan', 'hann', 'hamming']
filter_labels = ['Ram-Lak (ramp)', 'Shepp-Logan', 'Hann', 'Hamming']
colors = ['#ff0000', '#0000ff', '#00ff00', "#007aff"]

fig, ax = plt.subplots(figsize=(8, 6))
for fname, label, color in zip(filter_names, filter_labels, colors):
    h = _get_fourier_filter(2000, fname)
    freqs = np.linspace(0, 1, len(h) // 2)
    ax.plot(freqs, h[:len(h)//2], label=label, color=color, linewidth=2)

ax.set_xlabel('Frecuencia normalizada')
ax.set_ylabel('Amplitud')
ax.set_title('Respuesta en frecuencia de los filtros FBP')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- 2. Simulación de sinograma con ruido cuántico (IO = 1e4, baja) ---
sinogram_scaled = sinogram / sinogram.max() * 2.0

I0 = 1e4
I = I0 * np.exp(-sinogram_scaled)
I_noisy = np.random.poisson(I)
I_noisy[I_noisy == 0] = 1
sinogram_noisy = -np.log(I_noisy / I0)

# Reconstrucción ideal (sin ruido)
recon_ideal = iradon(sinogram_scaled, theta=theta, filter_name='ramp')

# --- 3. Reconstrucción FBP con cada filtro ---
recons = {}
errors = {}
for fname in filter_names:
    recon = iradon(sinogram_noisy, theta=theta, filter_name=fname)
    recons[fname] = recon
    errors[fname] = recon - recon_ideal

# --- 4. Visualización: reconstrucciones y errores ---
vmin = recon_ideal.min()
vmax = recon_ideal.max()

fig, axes = plt.subplots(2, len(filter_names), figsize=(5 * len(filter_names), 10))

err_vmax = max(np.abs(errors[f]).max() for f in filter_names)

for i, (fname, label) in enumerate(zip(filter_names, filter_labels)):
    # Fila 1: Reconstrucciones
    axes[0, i].imshow(recons[fname], cmap='gray', vmin=vmin, vmax=vmax)
    axes[0, i].set_title(f"FBP - {label}")
    axes[0, i].axis('off')

    # Fila 2: Errores
    rmse = np.sqrt(np.mean(errors[fname]**2))
    axes[1, i].imshow(errors[fname], cmap='gray', vmin=-err_vmax, vmax=err_vmax)
    axes[1, i].set_title(f"Error - {label}\nRMSE = {rmse:.4f}")
    axes[1, i].axis('off')

plt.suptitle(r"Comparativa de filtros FBP con ruido cuántico ($I_0 = 10^4$)", fontsize=15)
plt.tight_layout()
plt.show()

# --- 5. ROI de bajo contraste ---
roi_row = slice(150, 200)
roi_col = slice(150, 250)

fig, axes = plt.subplots(2, len(filter_names), figsize=(5 * len(filter_names), 10))

for i, (fname, label) in enumerate(zip(filter_names, filter_labels)):
    axes[0, i].imshow(recons[fname][roi_row, roi_col], cmap='gray', vmin=vmin, vmax=vmax)
    axes[0, i].set_title(f"{label} (ROI)")
    axes[0, i].axis('off')

    rmse_roi = np.sqrt(np.mean(errors[fname][roi_row, roi_col]**2))
    axes[1, i].imshow(errors[fname][roi_row, roi_col], cmap='gray', vmin=-err_vmax, vmax=err_vmax)
    axes[1, i].set_title(f"Error {label} (ROI)\nRMSE = {rmse_roi:.4f}")
    axes[1, i].axis('off')

plt.suptitle(r"Comparativa de filtros FBP - Región de interés ($I_0 = 10^4$)", fontsize=15)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### *Ejercicio 3. Reconstrucción iterativa y submuestreo*
#
# a) Reconstruir la imagen utilizando un número reducido de proyecciones (por ejemplo 50 ángulos) mediante FBP. Analizar los artefactos que aparecen y compararlos con los producidos por ruido cuántico.
#
# b) Aplicar el algoritmo SART para uno y dos ciclos de iteración sobre el mismo conjunto de datos. Comparar las reconstrucciones obtenidas y discutir la evolución del error.

# %%
# SOLUCIÓN DEL EJERCICIO 3

import numpy as np
import matplotlib.pyplot as plt
from skimage.transform import iradon, iradon_sart, radon

# a) Reconstrucción FBP con número reducido de proyecciones

# Sinograma con muestreo completo (referencia)
theta_full = np.linspace(0., 180., max(image.shape), endpoint=False)
sinogram_full = radon(image, theta=theta_full)
recon_full = iradon(sinogram_full, theta=theta_full, filter_name='ramp')

# Sinograma submuestreado (50 ángulos)
n_angles = 50
theta_sub = np.linspace(0., 180., n_angles, endpoint=False)
sinogram_sub = radon(image, theta=theta_sub)

# Reconstrucción FBP con 50 proyecciones
recon_fbp_sub = iradon(sinogram_sub, theta=theta_sub, filter_name='ramp')
error_fbp_sub = recon_fbp_sub - image

# Reconstrucción FBP con ruido cuántico (I0 = 1e4, muestreo completo) para comparación
sinogram_scaled = sinogram_full / sinogram_full.max() * 2.0
I0 = 1e4
I = I0 * np.exp(-sinogram_scaled)
I_noisy = np.random.poisson(I)
I_noisy[I_noisy == 0] = 1
sinogram_poisson = -np.log(I_noisy / I0)
recon_poisson = iradon(sinogram_poisson, theta=theta_full, filter_name='ramp')
recon_ideal = iradon(sinogram_scaled, theta=theta_full, filter_name='ramp')
error_poisson = recon_poisson - recon_ideal

# --- Visualización comparativa: submuestreo vs ruido cuántico ---
vmin = image.min()
vmax = image.max()

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Fila 1: Reconstrucciones
axes[0, 0].imshow(image, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 0].set_title("Referencia")
axes[0, 0].axis('off')

axes[0, 1].imshow(recon_fbp_sub, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 1].set_title(f"FBP submuestreado ({n_angles} ángulos)")
axes[0, 1].axis('off')

axes[0, 2].imshow(recon_poisson, cmap='gray')
axes[0, 2].set_title(r"FBP con ruido cuántico ($I_0 = 10^4$)")
axes[0, 2].axis('off')

# Fila 2: Errores
axes[1, 0].axis('off')
axes[1, 0].set_title("—")

err_vmax_sub = np.abs(error_fbp_sub).max()
err_vmax_poi = np.abs(error_poisson).max()
err_vmax = max(err_vmax_sub, err_vmax_poi)

rmse_sub = np.sqrt(np.mean(error_fbp_sub**2))
axes[1, 1].imshow(error_fbp_sub, cmap='gray', vmin=-err_vmax, vmax=err_vmax)
axes[1, 1].set_title(f"Error submuestreo\nRMSE = {rmse_sub:.4f}")
axes[1, 1].axis('off')

rmse_poi = np.sqrt(np.mean(error_poisson**2))
axes[1, 2].imshow(error_poisson, cmap='gray', vmin=-err_vmax, vmax=err_vmax)
axes[1, 2].set_title(f"Error ruido cuántico\nRMSE = {rmse_poi:.4f}")
axes[1, 2].axis('off')

plt.suptitle("Comparativa: artefactos por submuestreo angular vs ruido cuántico", fontsize=15)
plt.tight_layout()
plt.show()

# b) Reconstrucción SART con datos submuestreados (50 ángulos)

# SART - 1 iteración
recon_sart1 = iradon_sart(sinogram_sub, theta=theta_sub)
error_sart1 = recon_sart1 - image
rmse_sart1 = np.sqrt(np.mean(error_sart1**2))

# SART - 2 iteraciones
recon_sart2 = iradon_sart(sinogram_sub, theta=theta_sub, image=recon_sart1)
error_sart2 = recon_sart2 - image
rmse_sart2 = np.sqrt(np.mean(error_sart2**2))

# --- Visualización: FBP vs SART (1 iter) vs SART (2 iter) ---
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Fila 1: Reconstrucciones
axes[0, 0].imshow(recon_fbp_sub, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 0].set_title(f"FBP ({n_angles} ángulos)")
axes[0, 0].axis('off')

axes[0, 1].imshow(recon_sart1, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 1].set_title(f"SART 1 iter. ({n_angles} ángulos)")
axes[0, 1].axis('off')

axes[0, 2].imshow(recon_sart2, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 2].set_title(f"SART 2 iter. ({n_angles} ángulos)")
axes[0, 2].axis('off')

# Fila 2: Errores
err_vmax_all = max(np.abs(error_fbp_sub).max(),
                   np.abs(error_sart1).max(),
                   np.abs(error_sart2).max())

axes[1, 0].imshow(error_fbp_sub, cmap='gray', vmin=-err_vmax_all, vmax=err_vmax_all)
axes[1, 0].set_title(f"Error FBP\nRMSE = {rmse_sub:.4f}")
axes[1, 0].axis('off')

axes[1, 1].imshow(error_sart1, cmap='gray', vmin=-err_vmax_all, vmax=err_vmax_all)
axes[1, 1].set_title(f"Error SART 1 iter.\nRMSE = {rmse_sart1:.4f}")
axes[1, 1].axis('off')

axes[1, 2].imshow(error_sart2, cmap='gray', vmin=-err_vmax_all, vmax=err_vmax_all)
axes[1, 2].set_title(f"Error SART 2 iter.\nRMSE = {rmse_sart2:.4f}")
axes[1, 2].axis('off')

plt.suptitle(f"Reconstrucción con {n_angles} proyecciones: FBP vs SART", fontsize=15)
plt.tight_layout()
plt.show()

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='dicom01'></a>
#
# ## <span style="color: #667eea;">4. Reconstrucción MRI</span>
#
# En esta sección se pretende introducir el proceso básico de reconstrucción en MRI a partir del espacio-k, analizando la relación entre muestreo en k-espacio, efecto del submuestreo y artefactos en la imagen.
#
#
# En MRI, la imagen no se adquiere directamente en el espacio de imagen, sino en el **espacio de frecuencias espaciales**, denominado **k-espacio**. 
# La relación entre el k-espacio y la imagen viene dada por la **Transformada de Fourier ($\mathcal{F}$)**.
# La reconstrucción de la imagen consiste en aplicar la Transformada inversa de Fourier a los datos adquirido:
#
# $I(x,y) = \mathcal{F}^{-1}\{ S(k_x, k_y) \}$,
#
# donde $S(k_x, k_y)$ representa los datos adquiridos en el k-espacio.

# %% [markdown]
# ### *4.1. Simulación de datos en el k-espacio (muestreo completo):*
#
# Partiendo de la misma imagen de referencia (fantoma Shepp-Logan) que se considera la magnetización transversal ideal:
#
# 1. Se calcula su k-espacio mediante FFT 2D.
# 2. Se reconstruye la imagen aplicando la IFFT.
#
# Este caso representa una adquisición ideal, sin ruido y con muestreo completo del k-espacio.
#
#
# **Conceptos clave:**
# - El centro del k-espacio contiene la información de bajo contraste.
# - Las altas frecuencias (bordes) se encuentran en la periferia del k-espacio.

# %%
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# Simulación del espacio k mediante la Transformada de Fourier 2D 
k_space = fftshift(fft2(image))

# Reconstrucción directa (aplicación de IFFT 2D)
recon_mri = np.abs(ifft2(ifftshift(k_space)))

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
# k-espacio
im0 = axes[0].imshow(np.log(np.abs(k_space)+1), cmap=plt.cm.Greys_r)
axes[0].set_title("k-espacio (log-magnitud)")
axes[0].axis('off')
# Reconstrucción 
im1 = axes[1].imshow(recon_mri, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción MRI (ideal)")
axes[1].axis('off')

# %% [markdown]
# ### *4.2. Submuestreo cartesiano del k-espacio:*
#
# La MRI es una modalidad de imagen inherentemente lenta. En la práctica clínica, el tiempo de adquisición en MRI puede reducirse **submuestreando el k-espacio**, por ejemplo, adquiriendo solo una de cada varias líneas en la dirección de fase ($k_y$).
#
#
# En esta sección:
# - Se simula un submuestreo cartesiano uniforme del k-espacio.
# - Se reconstruye la imagen mediante IFFT directa.
#
#
# **Resultado esperado:**
# - Aparición de **aliasing periódico (wrap-around)** en la imagen reconstruida.
# - Pérdida de información espacial debido al incumplimiento del criterio de Nyquist.

# %%
# Submuestreo cartesiano uniforme (máscara de submuestreo)
R = 2  # Factor de aceleración (conservar 1 de cada 2 líneas del k-espacio)
mask = np.zeros(k_space.shape)
mask[::R, :] = 1 

# Aplicar máscara de submuestreo al k-espacio
k_space_under = k_space * mask

# Reconstrucción directa (aplicación de IFFT 2D)
recon_under = np.abs(ifft2(ifftshift(k_space_under)))

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
# máscara de submuestreo uniforme
im0 = axes[0].imshow(mask, cmap='gray')
axes[0].set_title("Máscara de submuestreo")
axes[0].axis('off')
# k-espacio submuestreado
im1 = axes[1].imshow(np.log(np.abs(k_space_under)+1), cmap=plt.cm.Greys_r)
axes[1].set_title("k-espacio submuestreado")
axes[1].axis('off')
# Reconstrucción submuestreada
im2 = axes[2].imshow(recon_under, cmap=plt.cm.Greys_r)
axes[2].set_title(f"Reconstrucción MRI submuestreada (R = {int(R)})")
axes[2].axis('off')

# %% [markdown]
# ### *4.3. Reconstrucción Partial Fourier (Half-Fourier):*
#
# En la práctica, es habitual reducir el tiempo de adquisición adquiriendo solo una fracción del k-espacio (se mide poco más de la mitad) en la dirección de fase. Esta técnica se conoce como Half-Fourier o Partial Fourier.
#
# La reconstrucción se basa en la hipótesis de que la imagen final es real (o aproximadamente real), lo que implica simetría conjugada en k-espacio (por las propiedades de la Transformada de Fourier):
#
# $ S(-k) = conj(S(k))$
#
# El resultado de este tipo de aceleración es que la imagen mantiene la resolución, pero pierde relación señal-ruido (SNR).

# %%
# Generar una máscara Half-Fourier
fraction = 0.6 # fracción de líneas adquiridas (por ejemplo, 60%)
N = k_space.shape[0]
num_lines = int(fraction * N)

mask_hf = np.zeros(k_space.shape)
mask_hf[:num_lines, :] = 1

# Aplicar la máscara al k-espacio 
kspace_hf = k_space * mask_hf

# Reconstrucción directa (sin completar k-espacio) 
recon_hf_naive = np.abs(np.fft.ifft2(np.fft.ifftshift(kspace_hf)))

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
# máscara HF
im0 = axes[0].imshow(mask_hf, cmap='gray')
axes[0].set_title(f'Máscara Half-Fourier ({fraction*100:.0f}%)')
axes[0].axis('off')
# k-espacio submuestreado
im1 = axes[1].imshow(np.log(np.abs(kspace_hf)+1), cmap=plt.cm.Greys_r)
axes[1].set_title("k-espacio (Half-Fourier)")
axes[1].axis('off')
# Reconstrucción submuestreada
im2 = axes[2].imshow(recon_hf_naive, cmap=plt.cm.Greys_r)
axes[2].set_title("Reconstrucción Half-Fourier (sin completar)")
axes[2].axis('off')

# %%
# Completar k-espacio por simetría conjugada
kspace_hf_filled = kspace_hf.copy()
for i in range(num_lines, N):
    kspace_hf_filled[i, :] = np.conj(kspace_hf[N - i - 1, ::-1])

# Reconstrucción Half-Fourier (k-espacio completado por simetría conjugada)
recon_hf_filled = np.abs(np.fft.ifft2(np.fft.ifftshift(kspace_hf_filled)))

# Visualización de la reconstrucción
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
# reconstrucción ideal (muestreo completo)
im0 = axes[0].imshow(recon_mri, cmap=plt.cm.Greys_r)
axes[0].set_title("Reconstrucción ideal")
axes[0].axis('off')
# Reconstrucción Half-Fourier (sin completar k-espacio)
im1 = axes[1].imshow(recon_hf_naive, cmap=plt.cm.Greys_r)
axes[1].set_title("Reconstrucción Half-Fourier (sin completar)")
axes[1].axis('off')
# Reconstrucción Half-Fourier (simetría conjugada)
im2 = axes[2].imshow(recon_hf_filled, cmap=plt.cm.Greys_r)
axes[2].set_title("Reconstrucción Half-Fourier (simetría)")
axes[2].axis('off')

# %% [markdown]
# La reconstrucción Half-Fourier basada en simetría conjugada asume una imagen real y sin fase.
# Al no cumplirse estrictamente esta hipótesis, completar el k-espacio aplicando directamente la propiedad de simetría conjugada introduce errores de fase e incosistencias en altas frecuencias que se manifiestan en la imagen como artefactos de Gibbs (efecto ringing) y distorsión de bordes.
#
# El error pasa de ser "falta de información" en la reconstrucción Half-Fourier (sin completar) a "información incorrecta" (compltando con simetría conjugada directamente).
#
# En la práctica real, las reconstrucciones Half-Fourier incluyen una corrección de fase y algoritmos iterativos para evitar estos efectos.

# %% [markdown]
# ### *4.4. Reconstrucción de datos multi-coil:*
#
# La utilización de múltiples bobinas receptoras (coils) en el escáner de resonancia magnética permite capturar datos simultáneamente desde diferentes posiciones espaciales (en paralelo).
#
# Los datos multi-coil permiten acelerar el proceso de adquisición mediante submuestreo del k-espacio y después recuperar la información faltante a partir de la información proporcionada por las distintas bobinas (técnica denominada Parallel Imaging, PI) en el proceso de reconstrucción.
#
# Las bobinas presentan sensibilidad espacial. Cada bobina tiene un "mapa de sensibilidad" específico; es decir, ve mejor la zona del cuerpo que tiene más cerca. 
#
# Los datos multi-coil consisten en múltiples conjuntos de mediciones en el espacio-k, uno por cada elemento de la bobina, que luego deben combinarse.
#
# Si no hay submuestreo, las imágenes de cada bobina se combinan comúnmente mediante la Raíz de la Suma de Cuadrados (Root-Sum-of-Squares, RSS) para maximizar la relación señal-ruido.
#
# En caso de tener datos multi-coil submuestreados, una combinación básica RSS no permite eliminar los artefactos de submuestreo (aliasing) y se necesitan esquemas de reconstrucción más elaborados como SENSE (Sensitivity Encoding), GRAPPA o CS (Compressed Sensing).

# %% [markdown]
# La siguiente función genera mapas de sensibilidad sintéticos adaptados a una determinada geometría (tamaño del objeto).

# %%
import numpy as np

def generate_sensitivity_maps(shape, ncoils):
    Nx, Ny = shape
    x = np.linspace(-1, 1, Nx)
    y = np.linspace(-1, 1, Ny)
    X, Y = np.meshgrid(x, y, indexing='ij')

    sens = []
    angles = np.linspace(0, 2*np.pi, ncoils, endpoint=False)
    for a in angles:
        sx = 0.3 * np.cos(a)
        sy = 0.3 * np.sin(a)
        mag = np.exp(-((X - sx)**2 + (Y - sy)**2) / 0.5)
        phase = np.exp(1j * (X * np.cos(a) + Y * np.sin(a)))
        sens.append(mag * phase)

    return np.stack(sens, axis=-1)


# %% [markdown]
# A continuación, vamos a simular datos multicoil a partir de la imagen de referencia. El proceso será el siguiente:
#
# 1. Simulación de los mapas de sensibilidad utilizando la función definida previamente (`generate_sensitivity_maps`): $S_c(r)$, con $c = 1,...,N_{coils}$)
# 2. Cálculo de las imágenes de cada bobina: $I_c(r) = S_c(r)·I(r)$, siendo $I(r)$ la imagen real
# 3. Simulación del k-espacio mediante FFT 2D
# 4. Reconstrucción por coil
# 5. Combinación RSS para obtener reconstrucción final (estándar clínico) y comparativa con recombinación de canales (coil combination)

# %%
# SIMULACIÓN DATOS MRI MULTI-COIL

N = image.shape[0]  # Tamaño de la imagen de referencia
ncoils = 4          # Número de bobinas

# 1. Generar mapas de sensibilidad sintéticos
sens = generate_sensitivity_maps((N, N), ncoils)

# Visualizamos magnitud y fase de los mapas de sensibilidad generados
fig, axes = plt.subplots(2, ncoils, figsize=(3*ncoils, 6))
for c in range(ncoils):
    # Magnitud
    axes[0, c].imshow(np.abs(sens[..., c]), cmap='viridis')
    axes[0, c].set_title(f"Coil {c+1} | Magnitud")
    axes[0, c].axis('off')
    # Fase
    axes[1, c].imshow(np.angle(sens[..., c]), cmap='twilight')
    axes[1, c].set_title(f"Coil {c+1} | Fase")
    axes[1, c].axis('off')
plt.suptitle("Mapas de sensibilidad de las bobinas", fontsize=14)
plt.tight_layout()
plt.show()

# 2. Simulación de las imágenes en cada bobina (cómo ve el objeto cada coil)
coil_images = image[..., None] * sens

# 3. Simulación de una adquisición multicoil (aplicando FFT 2D a cada coil_image)
kspace_coil = np.zeros_like(coil_images, dtype=complex)
for c in range(ncoils):
    kspace_coil[..., c] = np.fft.fftshift(np.fft.fft2(coil_images[..., c]))

# %%
# RECONSTRUCCIÓN DATOS MRI MULTI-COIL

# 4. Recontrucción de imagen por coil
recon_coil = np.zeros_like(coil_images, dtype=float)
for c in range(ncoils):
    recon_coil[..., c] = np.abs(np.fft.ifft2(np.fft.ifftshift(kspace_coil[..., c])))

fig, axes = plt.subplots(1, ncoils, figsize=(3*ncoils, 3))
for c in range(ncoils):
    axes[c].imshow(recon_coil[..., c], cmap='gray')
    axes[c].set_title(f"Recon. Coil {c+1}")
    axes[c].axis('off')
plt.suptitle("Imágenes reconstruidas por coil", fontsize=14)
plt.tight_layout()
plt.show()

# 5. Combinación RSS básica (estándar)
recon_rss = np.sqrt(np.sum(recon_coil**2, axis=-1))

# Comparamos con coil combination (combinación de máxima versosimilitud, utilizando los mapas de sensibilidad)
numerator = np.sum(np.conj(sens) * recon_coil, axis=-1)
denominator = np.sum(np.abs(sens)**2, axis=-1) + 1e-8
recon_cc = np.abs(numerator / denominator)


fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(image, cmap='gray')
axes[0].set_title("Imagen referencia (ideal)")
axes[0].axis('off')

axes[1].imshow(recon_rss, cmap='gray')
axes[1].set_title("RSS")
axes[1].axis('off')

axes[2].imshow(recon_cc, cmap='gray')
axes[2].set_title("Coil combination")
axes[2].axis('off')

plt.tight_layout()
plt.show()


# %% [markdown]
# La combinación RSS mejora la SNR respecto a un único coil, pero ignora la información de fase y la intensidad final no es uniforme espacialmente.
#
# Por otro lado, la recombinación de canales teniendo en cuenta los mapas de sensibilidad (coil combination) utiliza información de magnitud y fase de las bobinas proporcinando una imagen más homogénea. 
# En este caso, se maximiza la SNR bajo supuestos ideales, pero es sensible a errores en los mapas de sensibilidad.

# %% [markdown]
# <div style="page-break-before: always;"></div>
#
# <hr style="border: none; border-top: 2px solid #667eea; margin: 30px 0;">
# <a class='anchor' id='dicom01'></a>
#
# ## <span style="color: #667eea;">5. Ejercicios prácticos: MRI</span>

# %% [markdown]
# ### *Ejercicio 4. Efecto del submuestreo del k-espacio*
#
# Partiendo del k-espacio completo del fantoma de Shepp–Logan:
#
# 1. Simular un submuestreo cartesiano uniforme para distintos factores de aceleración (R = 2, 4 y 8)
#
# 2. Reconstruir en cada caso la imagen mediante IFFT directa
#
# 3. Comparar visualmente las imágenes reconstruidas con la reconstrucción completa

# %%
# SOLUCIÓN DEL EJERCICIO 4

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# k-espacio completo (ya calculado previamente)
k_space = fftshift(fft2(image))

# Reconstrucción ideal (muestreo completo)
recon_ideal = np.abs(ifft2(ifftshift(k_space)))

# Factores de aceleración
R_values = [2, 4, 8]

# Almacenar reusltados
masks = []
recons = []
errors = []

for R in R_values:
    # 1. Máscara de submuestreo cartesiano uniforme
    mask = np.zeros(k_space.shape)
    mask[::R, :] = 1
    masks.append(mask)

    # Aplicar máscara al k-espacio
    k_space_under = k_space * mask

    # 2. Reconstrucción mediante IFFT directa
    recon = np.abs(ifft2(ifftshift(k_space_under)))
    recons.append(recon)

    # Error respecto a la reconstrucción ideal
    errors.append(recon - recon_ideal)

# --- 3. Visualización comparativa ---
vmin = recon_ideal.min()
vmax = recon_ideal.max()

# Fila 1: Máscaras | Fila 2: Reconstrucciones | Fila 3: Errores
fig, axes = plt.subplots(3, len(R_values) + 1, figsize=(5 * (len(R_values) + 1), 15))

# Columna 0: Referencia (muestreo completo)
axes[0, 0].imshow(np.ones(k_space.shape), cmap='gray', vmin=0, vmax=1)
axes[0, 0].set_title("Máscara completa (R=1)")
axes[0, 0].axis('off')

axes[1, 0].imshow(recon_ideal, cmap='gray', vmin=vmin, vmax=vmax)
axes[1, 0].set_title("Reconstrucción ideal (R=1)")
axes[1, 0].axis('off')

axes[2, 0].axis('off')
axes[2, 0].set_title("-")

# Columnas 1..3: Para cada factor R
err_vmax = max(np.abs(e).max() for e in errors)

for i, R in enumerate(R_values):
    # Máscara de submuestreo
    axes[0, i+1].imshow(masks[i], cmap='gray', vmin=0, vmax=1)
    n_lines = int(masks[i].sum() / k_space.shape[1])
    axes[0, i+1].set_title(f"Máscara R={R}\n({n_lines} líneas de {k_space.shape[0]})")
    axes[0, i+1].axis('off')

    # Reconstrucción submuestreada
    axes[1, i+1].imshow(recons[i], cmap='gray', vmin=vmin, vmax=vmax)
    axes[1, i+1].set_title(f"Reconstrucción R={R}")
    axes[1, i+1].axis('off')

    # Error
    rmse = np.sqrt(np.mean(errors[i]**2))
    axes[2, i+1].imshow(errors[i], cmap='gray', vmin=-err_vmax, vmax=err_vmax)
    axes[2, i+1].set_title(f"Error R={R}\nRMSE = {rmse:.4f}")
    axes[2, i+1].axis('off')

plt.suptitle("Efecto del submuestreo cartesiano uniforme del k-espacio", fontsize=16)
plt.tight_layout()
plt.show()

# %% [markdown]
# ### *Ejercicio 5. Submuestreo no uniforme del k-espacio*
#
# Analizar el efecto de un submuestreo no uniforme del k-espacio, priorizando la adquisición de bajas frecuencias espaciales.
#
# 1. Diseñar una máscara de submuestreo cartesiano con muestreo denso en el centro del k-espacio (por ejemplo, un 15% de las líneas adquiridas) y progresivamente más disperso hacia las altas frecuencias (con densidad decreciente)
# 2. Ajustar la máscara para que el número total de líneas adquiridas sea similar al caso uniforme con R = 4
# 3. Reconstruir la imagen mediante IFFT 2D directa
# 4. Comparar el resultado con la reconstrucción con submuetreo uniforme del apartado anterior para el mismo factor de aceleración

# %%
# SOLUCIÓN DEL EJERCICIO 5

import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import fft2, ifft2, fftshift, ifftshift

# k-espacio completo (ya calculado previamente)
k_space = fftshift(fft2(image))
N = k_space.shape[0]

# Reconstrucción ideal (muestreo completo)
recon_ideal = np.abs(ifft2(ifftshift(k_space)))

# --- Número objetivo de líneas (equivalente a R=4) ---
target_lines = N // 4

# --- 1. Diseño de la máscara no uniforme ---
# Centro denso: 15% de las líneas centrales se adquieren todas
center_fraction = 0.15
center_half = int(center_fraction * N / 2)
center_start = N // 2 - center_half
center_end = N // 2 + center_half
n_center_lines = center_end - center_start

# Líneas restantes a adquirir en la periferia
n_peripheral_lines = target_lines - n_center_lines

# Índices periféricos (fuera de la banda central)
peripheral_indices = np.concatenate([
    np.arange(0, center_start),
    np.arange(center_end, N)
])

# Densidad decreciente: probabilidad proporcional a 1/distancia al centro
distances = np.abs(peripheral_indices - N // 2).astype(float)
prob = 1.0 / (distances + 1)  # +1 para evitar división por cero
prob /= prob.sum()  # Normalizar

# Seleccionar líneas periféricas según densidad decreciente
np.random.seed(42)  # Reproducibilidad
n_peripheral_lines = max(0, min(n_peripheral_lines, len(peripheral_indices)))
selected_peripheral = np.random.choice(
    peripheral_indices, size=n_peripheral_lines, replace=False, p=prob
)

# Construir máscara no uniforme
mask_nu = np.zeros(k_space.shape)
mask_nu[center_start:center_end, :] = 1  # Centro denso
mask_nu[selected_peripheral, :] = 1       # Periferia dispersa

total_lines_nu = int(mask_nu[:, 0].sum())

# --- 2. Máscara uniforme R=4 para comparación ---
R = 4
mask_uniform = np.zeros(k_space.shape)
mask_uniform[::R, :] = 1
total_lines_uniform = int(mask_uniform[:, 0].sum())

# --- 3. Aplicar máscaras y reconstruir ---
# No uniforme
k_space_nu = k_space * mask_nu
recon_nu = np.abs(ifft2(ifftshift(k_space_nu)))
error_nu = recon_nu - recon_ideal

# Uniforme R=4
k_space_uniform = k_space * mask_uniform
recon_uniform = np.abs(ifft2(ifftshift(k_space_uniform)))
error_uniform = recon_uniform - recon_ideal

# --- 4. Visualización comparativa ---
vmin = recon_ideal.min()
vmax = recon_ideal.max()

# Máscaras
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
axes[0].imshow(mask_uniform, cmap='gray')
axes[0].set_title(f"Máscara uniforme R={R}\n({total_lines_uniform} líneas)")
axes[0].axis('off')

axes[1].imshow(mask_nu, cmap='gray')
axes[1].set_title(f"Máscara no uniforme\n({total_lines_nu} líneas)")
axes[1].axis('off')

# Perfil 1D de las máscaras (líneas adquiridas en función de ky)
axes[2].stem(np.arange(N), mask_uniform[:, 0], linefmt='b-', markerfmt='b.', basefmt=' ',
             label=f'Uniforme ({total_lines_uniform} lín.)')
axes[2].stem(np.arange(N), mask_nu[:, 0] * 0.8, linefmt='r-', markerfmt='r.', basefmt=' ',
             label=f'No uniforme ({total_lines_nu} lín.)')
axes[2].set_xlabel('Índice $k_y$')
axes[2].set_ylabel('Adquirida')
axes[2].set_title('Perfil de muestreo')
axes[2].legend()
axes[2].set_xlim([0, N])

plt.suptitle("Comparativa de máscaras de submuestreo", fontsize=15)
plt.tight_layout()
plt.show()

# Reconstrucciones y errores
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Fila 1: Reconstrucciones
axes[0, 0].imshow(recon_ideal, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 0].set_title("Reconstrucción ideal (R=1)")
axes[0, 0].axis('off')

axes[0, 1].imshow(recon_uniform, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 1].set_title(f"Uniforme R={R}\n({total_lines_uniform} líneas)")
axes[0, 1].axis('off')

axes[0, 2].imshow(recon_nu, cmap='gray', vmin=vmin, vmax=vmax)
axes[0, 2].set_title(f"No uniforme\n({total_lines_nu} líneas)")
axes[0, 2].axis('off')

# Fila 2: Errores
err_vmax = max(np.abs(error_uniform).max(), np.abs(error_nu).max())

axes[1, 0].axis('off')
axes[1, 0].set_title("—")

rmse_uniform = np.sqrt(np.mean(error_uniform**2))
axes[1, 1].imshow(error_uniform, cmap='gray', vmin=-err_vmax, vmax=err_vmax)
axes[1, 1].set_title(f"Error uniforme R={R}\nRMSE = {rmse_uniform:.4f}")
axes[1, 1].axis('off')

rmse_nu = np.sqrt(np.mean(error_nu**2))
axes[1, 2].imshow(error_nu, cmap='gray', vmin=-err_vmax, vmax=err_vmax)
axes[1, 2].set_title(f"Error no uniforme\nRMSE = {rmse_nu:.4f}")
axes[1, 2].axis('off')

plt.suptitle("Submuestreo uniforme vs no uniforme (mismo número de líneas ≈ R=4)", fontsize=15)
plt.tight_layout()
plt.show()

