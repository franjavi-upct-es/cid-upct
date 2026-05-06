# Guía completa — Prácticas 3 y 4 de Deep Learning

> Asignatura: **Deep Learning** — Grado en Ciencia e Ingeniería de Datos (UPCT /
> UMU) Material cubierto: Práctica 3 (Transformers) + Práctica 4
> (Autocodificadores). Esta guía está pensada como **referencia de consulta
> rápida**: tipos de problema, palabras clave para reconocerlos, recetas de
> código comentadas y referencia cruzada de qué archivo abrir cuando busques
> algo concreto.

---

## 0. Índice de archivos y mapa de consulta rápida

| #   | Archivo                  | Tema                                              | Dataset                     | Modelo principal     |
| --- | ------------------------ | ------------------------------------------------- | --------------------------- | -------------------- |
| 1   | `p3_sesion1.ipynb`       | Codificación de secuencias de caracteres + MLP    | Péptidos AMP / no-AMP (CSV) | `MLP` baseline       |
| 2   | `p3_sesion2.ipynb`       | RNN bidireccional + Embedding                     | Mismos péptidos             | `BiLSTM`             |
| 3   | `p3_sesion3.ipynb`       | Transformer encoder propio + Embedding posicional | Mismos péptidos             | `Transformer` custom |
| 4   | `DL_p4_AE_sesion1.ipynb` | Autoencoder totalmente conectado para anomalías   | ECG5000 (series temporales) | `AE` denso           |
| 5   | `DL_p4_AE_sesion2.ipynb` | Sparse AE + Convolutional AE + coloreado          | CelebA 64x64                | `CAE`                |
| 6   | `DL_p4_AE_sesion3.ipynb` | Variational Autoencoder (VAE)                     | CelebA 64x64                | `VAE`                |

### ¿Dónde busco…?

| Si necesitas…                                                      | Mira en…                                    |
| ------------------------------------------------------------------ | ------------------------------------------- |
| Cargar y fusionar dos CSVs con etiqueta                            | `p3_sesion1.ipynb` (E1)                     |
| Stratified split 80/20 con `train_test_split`                      | `p3_sesion1.ipynb` (E2)                     |
| `TextVectorization` con `multi_hot` / `tf_idf` / `int` / n-gramas  | `p3_sesion1.ipynb`                          |
| Codificación **integer** y secuencias 3D para LSTM                 | `p3_sesion2.ipynb` (E1, E2)                 |
| `tf.one_hot` aplicado sobre un tensor de enteros                   | `p3_sesion2.ipynb` (E3)                     |
| Capa `Embedding` con `mask_zero`                                   | `p3_sesion2.ipynb` (E4), `p3_sesion3.ipynb` |
| Visualizar un embedding en 2D con PCA                              | `p3_sesion2.ipynb` (E6)                     |
| Implementar tu propia clase `Layer` (con `get_config`, máscaras)   | `p3_sesion3.ipynb` (E1, E4)                 |
| `MultiHeadAttention` + LayerNorm + residual                        | `p3_sesion3.ipynb` (E1)                     |
| Embedding posicional aprendido                                     | `p3_sesion3.ipynb` (E4)                     |
| `EarlyStopping` + `ReduceLROnPlateau` + `ModelCheckpoint`          | `p3_sesion1.ipynb`, `p3_sesion3.ipynb`      |
| Búsqueda de hiperparámetros por rejilla con repeticiones           | `p3_sesion3.ipynb` (E7)                     |
| Diseño de pirámide encoder/decoder densa                           | `DL_p4_AE_sesion1.ipynb` (E2)               |
| Detectar anomalías por **umbral en el error de reconstrucción**    | `DL_p4_AE_sesion1.ipynb` (E3, E4)           |
| `SpecificityAtSensitivity` y `StandardScaler`                      | `DL_p4_AE_sesion1.ipynb` (E5)               |
| Sparse AE con regularizador `activity_regularizer=l1`              | `DL_p4_AE_sesion2.ipynb` (E2)               |
| Convolutional AE 2D con `Conv2DTranspose`                          | `DL_p4_AE_sesion2.ipynb` (E3, E4)           |
| Coloreado gris→RGB                                                 | `DL_p4_AE_sesion2.ipynb` (E5)               |
| Reparametrization trick (`Sampling` layer)                         | `DL_p4_AE_sesion3.ipynb` (E1)               |
| `train_step` custom con pérdida combinada (recon + KL)             | `DL_p4_AE_sesion3.ipynb` (E1)               |
| Generación de imágenes desde el espacio latente                    | `DL_p4_AE_sesion3.ipynb` (E2)               |
| Estudio aislado de `latent_dim` y `kl_weight`                      | `DL_p4_AE_sesion3.ipynb` (E3)               |
| Comprobar gaussianidad del latente (PCA + histograma + normaltest) | `DL_p4_AE_sesion3.ipynb` (E4)               |
| Data augmentation con espejado horizontal + `tf.data` con shuffle  | `DL_p4_AE_sesion3.ipynb` (E5)               |

---

# PARTE 1 — PRÁCTICA 3: Transformers y procesamiento de secuencias

## 1.1 Tipos de problemas que se resuelven

Todos los ejercicios giran alrededor de un mismo problema **supervisado de
clasificación binaria**: dado un péptido representado como cadena de caracteres
(cada carácter = un aminoácido), predecir si tiene actividad antimicrobiana
(AMP=1) o no (AMP=0).

Dentro de ese problema general aparecen tres familias de subproblemas que
conviene saber distinguir, porque cada uno se resuelve con una arquitectura
distinta:

1. **Bag-of-tokens (sin orden).** El modelo solo ve qué tokens aparecen y/o con
   qué frecuencia, no en qué orden. Lo resolvemos con **MLP** alimentado por
   `multi_hot` o `tf_idf` (P3 sesión 1).
2. **Secuencia con dependencia de orden.** El orden importa. Lo resolvemos con
   **RNN bidireccional (BiLSTM)** sobre codificación integer + embedding (P3
   sesión 2).
3. **Secuencia con dependencias largas y contextuales.** Mismo objetivo, pero
   usando atención multi-cabeza para que cada token construya su representación
   a partir de todos los demás. Lo resolvemos con **Transformer encoder** +
   embedding posicional (P3 sesión 3).

## 1.2 Palabras clave para identificar la estructura del código

Cuando leas un enunciado, estas pistas te dicen qué patrón aplicar:

- **"clasificar / predecir si"** → salida `Dense(1, activation="sigmoid")` +
  `loss="binary_crossentropy"`.
- **"codificación multi-hot / TF-IDF / bag-of-words"** →
  `TextVectorization(output_mode=...)` + MLP. Sin orden.
- **"codificación integer / preserva orden"** →
  `TextVectorization(output_mode="int", output_sequence_length=max_len)`.
  Necesario para RNN/Transformer.
- **"unigramas / bigramas / n-gramas"** → parámetro `ngrams=(2,2)` de
  `TextVectorization`.
- **"vocabulario más rico" / "palabras similares cercanas"** → capa `Embedding`.
- **"recurrente / dependencia temporal / secuencial"** → `LSTM`, normalmente
  envuelto en `Bidirectional(...)`.
- **"contexto / atención"** → `MultiHeadAttention` dentro de un Transformer
  encoder.
- **"sensible al orden / posición"** → `MyPositionEmbedding` (embedding de
  tokens + embedding de posiciones, sumados).
- **"capa personalizada"** → heredar de `keras.layers.Layer`, implementar
  `__init__`, `call`, `compute_mask`, `get_config`.
- **"ajusta hiperparámetros / busca configuración óptima"** → grid search con
  `repeats` para cuantificar varianza (P3 sesión 3 E7).

## 1.3 Esqueleto común a las tres sesiones

Las tres sesiones comparten preámbulo. Si lo memorizas, ahorras mucho tiempo:

```python
# === IMPORTS ESTÁNDAR ===
import os, random
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers

# === REPRODUCIBILIDAD ===
# Fija las tres semillas (np, random, tf). Imprescindible para comparar
# configuraciones de forma justa entre ejecuciones.
seed = 42
np.random.seed(seed)
random.seed(seed)
tf.random.set_seed(seed)

# === CARGA Y FUSIÓN DE DATOS (P3) ===
df_non = pd.read_csv("data/in/non_amp_ampep_cdhit90.csv", index_col=0)
df_amp = pd.read_csv("data/in/veltri_dramp_cdhit_90.csv",  index_col=0)
df = pd.concat([df_non, df_amp], axis=0, ignore_index=True)

# Limpieza: a string, sin espacios, mayúsculas (los AAs son letras mayúscula)
df["aa_seq"] = df["aa_seq"].astype(str).str.strip().str.upper()
df["AMP"]    = df["AMP"].astype(int)

# Listas paralelas: secuencia (str) y etiqueta (0/1)
X = df["aa_seq"].to_numpy()
y = df["AMP"].to_numpy()

# === SPLIT ESTRATIFICADO 80/20 ===
# stratify=y mantiene la proporción AMP / no-AMP en train y test.
X_train_text, X_test_text, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=seed, stratify=y
)

# Longitud máxima en train -> se usará como output_sequence_length.
# Importante: calcularla SOLO con train para evitar "fuga" de información de test.
max_len = max(len(s) for s in X_train_text)
```

## 1.4 Codificaciones de texto disponibles (referencia rápida)

`TextVectorization` (módulo `keras.layers`) cubre prácticamente todos los modos.
La elección depende del modelo posterior:

```python
# --- Multi-hot (presencia 0/1 por token; descarta orden y frecuencia) ---
# Salida: vector binario de tamaño |vocabulario|.
# Útil con MLP cuando solo importa "qué AAs aparecen".
vec_mh = layers.TextVectorization(
    standardize=None,    # NO modificar el texto (cada AA es relevante tal cual)
    split="character",   # tokenización carácter a carácter
    output_mode="multi_hot",
)
vec_mh.adapt(X_train_text)               # aprende vocabulario solo en train
X_train_mh = vec_mh(tf.constant(X_train_text)).numpy()

# --- TF-IDF (presencia ponderada por frecuencia) ---
# Suele mejorar a multi-hot si los AAs muy frecuentes son menos discriminativos.
vec_tfidf = layers.TextVectorization(
    standardize=None, split="character", output_mode="tf_idf"
)

# --- N-gramas (captura patrones LOCALES de orden) ---
# ngrams=(2,2) genera SOLO bigramas; (1,2) genera unigramas + bigramas.
# Cuidado: el vocabulario crece muchísimo -> primera capa Dense con muchos params.
vec_bi = layers.TextVectorization(
    standardize=None, split="character", output_mode="tf_idf", ngrams=(2, 2)
)

# --- Integer (preserva ORDEN; obligatorio para RNN / Transformer) ---
# output_sequence_length fija el padding. Las secuencias más cortas se rellenan con 0.
vec_int = layers.TextVectorization(
    standardize=None, split="character",
    output_mode="int", output_sequence_length=max_len,
)
vec_int.adapt(X_train_text)
X_train_int = vec_int(tf.constant(X_train_text)).numpy()
vocab_int   = vec_int.get_vocabulary()
vocab_size  = len(vocab_int)
```

> **Truco mental:** integer + `mask_zero=True` en la siguiente capa de Embedding
> propaga automáticamente la máscara de padding. Sin máscara, el modelo aprende
> "ruido" sobre los ceros de relleno.

## 1.5 Modelo 1 — MLP baseline (P3 sesión 1, E4–E8)

**Cuándo usarlo:** primer baseline rápido cuando solo importa la **presencia**
de tokens.

```python
# Pirámide decreciente clásica: 512 -> 256 -> 128 -> 64 -> 1
mlp = keras.Sequential([
    layers.Input(shape=(dim_input,)),    # dim_input = tamaño del vector codificado
    layers.Dense(512, activation="relu"),
    layers.Dense(256, activation="relu"),
    layers.Dense(128, activation="relu"),
    layers.Dense( 64, activation="relu"),
    layers.Dense(  1, activation="sigmoid"),  # binaria
], name="MLP_baseline")

mlp.compile(optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"])

# === Entrenamiento con CHECKPOINT del mejor modelo según val_accuracy ===
os.makedirs("models", exist_ok=True)
ckpt = keras.callbacks.ModelCheckpoint(
    filepath="models/best_mlp.keras",
    monitor="val_accuracy",
    mode="max",
    save_best_only=True,   # solo guarda si mejora la métrica monitorizada
    verbose=1,
)
hist = mlp.fit(X_train_enc, y_train,
               validation_split=0.2,    # 20% del train para validar
               epochs=60, batch_size=32,
               callbacks=[ckpt], verbose=1)

# Cargar el "mejor" pesos antes de evaluar para no quedarte con los sobreajustados
best = keras.models.load_model("models/best_mlp.keras")
loss, acc = best.evaluate(X_test_enc, y_test, verbose=0)
```

## 1.6 Modelo 2 — BiLSTM (P3 sesión 2)

**Cuándo usarlo:** cuando el orden de los tokens importa pero las secuencias no
son muy largas. Bidireccional porque cada AA puede depender del contexto a su
izquierda **y** derecha.

```python
from keras.layers import LSTM, Bidirectional, Embedding, Dense, Input

# --- Variante 1: integer "crudo" -> 3D ---
# LSTM espera (batch, timesteps, features). Si features=1, expand_dims:
X_train_int_3d = np.expand_dims(X_train_int, -1)  # (N, max_len, 1)

model_int = keras.Sequential([
    Input(shape=(max_len, 1)),
    Bidirectional(LSTM(50)),       # 50 celdas LSTM, ida y vuelta
    Dense(1, activation="sigmoid"),
], name="LSTM_Integer")

# --- Variante 2: one-hot ---
# Mejor que integer "pelado" porque elimina jerarquía numérica falsa entre AAs.
# Pero NO escalable a lenguaje natural (vocabularios enormes -> matrices gigantes).
X_train_oh = tf.one_hot(X_train_int, depth=vocab_size).numpy()  # (N, max_len, V)

# --- Variante 3 (recomendada): embedding aprendido + mask_zero ---
# mask_zero=True hace que el padding (token 0) NO contribuya al gradiente.
model_emb = keras.Sequential([
    Input(shape=(max_len,)),
    Embedding(input_dim=vocab_size, output_dim=16, mask_zero=True),
    Bidirectional(LSTM(50)),
    Dense(1, activation="sigmoid"),
], name="LSTM_Embedding")

model_emb.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])
model_emb.fit(X_train_int, y_train, validation_split=0.2,
              epochs=10, batch_size=32, verbose=1)
```

### Visualizar el embedding en 2D (P3 sesión 2, E6)

```python
from sklearn.decomposition import PCA

# Pesos del Embedding: matriz (vocab_size, 16) - una fila por token.
embedding_weights = model_emb.layers[0].get_weights()[0]

# Reducción de 16D a 2D para inspección visual.
pca = PCA(n_components=2)
embedding_2d = pca.fit_transform(embedding_weights)

plt.figure(figsize=(10, 8))
for i, token in enumerate(vocab_int):
    if token in ("", "[UNK]"):     # ignora padding y desconocidos
        continue
    x, y_ = embedding_2d[i]
    plt.scatter(x, y_, s=50)
    plt.annotate(token, (x + 0.02, y_ - 0.01), fontsize=12)
plt.title("Proyección 2D del Embedding de Aminoácidos")
plt.xlabel("PC1"); plt.ylabel("PC2"); plt.grid(True); plt.show()
```

## 1.7 Modelo 3 — Transformer encoder propio (P3 sesión 3)

Este es el bloque más reutilizable de toda la práctica. Memorízalo: cualquier
`MyTransformerEncoder` que escribas en otro proyecto seguirá esta plantilla.

```python
@keras.utils.register_keras_serializable(package="custom")
class MyTransformerEncoder(layers.Layer):
    """
    Bloque encoder estándar:
      x -> MultiHeadAttention -> dropout -> + residual -> LayerNorm
        -> Dense (relu) -> Dense -> dropout -> + residual -> LayerNorm
    Soporta máscaras propagadas desde un Embedding(mask_zero=True).
    """
    def __init__(self, embed_dim, dense_dim, num_heads, dropout=0.1, **kwargs):
        super().__init__(**kwargs)
        # embed_dim DEBE ser divisible entre num_heads:
        # cada cabeza recibe (embed_dim // num_heads) dimensiones.
        if embed_dim % num_heads != 0:
            raise ValueError("embed_dim debe ser divisible por num_heads.")

        # Hiperparámetros (los guardamos para get_config / serialización).
        self.embed_dim = embed_dim
        self.dense_dim = dense_dim
        self.num_heads = num_heads
        self.dropout   = dropout

        # Indica a Keras que esta capa propaga máscaras hacia adelante.
        self.supports_masking = True

        # Auto-atención multi-cabeza.
        self.attention = layers.MultiHeadAttention(
            num_heads=num_heads,
            key_dim=embed_dim // num_heads,
            dropout=dropout,
        )

        # FFN del transformer: Dense expansivo -> Dense de vuelta a embed_dim
        # (necesario para que la conexión residual sume dimensiones compatibles).
        self.dense_proj = keras.Sequential([
            layers.Dense(dense_dim, activation="relu"),
            layers.Dense(embed_dim),
        ])

        self.dropout_1 = layers.Dropout(dropout)
        self.dropout_2 = layers.Dropout(dropout)
        self.layernorm_1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm_2 = layers.LayerNormalization(epsilon=1e-6)

    def call(self, inputs, mask=None, training=None):
        # MultiHeadAttention espera la máscara en forma (batch, 1, seq_len)
        # para hacer broadcasting sobre las cabezas. Por eso añadimos un eje.
        attention_mask = None
        if mask is not None:
            attention_mask = tf.cast(mask[:, tf.newaxis, :], dtype=tf.bool)

        # En un encoder, query=key=value (auto-atención).
        attn = self.attention(
            query=inputs, key=inputs, value=inputs,
            attention_mask=attention_mask, training=training,
        )
        attn = self.dropout_1(attn, training=training)
        out_1 = self.layernorm_1(inputs + attn)        # residual + norm

        proj = self.dense_proj(out_1, training=training)
        proj = self.dropout_2(proj, training=training)
        return self.layernorm_2(out_1 + proj)          # residual + norm

    def compute_mask(self, inputs, mask=None):
        # Reenvía la máscara hacia capas posteriores que también la necesiten.
        return mask

    def get_config(self):
        # Necesario para guardar/cargar el modelo con la capa custom.
        cfg = super().get_config()
        cfg.update(dict(
            embed_dim=self.embed_dim, dense_dim=self.dense_dim,
            num_heads=self.num_heads, dropout=self.dropout,
        ))
        return cfg
```

### Embedding posicional aprendido (P3 sesión 3, E4)

Sin él, el Transformer es **insensible al orden** (defecto grave en secuencias).
La idea es sumar dos embeddings: uno del token y otro de su posición absoluta.

```python
@keras.utils.register_keras_serializable(package="custom")
class MyPositionEmbedding(layers.Layer):
    def __init__(self, sequence_length, input_dim, output_dim,
                 mask_zero=True, **kwargs):
        super().__init__(**kwargs)
        self.sequence_length = sequence_length
        self.input_dim   = input_dim    # tamaño de vocabulario
        self.output_dim  = output_dim   # dimensión del embedding
        self.mask_zero   = mask_zero
        self.supports_masking = True

        # Embedding de tokens (con máscara de padding).
        self.token_embeddings = layers.Embedding(
            input_dim=input_dim, output_dim=output_dim, mask_zero=mask_zero
        )
        # Embedding APRENDIDO de posiciones [0..seq_len-1].
        self.position_embeddings = layers.Embedding(
            input_dim=sequence_length, output_dim=output_dim
        )

    def call(self, inputs):
        length = tf.shape(inputs)[-1]
        positions = tf.range(start=0, limit=length, delta=1)
        # Suma directa: cada vector token recibe el "sello" de su posición.
        return self.token_embeddings(inputs) + self.position_embeddings(positions)

    def compute_mask(self, inputs, mask=None):
        # Propagamos la máscara que calcula el Embedding de tokens.
        return self.token_embeddings.compute_mask(inputs)

    def get_config(self):
        cfg = super().get_config()
        cfg.update(dict(
            sequence_length=self.sequence_length,
            input_dim=self.input_dim,
            output_dim=self.output_dim,
            mask_zero=self.mask_zero,
        ))
        return cfg
```

### Clasificador completo basado en Transformer

```python
def build_transformer_classifier(vocab_size, max_len,
                                 embed_dim=64, dense_dim=128, num_heads=4,
                                 dropout=0.2, lr=1e-3, use_positional=False):
    inputs = keras.Input(shape=(max_len,), dtype="int32")

    # Embedding (con o sin posición). Activar mask_zero=True para padding.
    if use_positional:
        x = MyPositionEmbedding(sequence_length=max_len,
                                input_dim=vocab_size,
                                output_dim=embed_dim,
                                mask_zero=True)(inputs)
    else:
        x = layers.Embedding(input_dim=vocab_size, output_dim=embed_dim,
                             mask_zero=True)(inputs)

    # Bloque Transformer custom.
    x = MyTransformerEncoder(embed_dim, dense_dim, num_heads, dropout)(x)

    # Pooling temporal -> vector fijo por secuencia.
    x = layers.GlobalMaxPooling1D()(x)
    x = layers.Dropout(dropout)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)

    model = keras.Model(inputs, outputs, name="transformer_classifier")
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr),
                  loss="binary_crossentropy",
                  metrics=["accuracy", keras.metrics.AUC(name="auc")])
    return model
```

## 1.8 Callbacks recomendados (P3 sesión 3)

```python
def make_callbacks():
    """
    EarlyStopping  -> corta el entrenamiento si val_auc no mejora en 5 épocas.
                       restore_best_weights=True deja los pesos del MEJOR estado.
    ReduceLROnPlateau -> si val_auc se estanca 2 épocas, reduce el LR a la mitad
                          (fino para escapar de mesetas).
    """
    return [
        keras.callbacks.EarlyStopping(
            monitor="val_auc", mode="max",
            patience=5, restore_best_weights=True
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_auc", mode="max",
            factor=0.5, patience=2, min_lr=1e-5,
        ),
    ]
```

## 1.9 Grid search con repeticiones (P3 sesión 3, E7)

Patrón muy reutilizable cuando te piden "ajusta hiperparámetros":

```python
def train_eval_once(model, X_tr, y_tr, X_te, y_te, epochs=40, batch_size=64):
    """Entrena UNA vez y devuelve métricas de test + tiempo."""
    import time
    t0 = time.time()
    hist = model.fit(X_tr, y_tr, validation_split=0.2,
                     epochs=epochs, batch_size=batch_size,
                     callbacks=make_callbacks(), verbose=0)
    train_time = time.time() - t0
    test_metrics = model.evaluate(X_te, y_te, return_dict=True, verbose=0)
    return {
        "accuracy": float(test_metrics["accuracy"]),
        "auc":      float(test_metrics["auc"]),
        "best_val_accuracy": float(np.max(hist.history["val_accuracy"])),
        "best_val_auc":      float(np.max(hist.history["val_auc"])),
        "train_time_s":      float(train_time),
    }

def run_grid(builder_fn, grid, repeats=2, base_seed=42):
    """
    Para cada configuración del grid, entrena `repeats` veces (con semilla
    distinta) y reporta media + std. Esto es CLAVE para no caer en falsas
    diferencias debidas al ruido de inicialización.
    """
    rows = []
    for cfg in grid:
        runs = []
        for r in range(repeats):
            keras.backend.clear_session()                # libera grafo previo
            np.random.seed(base_seed + r); random.seed(base_seed + r)
            tf.random.set_seed(base_seed + r)
            model = builder_fn(**cfg)
            runs.append(train_eval_once(model, X_train_int, y_train,
                                        X_test_int, y_test))
        row = dict(cfg)
        for m in ["accuracy","auc","best_val_accuracy","best_val_auc","train_time_s"]:
            vals = [r[m] for r in runs]
            row[f"{m}_mean"] = float(np.mean(vals))
            row[f"{m}_std"]  = float(np.std(vals))
        rows.append(row)
    return pd.DataFrame(rows).sort_values("auc_mean", ascending=False).reset_index(drop=True)
```

---

# PARTE 2 — PRÁCTICA 4: Autocodificadores

## 2.1 Tipos de problemas que resuelve un autoencoder

Un autoencoder no se ajusta a un único problema, sino a una **familia** de
problemas en los que necesitas una representación compacta:

1. **Detección de anomalías** (sesión 1). Entrenas SOLO con datos normales. Las
   anomalías producen errores de reconstrucción altos → umbralizas el error.
2. **Reducción de dimensionalidad / compresión** (sesión 1, sesión 2). Mide
   compresión = `latent_dim / input_dim`.
3. **Eliminación de ruido / denoising**. (Mencionado pero no implementado en P4;
   sería entrenar `AE(x_ruidoso) → x_limpio`.)
4. **Coloreado y traducción imagen→imagen** (sesión 2 E5). Cambias el target del
   decoder: `images_gray → images_RGB`.
5. **Generación de muestras nuevas** (sesión 3, VAE). El espacio latente se
   fuerza a una distribución conocida y se puede muestrear.
6. **Sparse coding** (sesión 2 E2). Pocas neuronas activas en el espacio latente
   → mejor interpretabilidad.

## 2.2 Palabras clave para identificar el tipo de AE

| Si el enunciado dice…                                           | Tipo y archivo                                     |
| --------------------------------------------------------------- | -------------------------------------------------- |
| "detecte anomalías", "ECG normal vs anómalo", "umbral de error" | AE denso → `DL_p4_AE_sesion1.ipynb`                |
| "regularización L1 / dispersión / sparse"                       | Sparse AE → `DL_p4_AE_sesion2.ipynb` E2            |
| "imagen", "Conv2D", "campo receptivo", "kernel_size"            | CAE → `DL_p4_AE_sesion2.ipynb` E3–E5               |
| "colorear", "gris a RGB"                                        | CAE asimétrico → `DL_p4_AE_sesion2.ipynb` E5       |
| "generativo", "muestrear", "distribución gaussiana", "KL"       | VAE → `DL_p4_AE_sesion3.ipynb`                     |
| "reparametrización", "z_mean, z_log_var"                        | VAE (Sampling layer) → `DL_p4_AE_sesion3.ipynb` E1 |

## 2.3 Patrón general: encoder + decoder + autoencoder enlazados

Esta plantilla, tomada de la sesión 1, vale para todas las variantes (cambiando
densas por convolucionales, etc.):

```python
INPUT_SHAPE = X_train.shape[1]    # p.ej. 140 para ECG

def build_ae(latent_dim):
    # ===== ENCODER =====
    # Pirámide DECRECIENTE en potencias de 2, ReLU salvo en el espacio latente
    # (que suele ser linear para no perder rango).
    inp = keras.layers.Input(shape=(INPUT_SHAPE,))
    x   = keras.layers.Dense(64, activation="relu")(inp)
    x   = keras.layers.Dense(32, activation="relu")(x)
    z   = keras.layers.Dense(latent_dim, activation="linear")(x)   # espacio latente
    encoder = keras.Model(inp, z, name="encoder")

    # ===== DECODER =====
    # Misma pirámide pero CRECIENTE. La salida no lleva activación si reconstruyes
    # señales (ECG); usa "sigmoid" si el target está normalizado en [0,1] (imagen).
    dec_in = keras.layers.Input(shape=(latent_dim,))
    x = keras.layers.Dense(32, activation="relu")(dec_in)
    x = keras.layers.Dense(64, activation="relu")(x)
    out = keras.layers.Dense(INPUT_SHAPE, activation="linear")(x)
    decoder = keras.Model(dec_in, out, name="decoder")

    # ===== AUTOENCODER (enlaza encoder + decoder) =====
    ae_in  = keras.layers.Input(shape=(INPUT_SHAPE,))
    ae_out = decoder(encoder(ae_in))
    ae = keras.Model(ae_in, ae_out, name="autoencoder")
    ae.compile(optimizer="adam", loss="mae")     # MAE para señales / MSE para imágenes
    return ae, encoder, decoder
```

> **Tres modelos, no uno.** Mantener `encoder` y `decoder` separados es lo que
> te permite luego (a) extraer códigos latentes con `encoder.predict(X)` y (b)
> generar nuevas muestras con `decoder.predict(z)`.

## 2.4 Métricas y diagnósticos comunes (sesión 1)

```python
from sklearn.metrics import r2_score

# --- Calidad de reconstrucción: R^2 medio sobre el conjunto ---
decoded = ae.predict(x_test)
r2 = np.array([r2_score(x_test[i].flatten(), decoded[i].flatten())
               for i in range(len(x_test))]).mean()
print(f"R2 medio: {r2*100:.2f} %")

# --- Compresión efectiva (cociente de dimensionalidades) ---
print(f"Compresión: {LATENT_DIM / np.prod(INPUT_SHAPE) * 100:.2f} %")

# --- Sparsity en el espacio latente ---
encoded = encoder.predict(x_test)
print(f"No nulos: {np.count_nonzero(np.sum(encoded, axis=0))}/{LATENT_DIM}")
```

## 2.5 Caso 1 — Detección de anomalías por umbral (sesión 1, E1–E5)

**Idea esencial:** entrenas solo con normales → el AE NO aprende a reconstruir
anomalías → MAE de las anomalías será mayor → umbralizas.

```python
# === Carga + reetiquetado + split SOLO normales en train ===
# En el CSV original "1" = normal, "0" = anómalo. Reetiquetamos para que
# 0 = normal (clase conocida) y 1 = anómalo (clase desconocida).
df = pd.read_csv("http://storage.googleapis.com/download.tensorflow.org/data/ecg.csv",
                 header=None)
data = df.values
X_orig, y_orig = data[:, :-1], data[:, -1]
y = np.where(y_orig == 1, 0, 1)

X_normal    = X_orig[y == 0]
X_anomalous = X_orig[y == 1]

# 70% normales -> train; 30% normales + TODAS las anomalías -> test.
X_train_normal, X_test_normal = train_test_split(X_normal, test_size=0.3,
                                                 random_state=42)
X_train = X_train_normal
X_test  = np.vstack((X_test_normal, X_anomalous))
y_test  = np.concatenate((np.zeros(len(X_test_normal)),
                          np.ones (len(X_anomalous))))

# === Entrenamiento con EarlyStopping (imprescindible para no sobreajustar) ===
from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor="val_loss", patience=15, restore_best_weights=True)
ae.fit(X_train, X_train,           # mismo X de entrada y salida (autoencoder)
       epochs=150, batch_size=128,
       validation_split=0.2, callbacks=[es], verbose=0)

# === MAE por muestra ===
recon_train = ae.predict(X_train)
recon_test  = ae.predict(X_test)
train_losses = np.mean(np.abs(recon_train - X_train), axis=1)
test_losses  = np.mean(np.abs(recon_test  - X_test ), axis=1)

# === Umbral por percentil de los errores DE TRAINING ===
# El percentil 95 deja como "normal" al 95% de muestras de entrenamiento.
umbral = np.percentile(train_losses, 95)
y_pred = (test_losses > umbral).astype(int)

from sklearn.metrics import classification_report, confusion_matrix
print(classification_report(y_test, y_pred,
                            target_names=["Normales", "Anómalos"]))
```

### Especificidad a sensibilidad fija (E5)

```python
from tensorflow.keras.metrics import SpecificityAtSensitivity

# "¿Qué especificidad consigo si exijo recall (sensibilidad) >= 99%?"
metric = SpecificityAtSensitivity(0.99)
metric.update_state(y_test, test_losses)   # test_losses actúa como score
print(f"Especificidad @ sens=99%: {metric.result().numpy()*100:.2f} %")
```

> **Truco de mejora:** si los resultados son flojos, prueba a **estandarizar**
> primero con `StandardScaler` (fit en train, transform en test). Esto suele
> desbloquear mejoras importantes en señales con escalas distintas.

## 2.6 Caso 2 — Sparse Autoencoder (sesión 2, E2)

Cambia **una sola línea** respecto al AE denso: añade
`activity_regularizer=l1(...)` en la capa latente.

```python
from tensorflow.keras import regularizers

latent = layers.Dense(
    latent_dim,
    activation="relu",                                   # OJO: relu permite ceros
    activity_regularizer=regularizers.l1(10e-5),         # penaliza activaciones
)(x)
```

**Qué observar:** después del entrenamiento, muchos coeficientes de
`encoder.predict(X)` deberían ser exactamente 0. Ese es el efecto buscado: una
codificación dispersa más interpretable, normalmente con algo de pérdida de
calidad de reconstrucción.

## 2.7 Caso 3 — Convolutional Autoencoder (CAE) (sesión 2, E3–E4)

**Cuándo usarlo:** datos con estructura espacial 2D (imágenes). Sustituye
`Dense` por `Conv2D` / `Conv2DTranspose`.

### Receta de bloque por nivel

```python
# --- Nivel del codificador ---
# strides=2 reduce a la mitad cada dimensión espacial (downsampling).
# BatchNorm + LeakyReLU es la combinación estándar (más estable que Conv+ReLU sólo).
x = layers.Conv2D(filters, kernel_size=3, strides=2, padding="same")(x)
x = layers.BatchNormalization()(x)
x = layers.LeakyReLU()(x)

# --- Nivel del decodificador ---
# Conv2DTranspose con strides=2 hace upsampling (recupera la dimensión).
x = layers.Conv2DTranspose(filters, kernel_size=3, strides=2, padding="same")(x)
x = layers.BatchNormalization()(x)
x = layers.LeakyReLU()(x)
```

### CAE completo (3 niveles, espacio latente convolucional)

```python
# --- ENCODER ---
encoder_input = layers.Input(shape=(64, 64, 1))      # 1 canal = gris
x = layers.Conv2D(16, 3, strides=2, padding="same")(encoder_input)  # 32x32x16
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)
x = layers.Conv2D(32, 3, strides=2, padding="same")(x)              # 16x16x32
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)
x = layers.Conv2D(64, 3, strides=2, padding="same")(x)              # 8x8x64
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)

# Espacio latente "espacial" 8x8x16 = 1024 valores
# (sin BatchNorm en la salida del espacio latente, recomendación de la práctica)
x = layers.Conv2D(16, 3, strides=1, padding="same")(x)
latent = layers.LeakyReLU()(x)

# --- DECODER (simétrico) ---
x = layers.Conv2DTranspose(64, 3, strides=1, padding="same")(latent)
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)
x = layers.Conv2DTranspose(32, 3, strides=2, padding="same")(x)     # 16x16x32
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)
x = layers.Conv2DTranspose(16, 3, strides=2, padding="same")(x)     # 32x32x16
x = layers.BatchNormalization()(x); x = layers.LeakyReLU()(x)

# Salida: 1 canal (gris) o 3 canales (RGB). Sigmoid porque las imágenes están en [0,1].
output = layers.Conv2DTranspose(1, 3, strides=2, padding="same",
                                activation="sigmoid")(x)            # 64x64x1

ae = keras.Model(encoder_input, output, name="CAE")
ae.compile(optimizer="adam", loss="mse")
ae.fit(images_gray, images_gray, epochs=50, batch_size=32,
       validation_split=0.2)
```

### Variante: coloreado gris→RGB (E5)

```python
# Misma arquitectura, pero:
#   - input  -> 64x64x1 (gris)
#   - output -> 64x64x3 (RGB)
#   - target durante .fit() -> images (RGB), no images_gray
ae.fit(images_gray, images, epochs=50, batch_size=32, validation_split=0.2)
```

## 2.8 Caso 4 — Variational Autoencoder (sesión 3)

El VAE introduce dos cosas nuevas que es muy habitual confundir:

1. **Reparametrization trick:** en vez de muestrear `z ~ N(μ, σ)` (no
   diferenciable), muestreas `ε ~ N(0,1)` y calculas
   `z = μ + exp(0.5·log σ²)·ε`.
2. **Pérdida combinada:** `loss = reconstruction_loss + kl_weight * kl_loss`.

### Capa de muestreo (reparametrización)

```python
class Sampling(layers.Layer):
    """Toma (z_mean, z_log_var) y devuelve z = mu + sigma * eps."""
    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim   = tf.shape(z_mean)[1]
        epsilon = tf.keras.backend.random_normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon
```

### Encoder y decoder del VAE

```python
latent_dim = 64

# --- ENCODER convolucional. Salida: (z_mean, z_log_var, z) ---
encoder_inputs = keras.Input(shape=(64, 64, 3))
x = layers.Conv2D(16, 3, activation="relu", strides=2, padding="same")(encoder_inputs)
x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Flatten()(x)
x = layers.Dense(128, activation="relu")(x)
z_mean    = layers.Dense(latent_dim, name="z_mean")(x)
z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)
z         = Sampling()([z_mean, z_log_var])
encoder   = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")

# --- DECODER. Recupera 64x64x3 con Conv2DTranspose ---
latent_inputs = keras.Input(shape=(latent_dim,))
x = layers.Dense(8 * 8 * 64, activation="relu")(latent_inputs)
x = layers.Reshape((8, 8, 64))(x)
x = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(x)
x = layers.Conv2DTranspose(16, 3, activation="relu", strides=2, padding="same")(x)
decoder_outputs = layers.Conv2DTranspose(3, 3, activation="sigmoid", padding="same")(x)
decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")
```

### Modelo VAE con `train_step` personalizado

```python
class VAE(keras.Model):
    def __init__(self, encoder, decoder, kl_weight=1.0, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.kl_weight = kl_weight    # peso del término KL en la pérdida
        # Trackers para imprimir métricas medias por época.
        self.total_loss_tracker          = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(name="reconstruction_loss")
        self.kl_loss_tracker             = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [self.total_loss_tracker,
                self.reconstruction_loss_tracker,
                self.kl_loss_tracker]

    def train_step(self, data):
        with tf.GradientTape() as tape:
            z_mean, z_log_var, z = self.encoder(data)
            reconstruction = self.decoder(z)

            # 1) Pérdida de RECONSTRUCCIÓN: BCE píxel a píxel, sumada por imagen.
            reconstruction_loss = tf.reduce_mean(
                tf.reduce_sum(
                    keras.losses.binary_crossentropy(data, reconstruction),
                    axis=(1, 2),
                )
            )
            # 2) Pérdida KL: fuerza a que (z_mean, z_log_var) ~ N(0, I).
            kl_loss = -0.5 * (1 + z_log_var - tf.square(z_mean) - tf.exp(z_log_var))
            kl_loss = tf.reduce_mean(tf.reduce_sum(kl_loss, axis=1))

            total_loss = reconstruction_loss + self.kl_weight * kl_loss

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))

        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss":                self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss":             self.kl_loss_tracker.result(),
        }

vae = VAE(encoder, decoder, kl_weight=1.0)
vae.compile(optimizer=keras.optimizers.Adam(learning_rate=1e-3))
vae.fit(images, epochs=30, batch_size=128)
```

### Generación de muestras nuevas (E2)

```python
def generar_imagenes(decoder, latent_dim, n=10):
    """Muestra n imágenes nuevas tomando z ~ N(0, I) y decodificando."""
    z_sample = np.random.normal(size=(n, latent_dim))
    imgs = decoder.predict(z_sample, verbose=0)
    fig, axes = plt.subplots(1, n, figsize=(15, 3))
    for i, ax in enumerate(axes):
        ax.imshow(imgs[i]); ax.axis("off")
    plt.show()

generar_imagenes(vae.decoder, latent_dim, n=10)
```

### Estudio de hiperparámetros del VAE (E3)

Cuando el enunciado pide "evaluar la influencia" de varios hiperparámetros
(típicamente `latent_dim` y `kl_weight`), **no los muevas a la vez**: se solapan
los efectos y no puedes atribuir la diferencia a ninguno. Patrón correcto:

- Experimento A: solo `latent_dim` (p.ej. 64 → 1024), dejando `kl_weight=1.0`.
- Experimento B: solo `kl_weight` (p.ej. 1 → 10), dejando `latent_dim=64`.

```python
def construir_vae(latent_dim_, kl_weight_):
    """Encoder + Decoder + VAE con hiperparámetros configurables."""
    enc_in = keras.Input(shape=(64, 64, 3))
    x = layers.Conv2D(16, 3, activation="relu", strides=2, padding="same")(enc_in)
    x = layers.Conv2D(32, 3, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2D(64, 3, activation="relu", strides=2, padding="same")(x)
    x = layers.Flatten()(x)
    # OJO: la Dense intermedia se ESCALA con latent_dim. Si la dejas fija en 128
    # y subes el latente a 1024, creas un cuello de botella que limita la
    # información que llega a (z_mean, z_log_var) y "rompe" el experimento.
    x = layers.Dense(max(128, latent_dim_ * 2), activation="relu")(x)
    zm  = layers.Dense(latent_dim_, name="z_mean")(x)
    zlv = layers.Dense(latent_dim_, name="z_log_var")(x)
    zz  = Sampling()([zm, zlv])
    enc = keras.Model(enc_in, [zm, zlv, zz])

    dec_in = keras.Input(shape=(latent_dim_,))
    y = layers.Dense(8 * 8 * 64, activation="relu")(dec_in)
    y = layers.Reshape((8, 8, 64))(y)
    y = layers.Conv2DTranspose(64, 3, activation="relu", strides=2, padding="same")(y)
    y = layers.Conv2DTranspose(32, 3, activation="relu", strides=2, padding="same")(y)
    y = layers.Conv2DTranspose(16, 3, activation="relu", strides=2, padding="same")(y)
    out = layers.Conv2DTranspose(3, 3, activation="sigmoid", padding="same")(y)
    dec = keras.Model(dec_in, out)

    m = VAE(enc, dec, kl_weight=kl_weight_)
    m.compile(optimizer=keras.optimizers.Adam())
    return m
```

> **Lectura del trade-off:** subir `latent_dim` sin tocar nada más mejora la
> reconstrucción del _training_ pero diluye la regularización KL por dimensión
> (a menudo aparece _posterior collapse_ parcial: dimensiones inactivas y
> muestras ruidosas). Subir `kl_weight` empuja el latente a N(0, I) y mejora la
> coherencia de las muestras generadas, pero borra detalles (imágenes más
> "promediadas").

### Visualización del espacio latente con PCA + comprobación de gaussianidad (E4)

El scatter PCA por sí solo no demuestra que la estadística del latente se ajuste
a la predeterminada (N(0, I)); conviene añadir histogramas con la normal
ajustada y, opcionalmente, un test de normalidad.

```python
from sklearn.decomposition import PCA
from scipy import stats

# 1) Tomamos las MEDIAS (no muestras) -> latente determinista por imagen.
z_mean, _, _ = vae.encoder.predict(images, verbose=0)

# 2) Reducción a 2D con PCA para inspección visual.
pca = PCA(n_components=2)
z_pca = pca.fit_transform(z_mean)

plt.figure(figsize=(8, 6))
plt.scatter(z_pca[:, 0], z_pca[:, 1], alpha=0.3, s=2)
plt.title("Proyección PCA del espacio latente"); plt.grid(True); plt.show()

# 3) Histogramas de PC1/PC2 con la PDF normal ajustada superpuesta.
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for i, ax in enumerate(axes):
    datos = z_pca[:, i]
    ax.hist(datos, bins=50, density=True, alpha=0.6, label=f"PC{i+1}")
    xs = np.linspace(datos.min(), datos.max(), 200)
    ax.plot(xs, stats.norm.pdf(xs, datos.mean(), datos.std()),
            "r-", lw=2, label="N(μ, σ) ajustada")
    ax.set_title(f"PC{i+1} — μ={datos.mean():.3f}, σ={datos.std():.3f}")
    ax.legend()
plt.tight_layout(); plt.show()

# 4) Sanity check sobre el latente original: media≈0, desviación≈1 por dimensión.
print(f"μ global de z_mean: {z_mean.mean():.4f}  (esperado ≈ 0)")
print(f"σ global de z_mean: {z_mean.std():.4f}  (esperado ≈ 1)")

# 5) Test cuantitativo (D'Agostino-Pearson) sobre cada componente principal.
for i in range(2):
    stat, p = stats.normaltest(z_pca[:, i])
    print(f"PC{i+1}: estadístico={stat:.2f}, p-valor={p:.4g}")
```

> **Interpretación:** si la KL ha hecho su trabajo, el scatter forma una nube
> aproximadamente circular sin huecos, los histogramas casan con la normal
> ajustada y `μ ≈ 0`, `σ ≈ 1`. El p-valor del test casi siempre será pequeño
> (con miles de muestras, hasta desviaciones diminutas se vuelven
> significativas); es más útil mirar la **forma** que el p-valor estricto.
>
> **Trade-off VAE:** `kl_weight` bajo → la nube se sale de N(0, I) (mejor
> reconstrucción, peor generación). `kl_weight` alto → se ajusta a una gaussiana
> esférica (mejor generación, reconstrucción borrosa).

### Data augmentation por espejado (E5)

```python
# Espejo horizontal: axis=2 corresponde al eje de columnas en (N, H, W, C).
# Las caras son aproximadamente simétricas, así que duplicar el set por flip
# horizontal es coherente con la distribución de datos (no introduce sesgos).
X_flipped   = np.flip(images, axis=2)
X_augmented = np.concatenate((images, X_flipped), axis=0).astype(np.float32)

# Pipeline tf.data: shuffle + batch + prefetch.
# - shuffle es importante: si no se baraja, los lotes contendrán primero todas
#   las imágenes originales y luego todas las espejadas (sesgo de orden).
# - prefetch(AUTOTUNE) solapa carga y entrenamiento.
train_ds = (
    tf.data.Dataset.from_tensor_slices(X_augmented)
    .shuffle(buffer_size=2048)
    .batch(128)
    .prefetch(tf.data.AUTOTUNE)
)

# Para que la comparación con E2 sea JUSTA (mismas épocas, distinto dataset),
# se reentrena un VAE LIMPIO en lugar de seguir entrenando el de E2.
vae_aug = construir_vae(latent_dim_=64, kl_weight_=1.0)
es = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)
vae_aug.fit(train_ds, epochs=30, callbacks=[es])

# Generamos imágenes nuevas para comparar visualmente con las de E2.
generar_imagenes(vae_aug.decoder, latent_dim=64, n=10)
```

> **Por qué un VAE limpio en E5.** Si haces `vae.fit(train_ds, ...)`
> reutilizando el modelo de E2, mezclas dos efectos: épocas adicionales y nuevo
> dataset. Reinstanciar permite atribuir la mejora exclusivamente al aumento de
> datos.

---

# PARTE 3 — Recetas transversales

## 3.1 Cómo decidir la codificación de entrada (P3)

| Pregunta                                                | Respuesta                                                  |
| ------------------------------------------------------- | ---------------------------------------------------------- |
| ¿Importa el orden?                                      | **No** → multi-hot / TF-IDF. **Sí** → integer + embedding. |
| ¿El vocabulario es enorme (>10⁴)?                       | Evita one-hot. Usa embedding aprendido.                    |
| ¿Hay tokens muy frecuentes y poco discriminativos?      | TF-IDF mejor que multi-hot.                                |
| ¿Quieres capturar patrones locales sin RNN/Transformer? | TF-IDF + `ngrams=(2,2)` o `(1,2)`.                         |
| ¿Quieres una representación reutilizable y compacta?    | Embedding aprendido, después PCA para visualizar.          |

## 3.2 Cómo decidir el tipo de autoencoder (P4)

| Objetivo                                              | Arquitectura                                              |
| ----------------------------------------------------- | --------------------------------------------------------- |
| Detectar fuera-de-distribución                        | AE denso entrenado solo con clase normal + umbral en MAE. |
| Comprimir representaciones interpretables             | Sparse AE (regularizador L1 en latente).                  |
| Trabajar con imágenes manteniendo estructura espacial | CAE (`Conv2D` + `Conv2DTranspose`).                       |
| Generar datos nuevos / explorar latente continuo      | VAE (Sampling + KL).                                      |
| Traducir dominio A → dominio B (gris → color)         | CAE asimétrico (cambia el target).                        |

## 3.3 Errores frecuentes y cómo evitarlos

- **`adapt()` con todo el dataset.** Adapta SOLO con train
  (`vec.adapt(X_train_text)`); si no, contaminas el experimento con información
  de test.
- **Olvidar `mask_zero=True`.** Sin máscara, las RNNs y Transformers aprenden
  ruido sobre el padding. Activa siempre que uses `Embedding` después de un
  `TextVectorization` con `output_sequence_length`.
- **`embed_dim` no divisible entre `num_heads`.** El constructor de
  `MultiHeadAttention` exige `embed_dim % num_heads == 0`. Si quieres 6 cabezas,
  usa `embed_dim ∈ {6, 12, 18, 24, 30, 36, 60, 96, ...}`.
- **No reseteo de Keras entre runs.** Antes de cada repetición de un grid
  search: `keras.backend.clear_session()` + reseed. Si no, los pesos previos
  contaminan la nueva configuración.
- **Comparar configuraciones con UN solo entrenamiento.** Por ruido de
  inicialización, la diferencia que ves puede ser puro azar. Mínimo `repeats=2`,
  mejor 3–5, y reporta media ± std.
- **Pasar tensores RGB enormes a GPU.** En P4 sesión 3 con data augmentation,
  usa `tf.data.Dataset` con `batch().prefetch(AUTOTUNE)` en lugar de un único
  array NumPy.
- **Olvidar `get_config` en capas custom.** Si no lo defines, no podrás
  guardar/cargar el modelo y `keras.utils.register_keras_serializable` no
  salvará el día.
- **VAE con `kl_weight` mal calibrado.** Demasiado bajo: las muestras nuevas
  serán incoherentes. Demasiado alto ("posterior collapse"): el decoder ignora a
  `z` y todas las generaciones se parecen. Empieza por 1.0 y mueve en factores
  de 2–10.
- **Subir `latent_dim` sin escalar la Dense intermedia.** Si el encoder termina
  en `Dense(128) → Dense(latent_dim=1024)`, la información que llega al espacio
  latente está limitada por el cuello de 128. Escala la capa intermedia (p.ej.
  `max(128, latent_dim*2)`) cuando varíes la dimensión latente.
- **Mover dos hiperparámetros del VAE a la vez.** En E3 (sesión 3 de P4), si
  cambias `latent_dim` y `kl_weight` simultáneamente no puedes atribuir la
  mejora/empeoramiento a ninguno. Hay que aislar uno por experimento.
- **Reutilizar el modelo entrenado al añadir data augmentation.** En E5, llamar
  a `vae.fit(...)` sobre el VAE ya entrenado mezcla "más épocas" con "más
  datos". Reinstancia el VAE para que la comparación con E2 sea justa.
- **No barajar el dataset al concatenar augmentations.** `tf.data` lee en orden;
  si no haces `.shuffle(...)`, los primeros lotes son originales y los últimos
  espejados, sesgando el entrenamiento.

## 3.4 Mini-cheatsheet para recordar

```text
PROBLEMA                       ENCODING         MODELO          ARCHIVO
-----------------------------  ---------------  --------------  -------------------------
Clasificar péptido (presencia) multi-hot/tfidf  MLP             p3_sesion1.ipynb
Clasificar péptido (orden)     integer+emb      BiLSTM          p3_sesion2.ipynb
Clasificar péptido (contexto)  integer+posemb   Transformer     p3_sesion3.ipynb
Anomalía en ECG                señal cruda      AE denso        DL_p4_AE_sesion1.ipynb
Codificación dispersa          imagen plana     Sparse AE       DL_p4_AE_sesion2.ipynb (E2)
Comprimir/reconstr. imágenes   imagen 2D        CAE             DL_p4_AE_sesion2.ipynb (E3-4)
Coloreado gris->color          gris (in)/RGB    CAE asimétrico  DL_p4_AE_sesion2.ipynb (E5)
Generar caras nuevas           imagen RGB       VAE             DL_p4_AE_sesion3.ipynb
```

---

## Apéndice — Snippet "todo en uno" de plotting de entrenamiento

```python
def plot_history(history, metrics=("loss",), title=""):
    """
    Pinta train vs val para cada métrica indicada en una sola figura.
    Sirve igual para AEs (loss/val_loss), clasificadores
    (accuracy/val_accuracy) y VAEs (reconstruction_loss/kl_loss).
    """
    n = len(metrics)
    fig, axes = plt.subplots(1, n, figsize=(6*n, 4))
    if n == 1:
        axes = [axes]
    for ax, m in zip(axes, metrics):
        ax.plot(history.history[m], label=f"train {m}")
        if f"val_{m}" in history.history:
            ax.plot(history.history[f"val_{m}"], label=f"val {m}")
        ax.set_xlabel("Época"); ax.set_title(f"{title} — {m}")
        ax.legend(); ax.grid(True)
    plt.tight_layout(); plt.show()
```

---

_Última revisión: mayo 2026. Si encuentras un bloque que se repite en varios
apartados, probablemente esté implementado tal cual en el archivo
correspondiente — usa la tabla del apartado 0 para localizarlo._
