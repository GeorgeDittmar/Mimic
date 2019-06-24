from pyspark.sql import SparkSession
from pyspark.sql.functions import size, trim
from pyspark.ml.feature import Tokenizer, NGram

import PreProcess

''' Spark runner for markov chain generator code. WIP '''

spark = SparkSession.builder.master('local').appName("MarkovChain").getOrCreate()


text_df = spark.read.text("../data_repo/*.txt", wholetext=True).withColumnRenamed('value', 'text')
text_df = text_df.withColumn('text', trim(text_df.text))
# tokenize the data and get a new dataframe
tokenizer = Tokenizer(inputCol='text', outputCol='tokenized_text')

# use sparks built in tokenizer for simplicity and filter out empty new lines from dataset
tokenized_df = tokenizer.transform(text_df).drop('text')
tokenized_df = tokenized_df.filter(size('tokenized_text') > 1)

#tokens_rdd = tokenized_df.rdd.flatMap(lambda x: [elm[0] for elm in x])

ngram = NGram(n=2, inputCol='tokenized_text', outputCol='ngram')

ngram_df = ngram.transform(tokenized_df)

# create the ngram to adjacent term mappings
ngram_adjacent_text = ngram_df.rdd \
    .map(lambda x: PreProcess.generate_adjacent_terms(x.asDict()['ngram']))\
    .flatMap(lambda xs: [x for x in xs]) \
    .map(lambda y: (y[0], [y[1]])) \
    .reduceByKey(lambda a, b: a + b)

print(ngram_adjacent_text.lookup("the first")[0])

