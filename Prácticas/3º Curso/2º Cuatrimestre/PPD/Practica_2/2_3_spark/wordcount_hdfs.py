import sys
from pyspark.sql import SparkSession

if len(sys.argv) != 3:
    print("Usage: spark-submit wordcount_hdfs.py <input_path> <output_path>")
    sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

spark = SparkSession.builder.appName("WordCountHDFS").getOrCreate()
sc = spark.sparkContext

# WordCount
counts = (
    sc.textFile(input_path)
      .flatMap(lambda line: line.split())
      .map(lambda w: (w, 1))
      .reduceByKey(lambda a, b: a + b)
)

# Save result to HDFS
counts \
    .map(lambda kv: f"{kv[0]}\t{kv[1]}") \
    .saveAsTextFile(output_path)

spark.stop()
