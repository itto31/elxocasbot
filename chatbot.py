from email.mime import message
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from gtts import gTTS
import pygame
from os import remove
from tensorflow.keras.models import load_model


language = 'es'


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('./intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(
        word.lower()) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence, words, show_details=False):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return(np.array(bag))


def predict_class(sentence):
    bow = bag_of_words(sentence, words, show_details=True)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# get response


def get_response(ints, intents_json):
    result = ""
    tags = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag'] == tags):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg)
    intents_json = intents
    tags = ints[0]['intent']
    list_of_intents = intents_json['intents']
    res = get_response(ints, intents)
    for i in list_of_intents:
        if(i['tag'] == tags):
            result = random.choice(i['responses'])
            break
    return result


print("Go! bot is running...")


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = chatbot_response(sentence)
        print(resp)


# while True:
#     message = input("You: ")
#     ints = predict_class(message)
#     res = get_response(ints, intents)
#     print(res)
#     myobj = gTTS(text=res, lang=language, slow=False)
#     myobj.save("welcome.mp3")
#     archivo = "welcome.mp3"
#     pygame.mixer.init()
#     pygame.mixer.music.load(archivo)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     if(pygame.mixer.music.get_busy() == False):
#         pygame.mixer.music.unload()
#         remove(archivo)
