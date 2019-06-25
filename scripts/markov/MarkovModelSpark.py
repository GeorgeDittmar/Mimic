from pyspark.ml.feature import NGram

import PreProcess
import random


class MarkovModelSpark:

    def __init__(self, spark_session, n=2):
        self.spark_session = spark_session
        self.ngram_model = None
        self.model_keys = None
        self.n = n

    def learn(self, text_df, local):
        """Spark transformation to learn the adjacent terms of a given ngram"""

        ngram = NGram(n=self.n, inputCol='tokenized_text', outputCol='ngram')
        ngram_df = ngram.transform(text_df)
        # create the ngram to adjacent term mappings
        self.ngram_model = ngram_df.rdd \
            .map(lambda x: PreProcess.generate_adjacent_terms(x.asDict()['ngram'])) \
            .flatMap(lambda xs: [x for x in xs]) \
            .map(lambda y: (y[0], [y[1]])) \
            .reduceByKey(lambda a, b: a + b)

        # create list of the keys in the model and store them
        self.model_keys = self.ngram_model.map(lambda x: x[0]).collect()

    def generate(self, seed=None, n=2, max_tokens=125):
        """Generate text based on the model learned on the corpus"""

        if self.ngram_model is None:
            raise ValueError('Model cannot be None')

        if seed == None:
            seed = random.choice(self.model_keys)


