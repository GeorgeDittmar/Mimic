import nltk
import json
from pprint import pprint
from collections import Counter
from markov import MarkovChain
import PreProcess

def train_model(tweets,n=1):
    pass

def generate_tweet():
    pass

with open("data_repo/data.json") as json_data:
    trump_data = json.load(json_data)
    json_data.close()

# apparently have to download this data set to build the tokenizer
nltk.download('punkt')

speech_text = PreProcess.bulk_txt_load('data_repo/*.txt')
text_extract = [ x['text'] for x in trump_data ]
print(speech_text)
print(text_extract)
text_extract.extend(speech_text)

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
mc_model2 = mc.learn(tokens, 2)
output = mc.generate(2, seed=("Hillary", "Clinton"), max_tokens=125)


print ' '.join(output) + '.'