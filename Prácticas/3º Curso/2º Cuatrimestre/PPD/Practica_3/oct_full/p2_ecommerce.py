"""
EJERCICIO 2 (PySpark) sobre el dataset completo 2019-Oct.csv.

A partir de los Parquets generados por p1_ecommerce.py
(`dfInteracciones.parquet` y `dfInfoProductos.parquet`), agrupa por
marca y obtiene:
    - NumProductos        : nº de productos distintos por marca
    - TotalInteracciones  : suma de interacciones de todos sus productos
    - MediaInteracciones  : media de interacciones por producto
    - MaxInteracciones    : máximo de interacciones de un solo producto

Inner join entre ambos DataFrames. Ordenado por MaxInteracciones desc
y, en caso de empate, por Marca asc. Resultado guardado como CSV único
en `resultados_ej2_csv/`.

Ejecución local (desde esta carpeta):
    spark-submit --driver-memory 24g p2_ecommerce.py 2>/dev/null
    # o también:
    python p2_ecommerce.py
"""

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
