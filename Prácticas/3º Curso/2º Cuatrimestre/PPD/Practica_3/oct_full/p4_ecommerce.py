"""
EJERCICIO 4 (PySpark) sobre el dataset completo 2019-Oct.csv.

Volumen de tráfico por hora, restringido a las marcas tecnológicas
apple, samsung y xiaomi.

Pasos:
    1) Carga directa del CSV completo `2019-Oct.csv` con esquema
       explícito (evita el escaneo doble de inferSchema).
    2) Filtro por brand in {apple, samsung, xiaomi} con .isin().
    3) Conversión de event_time (formato 'yyyy-MM-dd HH:mm:ss UTC') a
       timestamp y extracción de la hora con hour().
    4) Agrupación por (Marca, Hora) y conteo de interacciones.
    5) Renombrado, orden por Marca asc y Hora asc, y guardado como CSV
       único con cabecera en `resultados_ej4_csv/`.

Ejecución local (desde esta carpeta):
    spark-submit --driver-memory 24g p4_ecommerce.py 2>/dev/null
    # o también:
    python p4_ecommerce.py
"""

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
