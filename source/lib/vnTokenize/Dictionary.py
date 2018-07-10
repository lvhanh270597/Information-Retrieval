
import pickle, time
from lib.vnTokenize.Trie import Trie
from lib.environment.env import ENV

class Dictionary:
    def __init__(self):
        self.generateTree()
    def generateTree(self):
        if not ENV['SAVED_VOCAB_TREE']:
            self.buildTree()
            self.saveTree()
        else:
            start = time.time()
            self.loadTree()
            print("Load successfully! Time for loading tree %f" %(time.time() - start))
    def buildTree(self):
        start = time.time()
        print("Building the tree with tag at %s" %ENV['DICTIONARY_PATH'])
        vocab = open(ENV['DICTIONARY_PATH'], 'r').read().split('\n')
        self.tree = Trie()
        for i in range(len(vocab)):
            word = vocab[i]
            self.tree.insertWord(word, i + 3)
        print("Build successully! Time for building tree %f " %(time.time() - start))
    def searchWord(self, word):
        index = self.tree.searchWord(word)
        if len(index) > 0: return index
        return [2]
    def exist(self, word):
        _list = self.tree.searchWord(word)
        return len(_list) > 0
    def saveTree(self):
        ENV['SAVED_VOCAB_TREE'] = True
        with open(ENV['VOCAB_TREE_PATH'], 'wb') as f:
            pickle.dump(self.tree, f)
    def loadTree(self):
        with open(ENV['VOCAB_TREE_PATH'], 'rb') as f:
            self.tree = pickle.load(f)
