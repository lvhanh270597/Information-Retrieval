
from lib.vnTokenize.StringMethod import Split, Lowers
from lib.environment.env import ENV

class Vectorizer:
    def getVectorY(self, sentence):
        vector = self.getVector(sentence)
        Y, Map = [], {0 : "B", 1 : "I"}
        for i in range(1, len(vector), 2):
            Y.append(Map[vector[i]])
        return Y
    def getVector(self, sentence):
        words = Lowers(Split(sentence))
        v = []
        for word in words:
            _words = word.split('_')
            if len(_words) == 1:
                index = ENV["ws_dict"].searchWord(word)[0]
                v += [index, 0]
            else:
                index = ENV["ws_dict"].searchWord(_words[0])[0]
                v += [index, 0]
                for i in range(1, len(_words)):
                    index = ENV["ws_dict"].searchWord(_words[i])[0]
                    v += [index, 1]
        return v

    def getVectorWindows(self, sentence, window_size):
        vector = self.getVector(sentence)
        haft_window = window_size // 2
        vector = [2, 0] * haft_window + vector + [2, 0] * haft_window
        vector_size = len(vector)
        X = []
        for i in range(haft_window * 2, vector_size - haft_window * 2, 2):
            X.append(vector[i - 2 * haft_window : i + 2 * haft_window + 2])
        return X
    def getSentenceWithVectorY(self, sentence, vectorY):
        words = Split(sentence)
        _words = []
        for word in words:
            _words += word.split('_')

        s = ""
        for (word, _type) in zip(_words, vectorY):
            if _type == "B":
                if len(s) > 0: s += " "
                s += word
            else: s += "_" + word
        return s

    def getVectorWord_Tag(self, sentence):
        words = Lowers(Split(sentence))
        v = []
        for word in words:
            _words = word.split('_')
            if len(_words) == 1:
                v += [word, 0]
            else:
                v += [_words[0], 0]
                for i in range(1, len(_words)):
                    v += [_words[i], 1]
        words, tags = [], []
        for i in range(len(v)):
            if i % 2 == 0: words.append(v[i])
            else:
                if (v[i] == 0): tags.append("B")
                else: tags.append("I")
        return (words, tags)

    def getWindowsWord_Tag(self, sentence, window_size = 5):
        words, tags = self.getVectorWord_Tag(sentence)
        haft_window = window_size // 2
        words = [""] * haft_window + words + [""] * haft_window
        tags = ["B"] * haft_window + tags + ["B"] * haft_window
        vector_size = len(words)
        items = []
        for i in range(haft_window * 1, vector_size - haft_window * 1, 1):
            items.append((words[i - 1 * haft_window : i + 1 * haft_window + 1],
                          tags[i - 1 * haft_window : i + 1 * haft_window + 1]))
        return items
