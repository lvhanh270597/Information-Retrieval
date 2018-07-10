
from lib.vnTokenize.StringMethod import Split, Lowers
from math import log
from lib.environment.env import ENV
class MaximumMatching:
    """
    Input is a sentence
    Return a list of (start, end) which segments
    """
    def tokenize(self, sentence):
        words_init = Split(sentence)
        words = Lowers(words_init)
        maxLength, start, listString = 4, 0, []
        while start < len(words):
            found = False
            for length in range(maxLength, 0, -1):
                end = start + length
                word = ' '.join(words[start : end])
                _word = '_'.join(words_init[start : end])
                if ENV['ws_dict'].exist(word):
                    listString += [_word]
                    start, found = end, True
                    break
            if not found:
                listString += [_word]
                start += 1
        return ' '.join(listString)

class WFST_Dynamic:
    """
    Input is list of words
    Return a list of (start, end) which segments
    """
    def __init__(self, _dict):
        self._dict = _dict
    def tokenize(self, sentence):
        words = Lowers(Split(sentence))
        maxLength, INF, n = 4, 1000000, len(words)
        d, trace = [0] + [INF] * n, [0] * (n + 1)
        for end in range(1, n + 1):
            for length in range(maxLength, 0, -1):
                start = end - length
                if (start >= 0):
                    word = '_'.join(words[start : end])
                    if self._dict.exist(word):
                        # get probalities
                        uv = -log(self._dict.searchString(word)[1], 2)
                        dv = d[start] + uv
                        if (d[end] > dv): trace[end], d[end] = start, dv
        end, listString = n, []
        while (end > 0):
            start = trace[end]
            word = '_'.join(words[start : end])
            listString = [word] + listString
            end = start
        return ' '.join(listString)
