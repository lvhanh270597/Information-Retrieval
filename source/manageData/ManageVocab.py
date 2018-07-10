
import time
from lib.vnTokenize.Trie import Trie
from lib.environment.env import ENV

class ManageVocab:
    def __init__(self):
        self.vocab = []
        self.exceptTree = Trie()
        self.buildTree()
    def buildTree(self):
        start = time.time()
        print("Building the tree with tag at %s" %ENV['DICTIONARY_PATH'])
        vocab = open(ENV['DICTIONARY_PATH'], 'r').read().split('\n')
        length = len(vocab)
        self.tree = Trie()
        for i in range(len(vocab)):
            word = vocab[i]
            if len(word) == 0: continue
            self.tree.insertWord(word, i)
        print("Build successully! Time for building tree %f " %(time.time() - start))
        self.vocab = vocab[:length - 1]
    def add(self, words):
        length = len(self.vocab)
        for word in words:
            if not self.tree.exist(word):
                self.tree.insertWord(word, length)
                self.vocab.append(word)
                length += 1
                print("Add %s successfully" %word)
    def remove(self, words):
        for word in words:
            self.exceptTree.insertWord(word)
    def saveData(self):
        f = open(ENV["DICTIONARY_PATH"], "w")
        for word in self.vocab:
            if not self.exceptTree.exist(word):
                f.write(word + "\n")
        f.close()
        print("Save parsing successfully")


