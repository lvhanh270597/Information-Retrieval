
import re
from environment.env import ENV
from lib.vnTokenize.Trie import Trie
from lib.vnTokenize.StringMethod import Split

class Preprocessing:
    def __init__(self, specialChar=False, stopword=False, separateSentence=False):
        self.treeReject = Trie()
        self.specialChar = ['$', '#', '@', '}', "{", "`", '|', '[', ']', '!!', '?!', '??','!?',
                            '^', '&', '*', "'"]

        self.special = specialChar
        if stopword: self.loadStopwords()
        self.stopword = stopword
        self.separate = separateSentence

    def loadStopwords(self):
        for line in open(ENV['STOPWORD_PATH']):
            word = line.replace('\n', '')
            self.treeReject.insertWord(word, True)

    def removeSpecialChar(self):
        if self.special:
            result = []
            for doc in self.docs:
                st = ''
                for ch in doc:
                    if ch not in self.specialChar:
                        st += ch
                result.append(st)
            self.docs = result
    def removeStopword(self):
        if self.stopword:
            result = []
            for doc in self.docs:
                vdoc = Split(doc)
                words = [word for word in vdoc if not self.treeReject.exist(word.lower()) and not self.treeReject.exist(word)]
                result.append(' '.join(words))
            self.docs = result
    def separateParagraph(self):
        if self.separate:
            result = []
            if self.separate:
                for doc in self.docs:
                    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', doc)
                    result.append(sentences)
            self.docs = result

    def processing(self):
        self.removeSpecialChar()
        self.removeStopword()
        self.separateParagraph()
    def fit(self, docs):
        self.docs = docs
        self.processing()
    def getResult(self):
        return self.docs
