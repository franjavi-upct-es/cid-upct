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

    #  b) Información normalizada de los productos
    # Seleccionamos columnas, eliminamos duplicados por product_id y renombramos
    df_info_productos = df_ecommerce.select(
        col("product_id").alias("ID_Producto"),
        col("brand").alias("Marca"),
        col("price").alias("Precio"),
    ).drop_duplicates(["ID_Producto"])

    # Guardamos en formato Parquet
    (df_info_productos.write.mode("overwrite").parquet("dfInfoProductos.parquet"))


if __name__ == "__main__":
    main()
