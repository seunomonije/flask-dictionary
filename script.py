import flask
from flask import request, render_template
import json
import csv

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# groups = [
#     ["omo",  "child", "kid", "baby"],
#     ["baba baba", "grandpa"],
#     ["opo", "widow", "widower"],
#     ["apejuwe", "description"],
#     ['eranko', 'Animal'], 
#     ['tolotolo', 'Turkey'], 
#     ['adie', 'Chicken'], 
#     ['maalu', 'Cow'], 
#     ['elede', 'Pig'], 
#     ['aguntan', 'Sheep'], 
#     ['Aja', 'Dog'], 
#     ['eye', 'Bird'], 
#     ['eja', 'Fish'], 
#     ['Erin', 'Elephant'], 
#     ['Ẹṣin', 'Horse'], 
#     ['Olóńgbò', 'Cat'], 
#     ['Ewúrẹ́', 'Goat'], 
#     ['Àgbò', 'Ram'], 
#     ['Pẹ́pẹ́yẹ', 'Duck'], 
#     ['Ràkúnmí', 'Camel'], 
#     ['Kìnìún', 'Lion'], 
#     ['Ẹkùn', 'Tiger'], 
#     ['Àmọ̀tẹkun', 'Leopard'], 
#     ['Ejò', 'Snake'], 
#     ['Èkúté', 'Mouse'], ['Ìjàpá', 'Turtle'], ['Agbọ́nmiréré', 'Giraffe'], ['Yànmùyánmú', 'Fly'], ['Ẹ̀fọn', 'Mosquito'], ['Oyin', 'Bee'], ['Aáyán', 'Cockroach'], ['Aláǹtaakùn', 'Spider'], ['Apejuwe', 'Description'], ['Se apejuwe', 'To describe'], ['Abuda', 'Characteristics'], ['Irisi', 'Physical appearance'], ['Iwoso', 'Clothing you wear'], ['Iwa adamo/ihuwasi', 'Inherent behavior'], ['Fi (direct object 1) we (direct object 2)', 'To compare (direct object 1) with (direct object 2)'], ['Ifiwera', 'Comparison'], ['Oni-', 'Prefix; means "owner of" (Literally: "He/she/it has..."'], ['Le', 'To be difficult'], ['Ro/Rorun', 'To be easy'], ['Ga', 'To be tall'], ['Giga', 'Tall'], ['Sanra', 'To be fat'], ['Sisanra', 'Fat'], ['Kuru', 'To be short'], ['Kikuru/kukuru', 'Short'], ['Tininrin', 'To be slim/thin'], ['Titininrin', 'Thin/skinny'], ['Tobi', 'To be big'], ['Titobi', 'Big'], ['Kere', 'To be small'], ['Kekere', 'Small'], ['Tooro', 'To be smooth'], ['Olowo', 'A rich person'], ['Kusee', 'To be poor'], ['Akusee', 'A very poor person'], ['Ole', 'A lazy person'], ['Osise', 'A hard working person'], ['Alaaanu', 'A merciful/kind person'], ['Alaiaaanu', 'A merciless person'], ['Ika', 'A wicked person'], ['Logbon', 'To be wise (Literally: "To have wisdom")'], ['Ologbon', 'A wise person'], ['Mowe', 'To be brilliant (Literally: "To know books")'], ['Omugo', 'A foolish person'], ['Go', 'To be foolish'], ['Gigo', 'Foolish'],
# ]

class WordInformation:
    def __init__(self, 
        yoruba_1, yoruba_2, 
        english_1, english_2, 
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
with open('words/holidays.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        # See class definition for row meanings
        word_information = WordInformation(
        row[0], row[1], 
        row[2], row[3], 
        row[4], 
        row[5], row[6])

        groups.append(word_information)

"""
with open('words/animals.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        group_row = fill_group_row(row, 1, 6)
        groups.append(group_row)

groups.pop(0)

with open('words/adjectives.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        group_row = fill_group_row(row, 2, 7)
        groups.append(group_row)
"""
print(groups)
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

app.run()

#for (i in tuples):
#    if (tuples[0] == englishValue)
#if (tuples in myDict):
#    print("English Translation: ")
#    print(myDict.get(englishValue))
#else:
#    print("doesn't exist")

