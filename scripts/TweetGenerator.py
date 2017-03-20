import nltk
import json
from pprint import pprint
from collections import Counter
from markov import MarkovChain


def train_model(tweets,n=1):
    pass

def generate_tweet():
    pass

with open("data_repo/data.txt") as json_data:
    trump_data = json.load(json_data)
    json_data.close()

# apparently have to download this data set to build the tokenizer
nltk.download('punkt')

text_extract = [ x['text'] for x in trump_data ]

# join all the tweets together into one long tweet
corpus = ' '.join(text_extract)

tokens = nltk.word_tokenize(corpus)

bigrams = nltk.ngrams(tokens,2)
trigrams = nltk.ngrams(tokens,3)
#
# ngram_list = [ item for item in ngrams]
#
print next(bigrams)
print next(bigrams)
print next(trigrams)

mc = MarkovChain.MarkovModel()

#mc_model = mc.build_model(bigrams)
mc_model2 = mc.learn(tokens,3)

output = mc.generate(3)

print ' '.join(output)