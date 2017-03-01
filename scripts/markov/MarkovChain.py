import random
class MarkovModel():
    def __init__(self):
        self.model = None

    def build_model(self,ngrams,n=2):
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

    def generate(self,seed=None, max_tokens=100):
        if seed == None:
            seed = random.choice(self.model.keys())
        output = list(seed)
        current = seed

        for i in range(0,max_tokens):
            # get next possible set of words from the seed word
            possible_transitions = self.model[current]
            current = random.choice(possible_transitions)
            output.append(current)

        return output
