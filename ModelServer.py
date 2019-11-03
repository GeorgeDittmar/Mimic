from flask import Flask, request, jsonify
from markov import MarkovChain

app = Flask(__name__)
markov_generator = MarkovChain()

@app.route("/")
def root():
    return "Mimic Text Generator"


@app.route('/health')
def health():
    return "UP"


# creating predict url and only allowing post requests.
@app.route('/generate', methods=['POST'])
def predict():

    return ""


if __name__ == '__main__':
    # load model
    markov_generator.load('')
    # start flask app
    app.run(port=3000, debug=True)
