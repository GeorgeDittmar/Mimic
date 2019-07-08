from pyspark.sql import SparkSession
from pyspark.sql.functions import size, trim
from pyspark.ml.feature import Tokenizer

from MarkovModelSpark import MarkovModelSpark
import PreProcess

''' Spark runner for markov chain generator code. WIP '''

spark = SparkSession.builder.master('local').appName("MarkovChain").getOrCreate()


text_df = PreProcess.bulk_text_distributed_load(spark, '../data_repo/*.txt')
text_df = text_df.withColumn('text', trim(text_df.text))
json_df = PreProcess.bulk_json_distributed_load(spark, '../data_repo/*.json').select('text')
total_df = text_df.union(json_df)
# tokenize the data and get a new dataframe
tokenizer = Tokenizer(inputCol='text', outputCol='tokenized_text')

# use sparks built in tokenizer for simplicity and filter out empty new lines from dataset
tokenized_df = tokenizer.transform(total_df).drop('text')
tokenized_df = tokenized_df.filter(size('tokenized_text') > 1)
mms = MarkovModelSpark(spark, n=2)
mms.learn(tokenized_df)
result = mms.generate(end_token_stop=False)

mms.save_model("../test_pickle")
mms.load_model("../text_pickle")
print(result)
