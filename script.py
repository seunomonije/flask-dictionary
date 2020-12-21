import flask
from flask import request, render_template
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


groups = []

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/get-english/<text>/', methods=['GET', 'POST'])
def get_english_request(text):

    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200
    
    else:
        print(text)
        result = convert_english_to_yoruba(text)
        return json.dumps(result)

@app.route('/get-yoruba/<text>/', methods=['GET', 'POST'])
def get_yoruba_request(text):

    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200
    
    else:
        print(text)
        result = convert_yoruba_to_english(text)
        return json.dumps(result)

def convert_yoruba_to_english(englishValue):
    groupsLength = len(groups)
    for i in range(groupsLength):
        if (englishValue in groups[i]):
            return groups[i][1:]

def convert_english_to_yoruba(yorubaValue):
    groupsLength = len(groups)
    for i in range(groupsLength):
        if (yorubaValue in groups[i][1:]):
            return [groups[i][0]] # list to help with iteration

app.run()