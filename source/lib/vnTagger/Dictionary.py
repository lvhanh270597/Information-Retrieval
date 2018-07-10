
import pickle, time
from lib.vnTagger.Trie import Trie
from lib.environment.env import ENV

class Dictionary:
    def __init__(self):
        self.generateTree()
    def split(self, word):
        for i in range(len(word) - 1, 0, -1):
            if word[i] == '/':
                return (word[:i], word[i+1:])
    def buildTree(self):
        start = time.time()
        self.tree = Trie()
        self.tags = []
        print("Building the tree in %s" %(ENV["TAG_DATA_PATH_POS"]))
        for line in open(ENV["TAG_DATA_PATH_POS"]):
            for word_tag in line.split():
                word, tag = self.split(word_tag)
                word = word.lower()
                if tag == "Np": continue
                self.tree.insertWord(word, tag)
                if tag not in self.tags: self.tags.append(tag)
        print("Time for building the tree is %f" %(time.time() - start))
    def saveTree(self):
        with open(ENV['TAG_TREE_PATH'], 'wb') as f:
            pickle.dump(self.tree, f)
        ENV['SAVED_TAG_TREE'] = True

        f = open(ENV["POSTAG_PATH"], "w")
        for tag in self.tags:
            f.write(tag + "\n")
        f.close()
        ENV["SAVED_POSTAG"] = True
    def loadTree(self):
        with open(ENV['TAG_TREE_PATH'], 'rb') as f:
            self.tree = pickle.load(f)

        f = open(ENV["POSTAG_PATH"])
        self.tags = [w for w in f.read().split('\n') if len(w) > 1]

    def generateTree(self):
        if not ENV['SAVED_TAG_TREE']:
            self.buildTree()
            self.saveTree()
        else:
            start = time.time()
            self.loadTree()
            print("Load successfully! Time for loading tree %f" %(time.time() - start))
    def searchWord(self, word):
        return self.tree.searchWord(word.lower())
    def exist(self, word):
        _list = self.tree.searchWord(word)
        return len(_list) > 0
    def getTag(self, word):
        return self.tree.getTag(word.lower())
