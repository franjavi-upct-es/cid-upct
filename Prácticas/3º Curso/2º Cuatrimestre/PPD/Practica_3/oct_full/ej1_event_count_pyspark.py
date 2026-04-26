"""
Ejemplo introductorio: Contador de eventos sobre el dataset completo
2019-Oct.csv usando PySpark.

Equivalente al ej1 de la Práctica 2 (MapReduce) pero implementado con
DataFrames de Spark: agrupa por la columna event_type y cuenta.

Ejecución local:
    spark-submit --driver-memory 24g ej1_event_count_pyspark.py 2>/dev/null
    # o también:
    python ej1_event_count_pyspark.py
"""

from pyspark.sql import SparkSession
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
    spark = (
        SparkSession.builder.appName("Ecommerce - Contador de eventos (2019-Oct.csv)")
        .master("local[*]")
        .config("spark.driver.memory", "24g")
        .config("spark.driver.maxResultSize", "4g")
        .config("spark.sql.shuffle.partitions", "80")
        .config("spark.sql.files.maxPartitionBytes", "256m")
        .config("spark.memory.fraction", "0.8")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("ERROR")

    # Esquema explícito: en CSVs grandes evita una pasada extra para
    # inferSchema y reduce drásticamente el tiempo de carga.
    df = (
        spark.read.option("header", "true")
        .schema(SCHEMA)
        .csv(INPUT_PATH)
    )

    df_eventos = df.groupBy("event_type").count()
    df_eventos.show()

    # Descomentar para inspeccionar la UI de Spark en http://localhost:4040
    # input("Pulsa ENTER para cerrar Spark...")
    spark.stop()


if __name__ == "__main__":
    main()
