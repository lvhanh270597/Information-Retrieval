

from datastructure.Trie import Trie

class nGramMatching:
    def __init__(self, n_grams=2):
        self.n_grams = n_grams
    def getNGram(self, sentence):
        result = []
        words = sentence.split()
        for i in range(self.n_grams - 1, len(words)):
            result.append(tuple(words[i - (self.n_grams - 1) : i + 1]))
        return result
    def buildTreeFromSentence(self, sentence):
        trie = Trie()
        for words in self.getNGram(sentence):
            trie.insertWord(' '.join(words), True)
        return trie
    def matching(self, sentence1, sentence2):
        trie = self.buildTreeFromSentence(sentence1)
        cnt = 0
        for words in self.getNGram(sentence2):
            words = ' '.join(words)
            if trie.exist(words): cnt += 1
        lenNGram1 = len(sentence1.split()) - self.n_grams + 1
        lenNGram2 = len(sentence2.split()) - self.n_grams + 1
        if cnt == 0: return 0
        return cnt / min(lenNGram1, lenNGram2)

