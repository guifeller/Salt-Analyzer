import json
from nltk.tokenize import word_tokenize

class Parser:
    def __init__(self, sent, jdata):
        self.jdata = jdata               # The json file listing all the command words
        self.toParse = sent.lower()      # The original sentence. Because the speech to text device doesn't necessarily know what to capitalize, everything is turned to lowercase
        self.fileName = ""               # The name of the file
        self.word_tokens = []            # The tokenized sentence
        self.sentence = []               # The sentence during and after parsing
        self.active = False              # Whether hey Salt has been uttered or not
        self.found = False               # Whether a command word has been found or not        

    def tokenize(self):
        try:
            self.word_tokens = word_tokenize(self.toParse)
            return self.word_tokens
        except:
            print(self.toParse)
            print("Unable to parse the sentence")
            return False

    def checkSalt(self):
        # We need to go through the word_tokens list through a for loop because it is not a given that "Hey Salt" will be the first two words of the received string.
        # For example, 'Please, Hey Salt ...' is a possibility.
        for index, w in enumerate(self.word_tokens):
            if(self.active):
                #Creates a sentence containing all the words appearing after "Hey Salt"
                self.sentence.append(w)
            if (w.lower() == "salt" and self.word_tokens[index - 1].lower() == "hey"):
                self.active = True
        return self.active

    def findCom(self):
        # We look for the first command word appearing in the sentence
        for index, word in enumerate(self.sentence):
            word = word.lower()
            if(self.found): # We only need one command word so no need to keep looping through the list
                break
            for key in self.jdata["Entry"]:
                if(self.found):
                    break
                if (word == key['commandWord']):
                    self.fileName = key['fileName']
                    self.sentence = self.sentence[index+1:] # We remove the command word and everything that comes before it from the sentence
                    self.found = True # We announce that the command word has been isolated
                    break
        return self.sentence

    def genRequest(self):
        # The request that will be sent to the server
        req = []
        req.append(self.fileName + ' ')
        req.append(" ".join(self.sentence))
        s = ""
        return s.join(req)

    def treat(self):
        # A general method that fully parses the sentence without requiring to use each method individually
        if(self.jdata == ""):
            return False
        self.tokenize()
        self.checkSalt()
        if(self.active == False):
            return self.active
        self.findCom()
        if(self.found == False):
            return -1
        return self.genRequest()