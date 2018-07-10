
import time, pickle
from lib.vnTagger.Trie import Trie
from lib.environment.env import ENV

class ManagePosTag:
    def __init__(self):
        self.buildTree()
    def split(self, word):
        for i in range(len(word) - 1, 0, -1):
            if word[i] == '/':
                return (word[:i], word[i+1:])
    def buildTree(self):
        start = time.time()
        self.tree = Trie()
        print("Building the tree in %s" %(ENV["TAG_DATA_PATH_POS"]))
        for line in open(ENV["TAG_DATA_PATH_POS"]):
            for word_tag in line.split():
                word, tag = self.split(word_tag)
                word = word.lower()
                self.tree.insertWord(word, tag)
        print("Time for building the tree is %f" %(time.time() - start))
    def add(self, word_tags):
        for word_tag in word_tags:
            word, tag = self.split(word_tag)
            self.tree.insertWord(word, tag)
            print("Add %s successfully" %word_tag)
    def saveData(self):
        ENV['SAVED_TAG_TREE'] = True
        filename = ENV['TAG_TREE_PATH']
        pickle.dump(self.tree, open(filename, 'wb'))

