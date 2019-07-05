import nltk
import json
import MarkovChain
import PreProcess

def train_model(tweets,n=1):
    pass

def train(row):
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
text_extract.extend(speech_text)

# join all the tweets together into one long tweet
corpus = ' '.join(text_extract)

tokens = corpus.split(" ")

# bigrams = nltk.ngrams(tokens,2)
# trigrams = nltk.ngrams(tokens,3)
#
# ngram_list = [ item for item in ngrams]
#

mc = MarkovChain.MarkovModel()

#mc_model = mc.build_model(bigrams)
mc_model2 = mc.learn(tokens, 2)
output = mc.generate(2, max_tokens=50)


print(' '.join(output) + '.')