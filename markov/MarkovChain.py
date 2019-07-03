import random
import string


class MarkovModel:

    def __init__(self):
        self.model = None

    def build_model(self, ngrams,n=2):
        model = dict()
        for ngram in ngrams:
            key = ngram[0]
            val = ngram[-1]
            if key in model:
                model[key].append(val)
            else:
                model[key] = [val]
        self.model = model
        return model

    def learn(self,tokens,n=2):
        model = {}

        for i in range(0,len(tokens)-n):
            gram = tuple(tokens[i:i+n])
            token = tokens[i+n]

            if gram in model:
                model[gram].append(token)
            else:
                model[gram] = [token]

        final_gram = tuple(tokens[len(tokens) - n:])
        if final_gram in model:
            model[final_gram].append(None)
        else:
            model[final_gram] = [None]
        self.model = model
        return model

    def generate(self,n=2,seed=None, max_tokens=100):
        if seed == None:
            seed = random.choice(self.model.keys())

        output = list(seed)
        output[0] = output[0].capitalize()
        current = seed

        for i in range(n, max_tokens):
            # get next possible set of words from the seed word
            if current in self.model:
                possible_transitions = self.model[current]
                choice = random.choice(possible_transitions)
                if choice is None: break

                # check if choice is period and if so append to previous element
                if choice == '.':
                    output[-1] = output[-1] + choice
                else:
                    output.append(choice)
                current = tuple(output[-n:])
            else:
                # should return ending punctuation of some sort
                if current not in string.punctuation:
                    output.append('.')
        return output
