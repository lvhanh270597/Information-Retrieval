
import time, os, pickle
from lib.vnTokenize.Vectorizer import Vectorizer
from lib.vnTokenize.SCRDRTree import SCRDRTree
from lib.vnTokenize.algorithms import MaximumMatching
from lib.environment.env import ENV
from lib.vnTokenize.StringMethod import connectName

class Tokenizer:
    def __init__(self):
        self.generateClassifier()

    def readData(self):
        tokenizer = MaximumMatching()
        start = time.time()
        inp, out = [], []
        for fname in os.listdir(ENV['WS_DATA_INPUT_DIR']):
            for line in open(ENV['WS_DATA_INPUT_DIR'] + "/" + fname):
                if len(line) < 2: continue
                inp.append(tokenizer.tokenize(line))
            for line in open(ENV['WS_DATA_OUTPUT_DIR'] + "/" + fname):
                line = line.replace("\n", "")
                if len(line) < 2: continue
                out.append(line)
        print("Time for reading tag from file %f" %(time.time() - start))
        return (inp, out)

    def buildClassifier(self):
        print("Building classifier tree")
        start = time.time()
        tree, vt = SCRDRTree(), Vectorizer()
        inp, out = self.readData()
        correctLabel, windows = [], []
        for (x, y) in zip(inp[:50], out[:50]):
            windows += vt.getWindowsWord_Tag(x)
            correctLabel += vt.getVectorY(y)
        n_train = int(0.7 * len(windows))
        X_train = windows[: n_train]
        y_train = correctLabel[: n_train]
        X_test = windows[n_train : ]
        y_test = correctLabel[n_train : ]
        # training
        tree.fit(X_train, y_train)
        # testing
        y = tree.predict(X_test)
        cnt, allItems = 0, len(y)
        for (y_real, y_pred) in zip(y_test, y):
            if (y_real == y_pred): cnt += 1
        print("Accuracy = %f" %(cnt / allItems))
        print("Time for training the tree %f" %(time.time() - start))
        self.tree = tree
    def loadClassifier(self):
        start = time.time()
        with open(ENV['WS_MODEL_PATH'], 'rb') as f:
            self.tree = pickle.load(f)
        print("Time for loading the tree %f" %(time.time() - start))
    def saveClassifier(self):
        with open(ENV['WS_MODEL_PATH'], 'wb') as f:
            pickle.dump(self.tree, f)
        ENV['SAVED_MODEL_WS'] = True
    def generateClassifier(self):
        if ENV['SAVED_MODEL_WS']:
            self.loadClassifier()
        else:
            self.buildClassifier()
            self.saveClassifier()
    def tokenize(self, sentence):
        tk, vt = MaximumMatching(), Vectorizer()
        '''windows = vt.getWindowsWord_Tag(tk.tokenize(sentence))
        y = self.tree.predict(windows)

        sentence = vt.getSentenceWithVectorY(sentence, y)
        return self.fixString(sentence)'''
        result = tk.tokenize(sentence)
        return connectName(result)
