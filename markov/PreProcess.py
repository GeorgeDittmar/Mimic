import glob


def tokenize(text):
    return [x for x in text.split()]


def extract_tweets(dataset):
    return [tokenize(x['text']) for x in dataset]


def bulk_txt_load(path):
    """ Feed in directory of text files and tokenize"""
    files = glob.glob(path)
    text = []
    for file in files:
        with open(file) as text_file:
            lines = [x.strip() for x in text_file]
            text.extend(lines)

    return text;


def bulk_json_load(path):
    pass


def bulk_text_distributed_load(spark_session, path):
    ''' Takes a path and sends to Spark for distributed loading and preprocessing'''
    return spark_session.read.text(path, wholetext=True).withColumnRenamed('value', 'text')


def bulk_json_distributed_load(spark_session, path):
    return spark_session.read.json(path)


# little hacky, should make a better one
def generate_adjacent_terms(ngrams):
    # get the current ngram and then extra the first element of the next ngram tuple
    adjacent_list = []
    for i in range(0, len(ngrams)):
        if i == len(ngrams) - 1:
            adjacent_tuple = (ngrams[i], "#END#")
            adjacent_list.append(adjacent_tuple)
        else:
            adjacent_tuple = (ngrams[i], ngrams[i + 1].split(" ")[-1])
            adjacent_list.append(adjacent_tuple)

    return adjacent_list
