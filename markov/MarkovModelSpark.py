from pyspark.ml.feature import NGram

import PreProcess
import random


class MarkovModelSpark:

    def __init__(self, spark_session, n=2):
        self.spark_session = spark_session
        self.ngram_model = None
        self.model_keys = None
        self.n = n

    def learn(self, text_df):
        """Spark transformation to learn the adjacent terms of a given ngram"""

        ngram = NGram(n=self.n, inputCol='tokenized_text', outputCol='ngram')
        ngram_df = ngram.transform(text_df)
        # create the ngram to adjacent term mappings
        ngram_list = ngram_df.select("ngram").rdd.map(lambda r: r['ngram']).collect()
        self.ngram_model = ngram_df.rdd \
            .map(lambda x: PreProcess.generate_adjacent_terms(x.asDict()['ngram'])) \
            .flatMap(lambda xs: [x for x in xs]) \
            .map(lambda y: (y[0], [y[1]])) \
            .reduceByKey(lambda a, b: a + b).collect()

        # create list of the keys in the model and store them
        self.model_keys = self.ngram_model.map(lambda x: x[0]).collect()

    def retrain(self, text_df):
        """Function to retrain a model given new text input so the model does not have to be fully retrained on all
        the data but only the parts that are new. Assumes the text_df is in the same format as the already trained
        model."""

        raise NotImplementedError("Retrain functionality has not been implemented yet.")

    def generate(self, seed=None, end_token_stop=True, max_tokens=200):
        """Generate text based on the model learned on the corpus"""

        if self.ngram_model is None:
            raise ValueError('Model has not been generated yet. Run the learn function first.')

        if seed is None:
            seed = random.choice(self.model_keys)

        output = seed.split(" ")
        output[0] = output[0].capitalize()
        current = seed

        for i in range(0, max_tokens):
            if current in self.model_keys:
                next_token = self.__get_next_token(current)
                if next_token is None or next_token == '#END#':
                    if end_token_stop:
                        break
                    else:
                        current = random.choice(self.model_keys)
                        next_token = self.__get_next_token(current)
                output.append(next_token)
                current = " ".join(output[-self.n:])

        return " ".join(output)

    def __get_next_token(self, current):
        return random.choice(self.ngram_model.lookup(current)[0])

    def save_model(self, file_path, spark_pickle=True):
        if spark_pickle:
            self.ngram_model.saveAsPickleFile(file_path)
        else:
            raise NotImplementedError("Only support for Spark based pickling currently implemented.")

    def load_model(self, file_path, spark_pickle=True):
        if spark_pickle:
            self.ngram_model = self.spark_session.sparkContext.pickleFile(file_path)
        else:
            raise NotImplementedError("Only support for Spark based pickling currently implemented.")
