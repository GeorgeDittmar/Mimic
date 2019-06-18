from pyspark.sql import SparkSession
from pyspark.sql.functions import size
from pyspark.ml.feature import Tokenizer
''' Spark runner for markov chain generator code. WIP '''

spark = SparkSession.builder.master('local').appName("MarkovChain").getOrCreate()

text_df = spark.read.text("../data_repo/*.txt").withColumnRenamed('value', 'text')

# tokenize the data and get a new dataframe
tokenizer = Tokenizer(inputCol='text', outputCol='tokenized_text')

# use sparks built in tokenizer for simplicity and filter out empty new lines from dataset
tokenized_df = tokenizer.transform(text_df).drop('text')
tokenized_df = tokenized_df.filter(size('tokenized_text') > 1)

print(tokenized_df.show())