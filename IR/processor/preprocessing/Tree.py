
from math import sqrt

class Node:
    def __init__(self):
        self.info = None
        self.child = {}

class Trie:
    def __init__(self):
        self.root = Node()
    def insertWord(self, word, info):
        p = self.root
        for c in word:
            if c not in p.child:
                p.child[c] = Node()
            p = p.child[c]
        p.info = info
    def searchWord(self, word):
        p = self.root
        for c in word:
            if c not in p.child:
                return None
            else:
                p = p.child[c]
        return p.info
    def buildTreeDepend(self, vector):
        size = 0
        for word, val in vector:
            self.insertWord(word, val)
            size += val * val
        self.size = sqrt(size)

    def exist(self, word):
        return self.searchWord(word) != None
    def cosine(self, vector):
        sizeVector = 0
        dot = 0
        for word, val in vector:
            sizeVector += val * val
            valTree = self.searchWord(word)
            if valTree == None: continue
            dot += val * valTree
        sizeVector = sqrt(sizeVector)
        return dot / (sizeVector * self.size + 0.0000001)
