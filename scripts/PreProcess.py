import glob
from pyspark.sql import SparkSession
from pyspark import SparkContext

def tokenize(text):
    return [x for x in text.split()]

def extract_tweets(dataset):
    return [tokenize(x['text']) for x in dataset]

def bulk_txt_load(path):
    """ Feed in directory of text files and tokenize"""
    files = glob.glob(path)
    print(files)
    text = []
    for file in files:
        with open(file) as text_file:
            lines = [x.strip().decode("utf-8") for x in text_file]
            text.extend(lines)

    return text;

def bulk_json_load(path):
    pass


def bulk_text_distributed_load(spark, path):
    ''' Takes a path and sends to Spark for distributed loading and preprocessing'''
    pass
