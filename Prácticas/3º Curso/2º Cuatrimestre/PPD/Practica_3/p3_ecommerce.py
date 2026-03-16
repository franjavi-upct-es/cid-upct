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
