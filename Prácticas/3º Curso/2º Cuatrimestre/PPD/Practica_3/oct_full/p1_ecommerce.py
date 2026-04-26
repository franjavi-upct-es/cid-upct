"""
EJERCICIO 1 (PySpark) sobre el dataset completo 2019-Oct.csv.

a) Calcula el número total de interacciones por producto y guarda el
   DataFrame en `dfInteracciones.parquet` con columnas
   (product_id, num_interacciones).

b) Genera un DataFrame con (ID_Producto, Marca, Precio) eliminando
   duplicados por ID_Producto y lo guarda en `dfInfoProductos.parquet`.

Ejecución local (desde esta carpeta `oct_full/`):
    spark-submit --driver-memory 24g p1_ecommerce.py 2>/dev/null
    # o también:
    python p1_ecommerce.py
"""

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
