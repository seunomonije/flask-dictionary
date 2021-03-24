import flask
from flask import request, render_template
import json
import csv
import os

app = flask.Flask(__name__)
app.config["DEBUG"] = True

class WordInformation:
    def __init__(self, 
        yoruba_1, yoruba_2, yoruba_3, 
        english_1, english_2, english_3,
        part_of_speech, 
        ex_sentence_yoruba, ex_sentence_english):
        self.yoruba_1 = yoruba_1
        self.yoruba_2 = yoruba_2
        self.english_1 = english_1
        self.english_2 = english_2
        self.part_of_speech = part_of_speech
        self.ex_sentence_yoruba = ex_sentence_yoruba
        self.ex_sentence_english = ex_sentence_english
 

def fill_group_row(csv_row, start, finish):
    yoruba_word = csv_row[0]

    group_row = []
    group_row.append(yoruba_word)
    for i in range(start, finish):
        if csv_row[i]:
            group_row.append(csv_row[i])
    return group_row

groups = []

words_path = os.getcwd() + '/words/'
for filename in os.listdir(words_path):
    with open(os.path.join(words_path, filename), newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            # See class definition for row meanings
            word_information = WordInformation(
            row[0], row[1], row[2], 
            row[3], row[4], row[5], 
            row[6], 
            row[7], row[8])

            groups.append(word_information)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/get-english/<text>/', methods=['GET', 'POST'])
def get_english_request(text):

    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200
    
    else:
       # print(text)
        result = convert_english_to_yoruba(text)
        return json.dumps(result)


def convert_english_to_yoruba(englishValue):
    print(englishValue)
    for el in groups:
        if (englishValue in el.english_1) or (englishValue in el.english_2):
            return [el.yoruba_1, el.yoruba_2, el.part_of_speech, el.ex_sentence_yoruba, el.ex_sentence_english]

    """
    groupsLength = len(groups)
    for i in range(groupsLength):
        if (yorubaValue in groups[i][1:]):
            return [groups[i][0]] # list to help with iteration
    """

@app.route('/get-yoruba/<text>/', methods=['GET', 'POST'])
def get_yoruba_request(text):

    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200
    
    else:
        #print(text)
        result = convert_yoruba_to_english(text)
        return json.dumps(result)

def convert_yoruba_to_english(yorubaValue):
    print(yorubaValue)
    for el in groups:
        if (yorubaValue in el.yoruba_1) or (yorubaValue in el.yoruba_2):
            return [el.english_1, el.english_2, el.part_of_speech, el.ex_sentence_yoruba, el.ex_sentence_english]

    """
    groupsLength = len(groups)
    for i in range(groupsLength):
        if (englishValue in groups[i]):
            return groups[i][1:]
    """

@app.route('/get-yoruba-by-letter/<letter>/', methods=['GET', 'POST'])
def get_yoruba_by_letter_request(letter):

    if request.method == 'POST':
        print(request.get_json())
        return 'OK', 200
    else:
        result = get_yoruba_by_letter(letter)
        return json.dumps(result)

def get_yoruba_by_letter(englishLetter):
    # Case issue here
    results = []
    for el in groups:
        if el.english_1:
            first_letter_of_english1 = el.english_1[0]

        if first_letter_of_english1 == englishLetter:
            results.append([el.english_1, el.yoruba_1])

    return sorted(results, key=lambda x: x[0])

app.run()

#for (i in tuples):
#    if (tuples[0] == englishValue)
#if (tuples in myDict):
#    print("English Translation: ")
#    print(myDict.get(englishValue))
#else:
#    print("doesn't exist")

