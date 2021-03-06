#Imports
import nltk
import numpy
import tflearn
import tensorflow
import random
import json
import pickle

#Global 
# Loading Required Files
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("D:/Repositories/White-Panda/chatbot/intents.json") as file:
    intentFile = json.load(file)
with open("D:/Repositories/White-Panda/chatbot/menu.json", "r") as read_file:
    x = json.load(read_file)

#Methods
#   Preprocessor : removes all specific items from question
def pre(userInput):
    userInput = userInput.lower()
    headers = ['stall_name','item_name','price','delivery_service','is_vegetarian','is_cosher','meal_time','is_dessert','is_appetizer','is_hallal','preperation_time','meal_base','calories','allergants']
    searchTerm = 'item_name'
    stripped_list = []

    '''Find if an item from our database is mensioned, 
    if so replace it with general information'''
    for row in range(len(x['criteria'])):
        meal = (x['criteria'][row]['item_name']).lower()

        try:
            userInput.index(meal)
            genericSentence = userInput.replace(meal, "")
            stripped_list.append(genericSentence)
            stripped_list.append(meal)
            stripped_list.append(getAllData(row))
            return(stripped_list)
        except ValueError:
            print("", end = '')
    else:
        stripped_list.append(userInput)
        return(stripped_list)
#   getAllData: Gets all data relating to a meal name
def getAllData(rowNumber):
    wordInfo = ['null','null','null','null','null','null','null','null','null','null','null','null','null','null']
    headers = ['stall_name','item_name','price','delivery_service','is_vegetarian','is_cosher','meal_time','is_dessert','is_appetizer','is_hallal','preperation_time','meal_base','calories','allergants']
    for header in headers:
        value = x['criteria'][rowNumber][header]
        wordInfo[headers.index(header)] = value
    return(wordInfo)
#   printToUser: Write to screen
def printToUser(chatbotOutput):
    print(">>>>>> " + chatbotOutput) #print("\t\t"+chatbotOutput)

#   bag: holds all our numbers
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1     
    return numpy.array(bag)

#Creating Neural Network
#   Create tags for our model
allWords = []
allTags = []
try:
    with open("D:/Repositories/White-Panda/chatbot/intentFile.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []

    for intent in intentFile["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            allWords.append(wrds)
            allTags.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    words = [stemmer.stem(w.lower()) for w in words if w != "?"]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(allWords):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(allTags[x])] = 1
        training.append(bag)
        output.append(output_row)


    training = numpy.array(training)
    output = numpy.array(output)

    with open("D:/Repositories/White-Panda/chatbot/intentFile.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

#   Build neural network
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)
model = tflearn.DNN(net)

#   Load our model (if not there, create and train)
try:
    model.load("D:/Repositories/White-Panda/chatbot/model.learningModel")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=False) #50000
    model.save("D:/Repositories/White-Panda/chatbot/model.learningModel")

def fillInfo(input):
    sentence = ""
    return sentence

#   The chat user-bot loop
def chatuserLoop(inputFromUser):
        #inputFromUser = (input(">\t")).lower()
        itemName = "null"
        itemInformation = "null"
        seperatedResult = pre(inputFromUser);
        genericText = seperatedResult[0]
        if len(seperatedResult)==3:
            itemName = seperatedResult[1]
            itemInformation = seperatedResult[2]

        results = model.predict([bag_of_words(genericText, words)])[0]
        results_index = numpy.argmax(results)
        tag = labels[results_index]
        print("(TAG ", tag, ")")
        if results[results_index] > 0.7: #70% accuracy
            for tg in intentFile["intents"]:
                if tg['tag'] == tag: #tags
                    responses = tg['responses']
                    # Custom responses only in value is found
                    if itemName != "null":
                        # Take values at variables
                        STALLNAME=itemInformation[0] #TODO change to none
                        ITEMNAME=itemInformation[1]
                        PRICE=itemInformation[2]
                        DEVLIVERY_SERVICE=itemInformation[3]
                        IS_VEGETARIAN=itemInformation[4]
                        IS_COSHER=itemInformation[5]
                        MEALTIME=itemInformation[6]
                        ISDESSERT=itemInformation[7]
                        ISAPPATIZER=itemInformation[8]
                        IS_HALLAL=itemInformation[9]
                        PREPERATIONTIME=itemInformation[10]
                        MEALBASE=itemInformation[11]
                        CALORIES=itemInformation[12]
                        ALLERGANTS=itemInformation[13]
                        if tag == "stall_name":
                            listWords = intentFile["intents"][7]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?stall?", STALLNAME)
                            return sentence
                            break;
                        elif tag == "item_price":
                            listWords = intentFile["intents"][8]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?price?", f"RM{PRICE}0")
                            return sentence
                            break;
                        elif tag == "delivery_service":
                            listWords = intentFile["intents"][9]["context_set"]
                            if DEVLIVERY_SERVICE == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                            break;
                        elif tag == "is_vegetarian":
                            listWords = intentFile["intents"][10]["context_set"]
                            if IS_VEGETARIAN == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                        elif tag == "is_cosher":
                            listWords = intentFile["intents"][11]["context_set"]
                            if IS_COSHER == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                        elif tag == "is_dessert":
                            listWords = intentFile["intents"][13]["context_set"]
                            if ISDESSERT == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                        elif tag == "is_appetizer":
                            listWords = intentFile["intents"][14]["context_set"]
                            if ISAPPATIZER == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                        elif tag == "is_hallal":
                            listWords = intentFile["intents"][12]["context_set"]
                            if IS_HALLAL == "yes":
                                conj = "is"
                            else:
                                conj = "is not"
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?conj?", conj)
                            return sentence
                        elif tag == "item_preperation_time":
                            listWords = intentFile["intents"][15]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?item_preperation_time?", f"{PREPERATIONTIME}")
                            return sentence
                        elif tag == "item_meal_base":
                            listWords = intentFile["intents"][16]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?mealbase?", MEALBASE)
                            return sentence
                        elif tag == "calories":
                            listWords = intentFile["intents"][17]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?calories?", f"{CALORIES}")
                            return sentence
                        elif tag == "allergants":
                            listWords = intentFile["intents"][18]["context_set"]
                            sentence = random.choice(listWords)
                            sentence = sentence.replace("?meal?", ITEMNAME)
                            sentence = sentence.replace("?allergants?", ALLERGANTS)
                            return sentence
                        else:
                           return random.choice(responses) # Result does not have input variable. Provide generic response
                    else:
                        return random.choice(responses) # Response does not require input variables. Provide generic response
        else:
            return "I do not understand that. Please ask again"

#    MAIN METHOD #
def main():
    #printToUser("Hello. We here at Notts-Cafeteria would be happy to answer any questions you may have for us")
    chatuserLoop()

# coding below
if __name__ == "__main__":
    for i in range(3):
        print()
    main()