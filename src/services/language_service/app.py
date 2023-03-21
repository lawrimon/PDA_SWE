"""This application is the stock market service.

The maps service provides an endpoint to get the latest quote of a list of symbols.
It also provides an endpoint to get the latest news of a list of symbols.
The functionality is based on the Alpaca API.
"""

from flask import Flask, jsonify, request
import requests
import os
import datetime
import spacy
import json

# nlp = spacy.load("de_core_news_md")  # Laden des mittelgroßen Modells von spaCy

# # Definieren der zu vergleichenden Sätze
# sentence1 = nlp("Zeig mir was es in der Nähe für Events gibt")
# sentence2 = nlp("Wo gibt es Events")

# # Vergleichen der Ähnlichkeit der beiden Sätze
# similarity = sentence1.similarity(sentence2)

# # Ausgabe des Ergebnisses
# if similarity >= 0.7:
#     print("Die Sätze sind ähnlich genug.")
# else:
#     print("Die Sätze sind nicht ähnlich genug.")
app = Flask(__name__)
with open('prompts.json', 'r') as f:
    prompts = json.load(f)

@app.route("/submit_transcript", methods=['POST'])
def load_prompts():
    """Quotes endpoint.

    This endpoint provides the latest quotes of a list of symbols.

    Args:
        symbols: A list of symbols (e.g. "IBM,MSFT,GOOG").

    Returns:
        A list of the latest quotes of the symbols.
    """
    user_input = request.json['input']

    # Check if user input matches any prompt
    for prompt in prompts['topic1']:
        if user_input == prompt:
            return jsonify({'response': 'User input matches prompt.'})

    check_intent(user_input)
    return jsonify({'response': 'User input does not match any prompt.'})
    print("this is a test")

def load_prompts():

def compare_prompts():

def check_intent():

if __name__ == '__main__':
    app.run(debug=True, port=3000)