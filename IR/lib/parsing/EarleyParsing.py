

from lib.environment.env import ENV
from lib.vnTagger.Tagger import Tagger
class State(object):
    def __init__(self, left, right, step, star = 0):
        self.left = left
        self.right = right[:]
        self.id_star = star
        self.step = step[:]
        self.index = 0
        self.trace = []
    def next(self):
        self.id_star += 1
    def isComplete(self):
        return (self.id_star == len(self.right))
    def getKey(self):
        return self.left
    def getVal(self):
        return self.right
    def getStar(self):
        return self.right[self.id_star]
    def getStep(self):
        return self.step[:]
    def getIndex(self):
        return self.index
    def getInstance(self):
        new_state = State(self.left, self.right, self.step, self.id_star)
        new_state.trace = self.trace[:]
        new_state.index = self.index
        return new_state
    def getTrace(self):
        return self.trace[:]
    def setStep(self, L):
        self.step = L[:]
    def setIndex(self, index):
        self.index = index
    def addTrace(self, x):
        self.trace.append(x)
    def __str__(self):
        l = ['']
        if (self.id_star > 0):
            l = self.right[ : self.id_star]
        r = self.right[self.id_star : ]
        return self.left + '-->' + ' '.join(l) + '*' + ' '.join(r) + ' ' + str(self.step)


class EarleyParsing:
    def __init__(self):
        self.tagger = Tagger()
        self.grammar = dict()
        self.words = []
        self.chart = []
        self.POS = {}

        self.isPOS = {"NNP", "NN", "IN", "RB", "VB",
                      "JJ", "JJS", "JJR", "CC", "RBR",
                      "RBS", "UNN", "PRP", "CD", "DT", "MD"}

        self.index = 0
        self.items = {}

        self.readData()

    def readData(self):
        for line in open(ENV["GRAMMAR_PATH"]):
            item = line.replace('\n', '')
            index = item.index('->')
            key, val = item[:index].strip(), item[index + 2 :].split()
            if key not in self.grammar.keys():
                self.grammar[key] = [val]
            else:
                self.grammar[key].append(val)
        '''for line in open(ENV["POS_PATH"]):
            s = line.split()
            self.POS[s[0]] = s[1 : ]'''
    def enqueue(self, s, chart):
        for sta in chart:
            if (str(sta) == str(s)):
                return
        instance = s.getInstance()
        self.index += 1
        instance.setIndex(self.index)
        self.items[instance.getIndex()] = instance
        chart.append(instance)
    def next_cat_is_POS(self, s):
        return (s.getStar() in self.isPOS)

    def scanner(self, s):
        B = s.getStar()
        i, j = s.getStep()
        wordj = self.words[j]
        englishTags = self.tagger.getEnglishTags(wordj)
        #if (B in self.POS[self.words[j]]):
        if B in englishTags:
            self.enqueue(State(B, [wordj], [j, j + 1], 1), self.chart[j + 1])
            return (True, B)
        else:
            return (False, B)

    def predictor(self, s):
        B = s.getStar()
        i, j = s.getStep()
        vals = self.grammar[B]
        for val in vals: self.enqueue(State(B, val, [j, j]), self.chart[j])

    def completer(self, s):
        key = s.getKey()
        j, k = s.getStep()
        for sta in self.chart[j]:
            if (sta.isComplete()): continue
            if (sta.getStar() == key):
                new_state = sta.getInstance()
                new_state.setStep([new_state.getStep()[0], k])
                new_state.next()
                new_state.addTrace(s.getIndex())
                self.enqueue(new_state, self.chart[k])

    def parse(self, sentence):
        self.chart = []
        self.words = sentence.split()
        for i in range(len(self.words) + 1):
            self.chart.append([])
        self.enqueue(State('gamma', ['S'], [0, 0]), self.chart[0])
        for i in range(len(self.words)):
            ok, maybe = False, []
            for s in self.chart[i]:
                if (not s.isComplete()):
                    if self.next_cat_is_POS(s):
                        c = self.scanner(s)
                        if c[0]: ok = True
                        else:
                            if c[1] not in maybe: maybe.append(c[1])
                    else: self.predictor(s)
                else: self.completer(s)
            if not ok:
                word = self.words[i]
                return [word, maybe, self.tagger.getEnglishTags(word)]
        for s in self.chart[len(self.words)]:
            self.completer(s)
    def DFS(self, u, depth):
        s = ''
        if (u.getKey() in self.isPOS):
            s += str(u.getKey()) + '(' + str(u.getVal()[0]) + ')'

        if u.getKey() not in self.isPOS:
            s += str(u.getKey()) + '('
            for v in u.getTrace():
                s += self.DFS(self.items[v], depth + 1)
            s += ')'
        return s
    def chunking(self, u, depth):
        s = ''
        if (u.getKey() in self.isPOS):
            s += str(u.getKey()) + '(' + str(u.getVal()[0]) + ')'

        if u.getKey() not in self.isPOS:
            s += str(u.getKey()) + '('
            for v in u.getTrace():
                s += self.chunking(self.items[v], depth + 1)
            s += ')'
        self.chunks.append(s)
        return s
    def getChunk(self, sentence):
        ok = self.parse(sentence)
        if not ok:
            #print("OKKKK")
            self.chunks = []
            root = self.chart[-1][-1]
            self.chunking(root, 0)
            print(self.chunks)
            return self.chunks
        else:
            #print("Can not parse this sentence")
            return []

    def getTree(self, sentence = "Hoa đã để Huệ"):
        ok = self.parse(sentence)
        if not ok:
            print("OKKKK")
            root = self.chart[-1][-1]
            return self.DFS(root, 0)
        else:
            print("Can not parse this sentence")
            return ''
    @staticmethod
    def getSimilarity(chunk1, chunk2):
        if len(chunk2) == 0 or len(chunk1) == 0: return 0
        set1 = set(chunk1)
        set2 = set(chunk2)
        common = set2.intersection(set1)
        if len(common) == 0: return 0
        min_max = min(max([len(item) for item in set1]),
                      max([len(item) for item in set2]))
        return 0.5 * max([len(item) for item in common]) / min_max + \
               0.5 * len(common) / min(len(set1), len(set2))
