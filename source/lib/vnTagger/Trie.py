
import operator

class Node:
    def __init__(self):
        self.info = {}
        self.child = {}

class Trie:
    def __init__(self):
        self.root = Node()
    def insertWord(self, word, tag):
        p = self.root
        for c in word:
            if c not in p.child:
                p.child[c] = Node()
            p = p.child[c]
        if tag not in p.info.keys():
            p.info[tag] = 1
        else:
            p.info[tag] += 1
    def searchWord(self, word):
        p = self.root
        for c in word:
            if c not in p.child:
                return {}
            else:
                p = p.child[c]
        return p.info
    def exist(self, word):
        p = self.root
        for c in word:
            if c not in p.child:
                return False
            else:
                p = p.child[c]
        return len(p.info) > 0
    def getTag(self, word):
        default_tag = 'Np'
        p = self.root
        for c in word:
            if c not in p.child:
                return default_tag
            else:
                p = p.child[c]
        if len(p.info) == 0:
            return default_tag
        stats = p.info
        return max(stats.items(), key=operator.itemgetter(1))[0]
