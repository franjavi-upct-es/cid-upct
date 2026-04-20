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
