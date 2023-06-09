from flask import Flask, jsonify
import os
import random
import json
import pickle
import numpy as np
import nltk
import pyttsx3
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

from firebase import firebase
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

from flask import Flask, jsonify, request
firebase = firebase.FirebaseApplication('https://vocals-e4589-default-rtdb.asia-southeast1.firebasedatabase.app/', None)

lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    return sentence_words

def bag_of_words(sentence,words):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence,model,words,classes):
    bow = bag_of_words(sentence,words)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
def firebase_response(entry):
    result = firebase.get('/prash/-NPmLDGT5Mvob4GFXAe_', None)
    res1 = result[entry]
    return res1
    
def chatbot_response(msg,model,intents,words,classes):
    if msg.lower() == "bye" or msg.lower()=="goodbye":
        ints = predict_class(msg, model,words,classes)
        res = "bye"
        return res
    
    else:
        ints = predict_class(msg, model,words,classes)
        res = get_response(ints, intents)
        return res

app = Flask(__name__)


@app.route('/')
def index():
    return 'Book your appointments now'

@app.route('/electrician/<name>') 
def electrician(name):
    
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("electrician.json").read())
    words = pickle.load(open('electrician_words.pkl', 'rb'))
    classes = pickle.load(open('electrician_classes.pkl', 'rb'))
    model = load_model('electrician_chatbotmodel.h5')
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
     
    return response
@app.route('/vehicle/<name>', methods= ['GET']) 
def vehicle(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("vehicle.json").read())
    words = pickle.load(open('vehicle_words.pkl', 'rb'))
    classes = pickle.load(open('vehicle_classes.pkl', 'rb'))
    model = load_model('vehicle_chatbotmodel.h5')
    
 
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response

@app.route('/hospital/<name>', methods= ['GET']) 
def hospital(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("hospital.json").read())
    words = pickle.load(open('hospital_words.pkl', 'rb'))
    classes = pickle.load(open('hospital_classes.pkl', 'rb'))
    model = load_model('hospital_chatbotmodel.h5')
    
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response

@app.route('/restaurant/<name>', methods= ['GET']) 
def restaurant(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("restaurant.json").read())
    words = pickle.load(open('restaurant_words.pkl', 'rb'))
    classes = pickle.load(open('restaurant_classes.pkl', 'rb'))
    model = load_model('restaurant_chatbotmodel.h5')
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response

@app.route('/salon/<name>', methods= ['GET']) 
def salon(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("salon.json").read())
    words = pickle.load(open('salon_words.pkl', 'rb'))
    classes = pickle.load(open('salon_classes.pkl', 'rb'))
    model = load_model('salon_chatbotmodel.h5')
    
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response

@app.route('/dentist/<name>', methods= ['GET']) 
def dentist(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("dentist.json").read())
    words = pickle.load(open('dentist_words.pkl', 'rb'))
    classes = pickle.load(open('dentist_classes.pkl', 'rb'))
    model = load_model('dentist_chatbotmodel.h5')
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response

@app.route('/plumber/<name>', methods= ['GET']) 
def plumber(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("plumber.json").read())
    words = pickle.load(open('plumber_words.pkl', 'rb'))
    classes = pickle.load(open('plumber_classes.pkl', 'rb'))
    model = load_model('plumber_chatbotmodel.h5')
       
    return response

@app.route('/emergency/<name>', methods= ['GET']) 
def emergency(name):
    
    #dec_msg is the real question asked by the user
    dec_msg = name.replace("+", " ")
    
    intents = json.loads(open("emergency.json").read())
    words = pickle.load(open('emergency_words.pkl', 'rb'))
    classes = pickle.load(open('emergency_classes.pkl', 'rb'))
    model = load_model('emergency_chatbotmodel.h5')
    
    #get the response from the ML model & dec_msg as the argument
    response = chatbot_response(dec_msg,model,intents,words,classes)
    
    return response



if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
