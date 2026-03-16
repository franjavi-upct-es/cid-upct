from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc

# 1. Creamos la sesión de Spark
spark = SparkSession.builder \
    .appName("Practica_Ecommerce_PySpark") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# 2. Cargamos el fichero CSV infiriendo el esquema y usando la cabecera
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("2019-Oct_10k.txt")

# 3. Agrupamos por la columna event_type y aplicamos la acción count
df_eventos = df.groupBy("event_type").count()
df_eventos.show()

input("Pulsa ENTER para cerrar Spark...")
