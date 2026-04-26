"""
EJERCICIO 3 (PySpark) sobre el dataset completo 2019-Oct.csv.

Window Functions: ranking de productos por marca según el número de
interacciones, restringido a apple, samsung y xiaomi.

Pasos:
    1) Inner join entre dfInteracciones.parquet y dfInfoProductos.parquet
       generados por p1_ecommerce.py.
    2) Filtro por Marca in {apple, samsung, xiaomi}.
    3) dense_rank() sobre Window particionada por Marca y ordenada por
       num_interacciones descendente.
    4) Selección final (Marca, ID_Producto, num_interacciones, Rango)
       ordenada por Marca asc y num_interacciones desc.
    5) Salida en `resultados_ej3_csv/` (CSV único con cabecera).

Ejecución local (desde esta carpeta):
    spark-submit --driver-memory 24g p3_ecommerce.py 2>/dev/null
    # o también:
    python p3_ecommerce.py
"""

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
