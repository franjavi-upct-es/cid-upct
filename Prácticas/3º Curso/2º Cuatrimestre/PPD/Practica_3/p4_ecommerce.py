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
