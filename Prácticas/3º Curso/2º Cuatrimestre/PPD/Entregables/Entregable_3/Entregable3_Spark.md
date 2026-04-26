---
title: "Procesamiento Paralelo de Datos"
subtitle: "Tarea 3: Apache Spark"
author: "Francisco Javier Mercader Martínez"
lang: es
format:
  pdf:
    documentclass: article
    listings: true
    toc: true
    toc-title: "Índice"
    number-sections: true
    colorlinks: true
    include-in-header:
      text: |
        \usepackage[table]{xcolor}
        \usepackage{listings}
        \usepackage{enumitem}
        \usepackage{multicol}
        \usepackage{graphicx}
        \usepackage{float}
        \usepackage{tikz} 
        \lstset{
          language=Python,
          basicstyle=\ttfamily\small,
          numberstyle=\tiny,
          keywordstyle=\color{blue},
          commentstyle=\color{olive},
          stringstyle=\color{red},
          breakatwhitespace=false, 
          breaklines=true,
          showspaces=false,
          showstringspaces=false,
          showtabs=false, 
          tabsize=2,
          literate={á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1{ñ}{{\~n}}1 {Á}{{\'A}}1 {Í}{{\'I}}1 {Ú}{{\'U}}1 {¿}{{\textexclamdown}}1,
          mathescape=false,
          backgroundcolor=\color{lightgray!10}
        }
        \usepackage{fancyhdr}
        \pagestyle{fancy}
        \fancyhf{}
        \fancyhead[R]{\textit{Procesamiento Paralelo de Datos}}
        \fancyfoot[C]{\thepage}
linestrectch: 1.5
papersize: a4
geometry: margin=1.5cm
---

\newpage

# Spark

**En este apartado se nos pide desarollar una solución a los ejercicios planteados**

Para poder ejecutar los códigos sobre el archivo de 10K lineas utilizaremos el siguiente comando:

```bash
spark-submit <script_python>
```

## Ejercicio 1

Filtra y extrae información del archivo `2019-Oct_10k.txt`, crea 2 dataframes y los guarda en formato _parquet_.

En el primer DataFrame se agrupa por la columna `product_id` y cuenta el número de elementos de cada grupo para conseguir el número de interacciones que ha tenido cada producto.

En el segundo DataFrame se seleccionan las columnas `product_id`, `brand` y `price`, y se renombran a `ID_Producto`, `Marca` y `Precio` respectivamente.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col


def load_data(spark: SparkSession, path_file: str) -> DataFrame:
    df: DataFrame = (
        spark.read.option("inferSchema", "true").option("header", "true").csv(path_file)
    )

    print(
        "Se han cargado "
        + str(df.count())
        + " entradas del fichero "
        + str(path_file)
        + "."
    )
    return df


def main():

    spark: SparkSession = SparkSession.builder.appName(
        "Ejercicio 1 - Ecommerce"
    ).getOrCreate()

    spark.sparkContext.setLogLevel("FATAL")

    df_ecommerce = load_data(spark, "2019-Oct_10k.txt")

    # a) Contador de interacciones por producto
    # Agrupamos por product_id, contamos y renombramos la columna resultante "count"
    # Mostrar número de particiones del DataFrame resultante
    df_interacciones = (
        df_ecommerce.groupBy("product_id")
        .count()
        .withColumnRenamed("count", "num_interacciones")
    )

    print(
        f"Número de particiones de df_interacciones: {df_interacciones.rdd.getNumPartitions()}"
    )

    # Guardamos en formato Parquet
    (df_interacciones.write.mode("overwrite").parquet("dfInteracciones.parquet"))
    df_interacciones.show()

    #  b) Información normalizada de los productos
    # Seleccionamos columnas, eliminamos duplicados por product_id y renombramos
    df_info_productos = df_ecommerce.select(
        col("product_id").alias("ID_Producto"),
        col("brand").alias("Marca"),
        col("price").alias("Precio"),
    ).drop_duplicates(["ID_Producto"])

    # Guardamos en formato Parquet
    (df_info_productos.write.mode("overwrite").parquet("dfInfoProductos.parquet"))
    df_info_productos.show()


if __name__ == "__main__":
    main()
```

:::: {layout-ncol=2}
::: {#first-layout}

```
+----------+-----------------+
|product_id|num_interacciones|
+----------+-----------------+
|   2900536|                6|
|   1004739|               42|
|  23800009|                3|
|   1005158|                6|
|  12300850|                1|
|   4600498|                2|
|   1003938|                3|
|   1305803|                2|
|  13400542|                2|
|  49300028|                2|
|  38900025|                1|
|  13200834|                6|
|  12701963|                1|
|  13300013|                2|
|   1480506|                2|
|  17200066|                1|
|   7600414|                1|
|  43700023|                1|
|   2900626|                1|
|  17302315|                1|
+----------+-----------------+
only showing top 20 rows
```

:::

::: {#second-column}

```
+-----------+-------+-------+
|ID_Producto|  Marca| Precio|
+-----------+-------+-------+
|    1002099|samsung| 370.41|
|    1002524|  apple| 515.67|
|    1002527|  apple| 771.96|
|    1002528|  apple| 643.23|
|    1002532|  apple| 642.69|
|    1002535|  apple| 864.63|
|    1002536|  apple| 581.48|
|    1002540|  apple| 511.78|
|    1002542|  apple| 475.95|
|    1002544|  apple| 464.13|
|    1002547|  apple|  470.8|
|    1002548|  apple| 580.13|
|    1002628|  apple| 397.95|
|    1002629|  apple| 377.29|
|    1002633|  apple| 360.08|
|    1002634|  apple| 377.03|
|    1002995|  apple| 456.79|
|    1003039|samsung|1154.86|
|    1003050|samsung| 617.52|
|    1003074|  meizu| 134.96|
+-----------+-------+-------+
only showing top 20 rows
```

:::
::::

## Ejercicio 2

Debemos juntar los 2 DataFrames creados anteriormente en la columna `id_producto`, agrupar por `marca` y agregar los resultados en una `cuenta`, una `suma`, una `media` y un `máximo` de las interacciones. Después se ordenará por maxímo de interacciones de manera descendente y marca de manera ascendente si hay un empate en las interacciones.

```python
import sys

from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import avg, col, count, max, sum


def main():
    spark: SparkSession = SparkSession.builder.appName(
        "Ejercicio 2 - Join Simple"
    ).getOrCreate()

    # Reducimos la verbosidad
    spark.sparkContext.setLogLevel("FATAL")

    # Leo los ficheros Parquet del ejercicio 1
    dfInteracciones: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInteracciones.parquet")
    )

    dfProductos: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInfoProductos.parquet")
    )

    # --- CÓDIGO DEL PROGRAMA A RELLENAR ---

    # 1. Join de ambos DataFrames
    dfJoin = dfInteracciones.alias("i").join(
        dfProductos.alias("p"), col("i.product_id") == col("p.ID_Producto"), "inner"
    )

    # 2. Agrupaciones y cálculos por Marca
    dfResultado = dfJoin.groupBy("Marca").agg(
        count("ID_Producto").alias("NumProductos"),
        sum("num_interacciones").alias("TotalInteracciones"),
        avg("num_interacciones").alias("MediaInteracciones"),
        max("num_interacciones").alias("MaxInteracciones"),
    )

    # 3. Ordenación
    dfResultado = dfResultado.orderBy(
        col("MaxInteracciones").desc(), col("Marca").asc()
    )

    # Mostramos 10 filas de ejemplo
    dfResultado.show(10, truncate=False)

    # Lo guardamos como un único fichero CSV
    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej2_csv")
    )

    spark.stop()


if __name__ == "__main__":
    main()
```

```
+--------+------------+------------------+------------------+----------------+
|Marca   |NumProductos|TotalInteracciones|MediaInteracciones|MaxInteracciones|
+--------+------------+------------------+------------------+----------------+
|samsung |180         |1231              |6.838888888888889 |128             |
|apple   |131         |1039              |7.931297709923665 |112             |
|xiaomi  |142         |698               |4.915492957746479 |63              |
|huawei  |50          |306               |6.12              |33              |
|cordiant|22          |89                |4.045454545454546 |31              |
|elari   |5           |29                |5.8               |18              |
|force   |9           |42                |4.666666666666667 |18              |
|acer    |38          |95                |2.5               |17              |
|elenberg|34          |102               |3.0               |17              |
|luminarc|13          |48                |3.6923076923076925|17              |
+--------+------------+------------------+------------------+----------------+
```

## Ejercicio 3

Utilizamos funciones de ventana para conseguir el ranking de productos con más interacciones por marca.

Se deben juntar los 2 DataFrames, creados anteriormente en la columna `id_producto`, se escogen solo las marcas `[apple, samsung, xiaomi]`, después se crea la ventana particionando por marca y ordenando por número de interacciones, con la función `dense_rank` en la ventana, seleccionando `marca`, `ID_Producto`, `num_interacciones`, `Rango` ordenando por `Rango` de manera ascendente y por `num_interacciones` de manera descendente.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, dense_rank
from pyspark.sql.window import Window
import sys


def main():
    spark: SparkSession = SparkSession.builder.appName(
        "Ejercicio 3 - Window Functions"
    ).getOrCreate()

    # Reducimos la verbosidad
    spark.sparkContext.setLogLevel("FATAL")

    # 1. Leo los ficheros Parquet del ejercicio 1
    dfInteracciones: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInteracciones.parquet")
    )

    dfProductos: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInfoProductos.parquet")
    )

    # --- CÓDIGO DEL PROGRAMA A RELLENAR ---

    # 2. Join de ambos DataFrames
    dfJoin = dfInteracciones.alias("i").join(
        dfProductos.alias("p"), col("i.product_id") == col("p.ID_Producto"), "inner"
    )

    # 3. Filtrar por las marcas especificadas ('apple', 'samsung', 'xiaomi')
    dfFiltrado = dfJoin.filter(col("Marca").isin("apple", "samsung", "xiaomi"))

    # 4. Especificar la Ventana (WindowSpec) particionando por marca y ordenando por interacciones
    wMarca = Window.partitionBy("Marca").orderBy(col("num_interacciones").desc())

    # 5. Añadir la columna Rango y ordenar el DataFrame final
    dfConRango = dfFiltrado.withColumn("Rango", dense_rank().over(wMarca))

    # Seleccionamos las columnas pedidas y aplicamos la ordenación global por marca ascendente y número de interacciones descendente
    dfResultado = (
        dfConRango
        .select("Marca", "ID_Producto", "num_interacciones", "Rango")
        .orderBy(col("Marca").asc(), col("num_interacciones").desc())
    )

    # ----------------------------------------------------
    # Mostramos los primeros 20 resultados por consola para validar
    dfResultado.show(20, truncate=False)

    # 6. Lo guardamos como un único fichero CSV

    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej3_csv")
    )

    spark.stop()


if __name__ == "__main__":
    main()
```

```
+-----+-----------+-----------------+-----+
|Marca|ID_Producto|num_interacciones|Rango|
+-----+-----------+-----------------+-----+
|apple|1005115    |112              |1    |
|apple|1005105    |68               |2    |
|apple|1002544    |61               |3    |
|apple|1004249    |53               |4    |
|apple|1004246    |38               |5    |
|apple|1005135    |38               |5    |
|apple|1002524    |36               |6    |
|apple|4804056    |35               |7    |
|apple|1005104    |27               |8    |
|apple|4804055    |26               |9    |
|apple|1003317    |25               |10   |
|apple|1004258    |25               |10   |
|apple|1002633    |24               |11   |
|apple|1003306    |24               |11   |
|apple|1004237    |20               |12   |
|apple|1003316    |18               |13   |
|apple|1003304    |16               |14   |
|apple|1004238    |15               |15   |
|apple|4802036    |13               |16   |
|apple|1005112    |12               |17   |
+-----+-----------+-----------------+-----+
```

## Ejercicio 4

Debemos obtener el numero de interacciones por horas de las marcas más populares `(apple, samsung, xiaomi)`

Se carga el fichero de 600k lineas y se filtran las marcas necesarias `(apple, samsung, xiaomi)`. Después, extraemos la hora de la columna `event_time` mediante la función `hour` y llamamos a la columna `hora`. Luego, se agrupa por `marca` y hora y se agregan los elementos en una cuenta para conseguir `num_interacciones`. Finalmente se seleccionan las columnas `Brand`, `hora` y `num_interacciones` y se guardan.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, hour, count, to_timestamp
import sys


def main():
    spark: SparkSession = SparkSession.builder.appName(
        "Ejercicio 4 - Top marcas por hora"
    ).getOrCreate()

    spark.sparkContext.setLogLevel("FATAL")

    # Cargamos el fichero original
    df_ecommerce: DataFrame = (
        spark.read.option("inferSchema", "true")
        .option("header", "true")
        .csv("2019-Oct_600k.txt")
    )

    # --- CÓDIGO DEL PROGRAMA A RELLENAR ---

    # 1. Definir la lista de marcas objetivo y filtrar el DataFrame
    marcas_objetivo = ["apple", "samsung", "xiaomi"]
    dfMarcas = df_ecommerce.filter(col("brand").isin(marcas_objetivo))

    # 2. Extraer la Hora de la columna event_time
    # Usamos la función hour() nativa de PySpark sobre el df ya filtrado
    dfConHora = dfMarcas.withColumn(
        "event_ts", to_timestamp(col("event_time"), "yyyy-MM-dd HH:mm:ss 'UTC'")
    ).withColumn("Hora", hour(col("event_ts")))

    # 3. Agrupar por Marca y Hora, y contar las interacciones
    dfAgrupado = dfConHora.groupBy("brand", "Hora").agg(
        count("*").alias("NInteracciones")
    )

    # 4. Seleccionar columnas finales, renombrar y ordenar
    # Ordenamos primero por Marca (ascendente) y luego por la Hora (ascendente)
    dfResultado = dfAgrupado.select(
        col("brand").alias("Marca"), col("Hora"), col("NInteracciones")
    ).orderBy(col("Marca").asc(), col("Hora").asc())

    # Mostramos los primeros resultados por pantalla para verificar
    dfResultado.show(20)
    # ----------------------------------------------------
    # Lo guardamos como un único fichero CSV
    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej4_csv")
    )
    spark.stop()


if __name__ == "__main__":
    main()
```

```
+-------+----+--------------+
|  Marca|Hora|NInteracciones|
+-------+----+--------------+
|  apple|   2|           106|
|  apple|   3|            10|
|  apple|   4|          2210|
|  apple|   5|          4531|
|  apple|   6|          5592|
|  apple|   7|          6681|
|  apple|   8|          6903|
|  apple|   9|          7814|
|  apple|  10|          7873|
|  apple|  11|          7702|
|  apple|  12|          7412|
|  apple|  13|          6206|
|samsung|   2|           146|
|samsung|   3|            21|
|samsung|   4|          2685|
|samsung|   5|          5884|
|samsung|   6|          6492|
|samsung|   7|          7687|
|samsung|   8|          7962|
|samsung|   9|          9050|
+-------+----+--------------+
```

# Ejercicios opcionales

**En este apartado se resolverán los ejercicios opcionales presentados en la práctica.**

## Spark en Hadoop

Para ejecutar los códigos anteriores en Hadoop se deben introducir los códigos y el dataset de 600K lineas al entorno mediante. Además, en el ejercicio 1 se debe cambiar la dirección en `load_dataset()` del archivo de 10K al de 600K.

```bash
docker cp <ruta_script> workbench:/home/luser
```

Después ejecutamos desde el usuario `luser`:

```bash
docker compose exec workbench bash
su - luser
hdfs dfs -put 2019-Oct_600k.txt /user/luser
spark-submit --master yarn <ruta_script>
```

### Ejercicio 1

:::: {layout-ncol=2}
::: {#first-layout}

```
+----------+-----------------+
|product_id|num_interacciones|
+----------+-----------------+
|   2900536|              275|
|   1004739|             2617|
|  23800009|               48|
|   1005158|              434|
|  12300850|               49|
|   4600498|               18|
|   1003938|               54|
|   1305803|               27|
|  13400542|                4|
|  49300028|                4|
|  38900025|               22|
|  13200834|               76|
|  12701963|                5|
|  13300013|                3|
|   1480506|               21|
|  17200066|               20|
|   7600414|               18|
|  43700023|                6|
|   2900626|               24|
|  17302315|                2|
+----------+-----------------+
```

:::

::: {#second-column}

```
+-----------+-------+------+
|ID_Producto|  Marca|Precio|
+-----------+-------+------+
|    1002100|samsung|409.02|
|    1002101|samsung|409.02|
|    1002442|   sony|128.68|
|    1002527|  apple|771.96|
|    1002528|  apple|643.23|
|    1002531|  apple|800.51|
|    1002538|  apple| 603.5|
|    1002628|  apple|397.95|
|    1002678|  meizu|231.27|
|    1002757|samsung|168.69|
|    1002796|   NULL|   0.0|
|    1002995|  apple|456.79|
|    1003023|    htc|126.13|
|    1003112|   sony|141.99|
|    1003159|   sony|123.56|
|    1003176| xiaomi|434.76|
|    1003195| huawei| 124.2|
|    1003203| gionee| 95.21|
|    1003208|   NULL|184.82|
|    1003210|samsung|330.86|
+-----------+-------+------+
```

:::
::::

### Ejercicio 2

```
+--------+------------+------------------+------------------+----------------+
|Marca   |NumProductos|TotalInteracciones|MediaInteracciones|MaxInteracciones|
+--------+------------+------------------+------------------+----------------+
|samsung |725         |72730             |100.31724137931035|7722            |
|apple   |412         |63040             |153.0097087378641 |6522            |
|xiaomi  |509         |41523             |81.57760314341847 |3100            |
|huawei  |103         |16505             |160.24271844660194|1794            |
|oppo    |25          |4997              |199.88            |1543            |
|artel   |157         |5091              |32.42675159235669 |925             |
|cordiant|181         |4119              |22.756906077348066|767             |
|vivo    |10          |2385              |238.5             |630             |
|indesit |87          |3220              |37.01149425287356 |587             |
|stels   |49          |2540              |51.83673469387755 |554             |
+--------+------------+------------------+------------------+----------------+
```

### Ejercicio 3

```
+-----+-----------+-----------------+-----+
|Marca|ID_Producto|num_interacciones|Rango|
+-----+-----------+-----------------+-----+
|apple|1005115    |6522             |1    |
|apple|1005105    |3557             |2    |
|apple|1004249    |3285             |3    |
|apple|1002544    |2898             |4    |
|apple|4804056    |2873             |5    |
|apple|1002524    |2051             |6    |
|apple|1005135    |1827             |7    |
|apple|1002633    |1671             |8    |
|apple|1004258    |1568             |9    |
|apple|1003317    |1561             |10   |
|apple|1003306    |1521             |11   |
|apple|4804055    |1497             |12   |
|apple|1005104    |1168             |13   |
|apple|1004246    |1147             |14   |
|apple|1003316    |987              |15   |
|apple|1004237    |934              |16   |
|apple|1005132    |802              |17   |
|apple|4802036    |726              |18   |
|apple|1005116    |710              |19   |
|apple|1004227    |701              |20   |
+-----+-----------+-----------------+-----+
```

### Ejercicio 4

```
+-------+----+--------------+
|  Marca|Hora|NInteracciones|
+-------+----+--------------+
|  apple|   2|           106|
|  apple|   3|            10|
|  apple|   4|          2210|
|  apple|   5|          4531|
|  apple|   6|          5592|
|  apple|   7|          6681|
|  apple|   8|          6903|
|  apple|   9|          7814|
|  apple|  10|          7873|
|  apple|  11|          7702|
|  apple|  12|          7412|
|  apple|  13|          6206|
|samsung|   2|           146|
|samsung|   3|            21|
|samsung|   4|          2685|
|samsung|   5|          5884|
|samsung|   6|          6492|
|samsung|   7|          7687|
|samsung|   8|          7962|
|samsung|   9|          9050|
+-------+----+--------------+
```

## Map Reduce en un Dataset propio ([eCommerce behavior data from multi category store](https://www.kaggle.com/mkechinov/ecommerce-behavior-data-from-multi-category-store))

Este dataset contiene ~44.5 M de líneas y 9 columnas. Para ejecutar los siguientes ejercicios seguiremos los pasos realizados en el ejercicio anterior.

- `event_time`: Fecha y hora exactas en que se produjo el evento, con format `YYYY-MM-DD HH:MM:SS UCT`. Permite ordenar cronológicamente, agrupar por dia/hora y analizar series temporales (p. ej. picos de tráfico).
- `envet_type`: Tipo de interacción del usuario con un producto. Toma exactamente uno de tres valores: `view` (el usuario abre la ficha del producto), `cart` (lo añade al carrito) y `purchase` (efectúa la compra). Es la columna clave para analizar el embudo de conversión
- `product_id`: Identificador único del producto sobre el que ocurre el evento. Sirve para agregar interacciones por artículo (productos más vistos, más comprados, etc.).
- `category_id`: Identificador numérico interno de la categoría a la que pertenece el producto. Es un código opaco (no legible por humanos), pero sí estable y siempre presente. Útil para joins y agregaciones por categoría.
- `category_code`: Nombre legible de la categoría, expresado como una jerarquía con puntos: `dominio.subdominio.detalle` (p. ej. `electronics.smartphone`, `appliances.environment.water_heater`). Puede estar vacío para muchos productos (no todas las categorías están etiquetadas).
- `brand`: Marca del producto en minúsculas (`samsung`, `apple`, `xiaomi`, `aqua`, `lenovo`...). Puede estar vacío si el producto no tiene marca asociada.
- `price`: Precio unitario del producto en el momento del evento, en la divisa interna del dataset (sin símbolo). Suele tener dos decimales (p. ej. `33.20`, `543.10`).
- `user_id`: Identificador permanente del usuario (anonimizado). Persiste entre sesiones, lo que permite estudiar el comportamiento de un mismo usuario a lo largo del tiempo.
- `user_sesion`: Identificador temporal de la sesión del usuario (formato UUID v4, p. ej. `9333dfbd-b87a-4708-9857-6336556b0fcc`). Cambia cuando el usuario abre una nueva sesión, tras cerrar el navegador, expirar las cookies, o tras un periodo prolongado de inactividad. Sirve para agrupar eventos contiguos de un mismo "viaje" de compra.

### Ejercicio 1

a) Calcula el número total de interacciones por producto y guarda el DataFrame en `dfInteracciones.parquet` con columnas `(product_id, num_interacciones)`.

b) Genera un DataFrame con (ID_Producto, Marca, Precio) eliminando duplicados por ID_Producto y lo guarda en `dfInfoProductos.parquet`.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col
from pyspark.sql.types import (
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
)

INPUT_PATH = "../2019-Oct.csv"

SCHEMA = StructType(
    [
        StructField("event_time", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("product_id", LongType(), True),
        StructField("category_id", LongType(), True),
        StructField("category_code", StringType(), True),
        StructField("brand", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("user_id", LongType(), True),
        StructField("user_session", StringType(), True),
    ]
)


def load_data(spark: SparkSession, path_file: str) -> DataFrame:
    """Carga el CSV con esquema explícito y cabecera."""
    return spark.read.option("header", "true").schema(SCHEMA).csv(path_file)


def main():
    spark: SparkSession = (
        SparkSession.builder.appName("Ejercicio 1 - Ecommerce (2019-Oct.csv)")
        .master("local[*]")
        # Si se ejecuta con `python script.py` (sin spark-submit) estos
        # configs aplican. Con spark-submit usa --driver-memory 24g.
        .config("spark.driver.memory", "24g")
        .config("spark.driver.maxResultSize", "4g")
        .config("spark.sql.shuffle.partitions", "80")
        .config("spark.sql.files.maxPartitionBytes", "256m")
        .config("spark.memory.fraction", "0.8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("FATAL")

    df_ecommerce = load_data(spark, INPUT_PATH)

    # a) Número de interacciones por producto
    df_interacciones = (
        df_ecommerce.groupBy("product_id")
        .count()
        .withColumnRenamed("count", "num_interacciones")
    )
    df_interacciones.write.mode("overwrite").parquet("dfInteracciones.parquet")
    df_interacciones.show()

    # b) Información normalizada de los productos
    df_info_productos = df_ecommerce.select(
        col("product_id").alias("ID_Producto"),
        col("brand").alias("Marca"),
        col("price").alias("Precio"),
    ).drop_duplicates(["ID_Producto"])
    df_info_productos.write.mode("overwrite").parquet("dfInfoProductos.parquet")
    df_info_productos.show()

    spark.stop()


if __name__ == "__main__":
    main()
```

:::: {layout-ncol=2}
::: {#first-layout}

```
+----------+-----------------+
|product_id|num_interacciones|
+----------+-----------------+
|  28714755|             3710|
|  28704388|             2548|
|  28101002|             5725|
|  39600005|             1612|
|   3600231|            11878|
|   3200144|              411|
|   5800792|             6897|
|  12705542|              152|
|  12703209|              176|
|   1004791|             7707|
|   9400014|              306|
|   4802068|             1097|
|  25500885|                1|
|  14701558|              495|
|  13300565|              128|
|   3200344|              524|
|   2600283|             3704|
|   4804137|            10370|
|   5000045|               16|
|   6000120|              492|
+----------+-----------------+
only showing top 20 rows
```

:::

::: {#second-column}

```
+-----------+-------+-------+
|ID_Producto|  Marca| Precio|
+-----------+-------+-------+
|    1002103|   NULL|    0.0|
|    1002549|  apple| 488.79|
|    1003028|  apple| 615.54|
|    1003039|samsung|1154.86|
|    1003738|samsung|  120.7|
|    1003761|   sony| 591.78|
|    1003798|  nokia| 639.53|
|    1003856| xiaomi| 140.91|
|    1003895| xiaomi| 179.93|
|    1004078| xiaomi| 406.45|
|    1004157|samsung| 746.48|
|    1004171|  meizu| 123.53|
|    1004174|tp-link|  97.56|
|    1004243|  apple|  737.6|
|    1004266|   inoi|  61.92|
|    1004324|  honor| 247.11|
|    1004341|  meizu| 200.29|
|    1004372|  honor| 378.39|
|    1004501|   oppo| 308.86|
|    1004503|   oppo| 514.79|
+-----------+-------+-------+
only showing top 20 rows
```

:::
::::

### Ejercicio 2

A partir de los Parquets generados por p1_ecommerce.py (`dfInteracciones.parquet` y `dfInfoProductos.parquet`), agrupa por marca y obtiene:

- NumProductos : nº de productos distintos por marca
- TotalInteracciones : suma de interacciones de todos sus productos
- MediaInteracciones : media de interacciones por producto
- MaxInteracciones : máximo de interacciones de un solo producto

Inner join entre ambos DataFrames. Ordenado por MaxInteracciones desc y, en caso de empate, por Marca asc. Resultado guardado como CSV único en `resultados_ej2_csv/`.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import avg, col, count, max, sum


def main():
    spark: SparkSession = (
        SparkSession.builder.appName("Ejercicio 2 - Join Simple (2019-Oct.csv)")
        .master("local[*]")
        .config("spark.driver.memory", "24g")
        .config("spark.driver.maxResultSize", "4g")
        .config("spark.sql.shuffle.partitions", "80")
        .config("spark.sql.files.maxPartitionBytes", "256m")
        .config("spark.memory.fraction", "0.8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("FATAL")

    # 1. Carga de los Parquets generados en el ejercicio 1
    dfInteracciones: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInteracciones.parquet")
    )
    dfProductos: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInfoProductos.parquet")
    )

    # 2. Inner join por id de producto
    dfJoin = dfInteracciones.alias("i").join(
        dfProductos.alias("p"),
        col("i.product_id") == col("p.ID_Producto"),
        "inner",
    )

    # 3. Agregaciones por marca
    dfResultado = dfJoin.groupBy("Marca").agg(
        count("ID_Producto").alias("NumProductos"),
        sum("num_interacciones").alias("TotalInteracciones"),
        avg("num_interacciones").alias("MediaInteracciones"),
        max("num_interacciones").alias("MaxInteracciones"),
    )

    # 4. Ordenación: MaxInteracciones desc y Marca asc en caso de empate
    dfResultado = dfResultado.orderBy(
        col("MaxInteracciones").desc(), col("Marca").asc()
    )

    dfResultado.show(10, truncate=False)

    # 5. Guardado como CSV único con cabecera
    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej2_csv")
    )

    spark.stop()


if __name__ == "__main__":
    main()
```

```
+--------+------------+------------------+------------------+----------------+
|Marca   |NumProductos|TotalInteracciones|MediaInteracciones|MaxInteracciones|
+--------+------------+------------------+------------------+----------------+
|samsung |1047        |5087713           |4859.324737344795 |500354          |
|apple   |554         |4068462           |7343.794223826715 |355786          |
|xiaomi  |765         |2855610           |3732.823529411765 |189460          |
|huawei  |116         |1098424           |9469.172413793103 |126394          |
|oppo    |32          |395074            |12346.0625        |110648          |
|artel   |210         |333502            |1588.104761904762 |76222           |
|NULL    |51190       |7635545           |149.16087126391872|69028           |
|cordiant|251         |366373            |1459.6533864541832|58330           |
|force   |30          |166301            |5543.366666666667 |50448           |
|stels   |80          |233693            |2921.1625         |49847           |
+--------+------------+------------------+------------------+----------------+
only showing top 10 rows
```

### Ejercicio 3

Window Functions: ranking de productos por marca según el número de interacciones, restringido a apple, samsung y xiaomi.

Pasos:

1. Inner join entre dfInteracciones.parquet y dfInfoProductos.parquet
   generados por p1_ecommerce.py.
2. Filtro por Marca in {apple, samsung, xiaomi}.
3. dense_rank() sobre Window particionada por Marca y ordenada por
   num_interacciones descendente.
4. Selección final (Marca, ID_Producto, num_interacciones, Rango)
   ordenada por Marca asc y num_interacciones desc.
5. Salida en `resultados_ej3_csv/` (CSV único con cabecera).

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, dense_rank
from pyspark.sql.window import Window


def main():
    spark: SparkSession = (
        SparkSession.builder.appName("Ejercicio 3 - Window Functions (2019-Oct.csv)")
        .master("local[*]")
        .config("spark.driver.memory", "24g")
        .config("spark.driver.maxResultSize", "4g")
        .config("spark.sql.shuffle.partitions", "80")
        .config("spark.sql.files.maxPartitionBytes", "256m")
        .config("spark.memory.fraction", "0.8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("FATAL")

    # 1. Lectura de los Parquets del ejercicio 1
    dfInteracciones: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInteracciones.parquet")
    )
    dfProductos: DataFrame = (
        spark.read.format("parquet")
        .option("mode", "FAILFAST")
        .load("dfInfoProductos.parquet")
    )

    # 2. Inner join
    dfJoin = dfInteracciones.alias("i").join(
        dfProductos.alias("p"),
        col("i.product_id") == col("p.ID_Producto"),
        "inner",
    )

    # 3. Filtro por las marcas pedidas
    dfFiltrado = dfJoin.filter(col("Marca").isin("apple", "samsung", "xiaomi"))

    # 4. Window: partición por Marca, orden por num_interacciones desc
    wMarca = Window.partitionBy("Marca").orderBy(col("num_interacciones").desc())
    dfConRango = dfFiltrado.withColumn("Rango", dense_rank().over(wMarca))

    # 5. Proyección y orden global
    dfResultado = (
        dfConRango.select("Marca", "ID_Producto", "num_interacciones", "Rango")
        .orderBy(col("Marca").asc(), col("num_interacciones").desc())
    )

    dfResultado.show(20, truncate=False)

    # 6. CSV único con cabecera
    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej3_csv")
    )

    spark.stop()


if __name__ == "__main__":
    main()
```

```
+-----+-----------+-----------------+-----+
|Marca|ID_Producto|num_interacciones|Rango|
+-----+-----------+-----------------+-----+
|apple|1005115    |355786           |1    |
|apple|1004249    |231070           |2    |
|apple|1005105    |215598           |3    |
|apple|4804056    |214234           |4    |
|apple|1002544    |205597           |5    |
|apple|1002524    |134206           |6    |
|apple|1002633    |123521           |7    |
|apple|1003306    |115633           |8    |
|apple|1005135    |108623           |9    |
|apple|1003317    |105606           |10   |
|apple|1004258    |89422            |11   |
|apple|4804055    |85574            |12   |
|apple|1004246    |61772            |13   |
|apple|1004237    |58195            |14   |
|apple|1003310    |56665            |15   |
|apple|1005104    |53934            |16   |
|apple|1005116    |53560            |17   |
|apple|4802036    |51517            |18   |
|apple|1004250    |50367            |19   |
|apple|1003316    |50163            |20   |
+-----+-----------+-----------------+-----+
only showing top 20 rows
```

### Ejercicio 4

Volumen de tráfico por hora, restringido a las marcas tecnológicas
apple, samsung y xiaomi.

Pasos:

1. Carga directa del CSV completo `2019-Oct.csv` con esquema explícito (evita el escaneo doble de inferSchema).
2. Filtro por brand in `{apple, samsung, xiaomi}` con `.isin()`.
3. Conversión de event_time (formato `'yyyy-MM-dd HH:mm:ss UTC'`) a timestamp y extracción de la hora con `hour()`.
4. Agrupación por (Marca, Hora) y conteo de interacciones.
5. Renombrado, orden por Marca asc y Hora asc, y guardado como CSV único con cabecera en `resultados_ej4_csv/`.

```python
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import col, count, hour, to_timestamp
from pyspark.sql.types import (
    DoubleType,
    LongType,
    StringType,
    StructField,
    StructType,
)

INPUT_PATH = "../2019-Oct.csv"

SCHEMA = StructType(
    [
        StructField("event_time", StringType(), True),
        StructField("event_type", StringType(), True),
        StructField("product_id", LongType(), True),
        StructField("category_id", LongType(), True),
        StructField("category_code", StringType(), True),
        StructField("brand", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("user_id", LongType(), True),
        StructField("user_session", StringType(), True),
    ]
)


def main():
    spark: SparkSession = (
        SparkSession.builder.appName("Ejercicio 4 - Top marcas por hora (2019-Oct.csv)")
        .master("local[*]")
        .config("spark.driver.memory", "24g")
        .config("spark.driver.maxResultSize", "4g")
        .config("spark.sql.shuffle.partitions", "80")
        .config("spark.sql.files.maxPartitionBytes", "256m")
        .config("spark.memory.fraction", "0.8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("FATAL")

    # 1. Carga del CSV completo con esquema explícito
    df_ecommerce: DataFrame = (
        spark.read.option("header", "true").schema(SCHEMA).csv(INPUT_PATH)
    )

    # 2. Filtro por marcas objetivo (se aplica antes que cualquier
    #    transformación cara para reducir el volumen lo antes posible)
    marcas_objetivo = ["apple", "samsung", "xiaomi"]
    dfMarcas = df_ecommerce.filter(col("brand").isin(marcas_objetivo))

    # 3. Extracción de la hora desde event_time (incluye sufijo 'UTC')
    dfConHora = dfMarcas.withColumn(
        "event_ts", to_timestamp(col("event_time"), "yyyy-MM-dd HH:mm:ss 'UTC'")
    ).withColumn("Hora", hour(col("event_ts")))

    # 4. Agrupación por marca y hora
    dfAgrupado = dfConHora.groupBy("brand", "Hora").agg(
        count("*").alias("NInteracciones")
    )

    # 5. Selección, renombrado y ordenación
    dfResultado = dfAgrupado.select(
        col("brand").alias("Marca"), col("Hora"), col("NInteracciones")
    ).orderBy(col("Marca").asc(), col("Hora").asc())

    dfResultado.show(24)

    # 6. Guardado como CSV único con cabecera
    (
        dfResultado.coalesce(1)
        .write.format("csv")
        .mode("overwrite")
        .option("header", True)
        .save("resultados_ej4_csv")
    )

    spark.stop()


if __name__ == "__main__":
    main()
```

```
+-----+----+--------------+
|Marca|Hora|NInteracciones|
+-----+----+--------------+
|apple|   0|         23892|
|apple|   1|         43117|
|apple|   2|         85673|
|apple|   3|        138882|
|apple|   4|        184386|
|apple|   5|        212968|
|apple|   6|        230441|
|apple|   7|        235664|
|apple|   8|        242097|
|apple|   9|        243057|
|apple|  10|        234109|
|apple|  11|        226096|
|apple|  12|        218861|
|apple|  13|        230097|
|apple|  14|        247175|
|apple|  15|        265578|
|apple|  16|        271199|
|apple|  17|        248149|
|apple|  18|        208085|
|apple|  19|        140952|
|apple|  20|         84818|
|apple|  21|         53489|
|apple|  22|         31606|
|apple|  23|         22163|
+-----+----+--------------+
only showing top 24 rows
```
