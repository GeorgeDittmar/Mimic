from pyspark.sql import SparkSession

''' Spark runner for markov chain generator code. WIP '''

spark = SparkSession.builder.master('local').appName("MarkovChain").getOrCreate()

text_df = spark.read.text("../data_repo/*.txt")

print(text_df.count())