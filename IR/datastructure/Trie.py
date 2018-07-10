
from datastructure.Node import Node

class Trie:
    def __init__(self):
        self.root = Node()
    def insertWord(self, word, info):
        p = self.root
        for c in word:
            if c not in p.child:
                p.child[c] = Node()
            p = p.child[c]
        p.info.append(info)
    def searchWord(self, word):
        p = self.root
        for c in word:
            if c not in p.child:
                return []
            else:
                p = p.child[c]
        return p.info
    def exist(self, word):
        return len(self.searchWord(word)) > 0
