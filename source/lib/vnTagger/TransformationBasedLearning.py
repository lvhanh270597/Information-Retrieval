from lib.environment.env import ENV
import pickle

class Word(object):
    def __init__(self, word, tag, correct_tag):
        self.word = word
        self.tag = tag
        self.correct_tag = correct_tag
    def setTag(self, new_tag):
        self.tag = new_tag
    def __str__(self):
        return '(' + self.word + "|" + str(self.tag) + '|' + str(self.correct_tag) + ')'

class Sentence(object):
    def split(self, word):
        for i in range(len(word) - 1, 0, -1):
            if word[i] == '/':
                return (word[:i], word[i+1:])
        return (word, 'No')
    def __init__(self, sourceSentence):
        dictionary = ENV["tag_dict"]
        self.word_tags, sentence = [], []
        for word_tag in sourceSentence.split():
            word, correct_tag = self.split(word_tag)
            tag = dictionary.getTag(word)
            self.word_tags.append(Word(word, tag, correct_tag))
            sentence.append(word + '/' + tag)
        self.sentence = ' '.join(sentence)
    def __str__(self):
        s = ''
        for item in self.word_tags:
            s += str(item) + ' '
        return s

class Transform:
    def __init__(self, prev, fr, to):
        self.prev = prev
        self.fr = fr
        self.to = to
    def apply(self, sentence):
        word_tags = sentence.word_tags
        n, ok = len(word_tags), False
        for i in range(1, n):
            if (word_tags[i - 1].tag == self.prev) and (word_tags[i].tag == self.fr):
                word_tags[i].tag, ok = self.to, True
        if not ok: return False
        sentence.word_tags = word_tags[:]
        return sentence
    def __str__(self):
        return str(self.prev) + "(-1): " + str(self.fr) + " --> " + str(self.to)

class TransformationBasedLearning:
    def __init__(self):
        self.rules = []
    def get_best_instance(self):
        tags = ENV["tag_dict"].tags
        best_instance = (None, 0)
        good_transform, bad_transform = {}, {}
        for fr in tags:
            for to in tags:
                if (fr == to): continue
                for tag in tags:
                    good_transform[tag] = 0
                    bad_transform[tag] = 0
                for sentence in self.sentences:
                    word_tags = sentence.word_tags
                    for i in range(1, len(word_tags)):
                        prev = word_tags[i - 1].tag
                        if (word_tags[i].tag == fr) and (word_tags[i].correct_tag == to):
                            good_transform[prev] += 1
                        elif (word_tags[i].tag == fr) and (word_tags[i].correct_tag == fr):
                            bad_transform[prev] += 1
                prev = tags[0]
                z_score = good_transform[prev] - bad_transform[prev]
                for tag in tags:
                    good_transform_tag = good_transform[tag]
                    bad_transform_tag = bad_transform[tag]
                    if (z_score < good_transform_tag - bad_transform_tag):
                        z_score = good_transform_tag - bad_transform_tag
                        prev = tag
                if (z_score > best_instance[1]):
                    new_transform = Transform(prev, fr, to)
                    best_instance = (new_transform, z_score)
        return best_instance

    def get_best_transform(self):
        best_transform = (None, -1)
        (instance, score) = self.get_best_instance()
        if (score > best_transform[1]):
            best_transform = (instance, score)
        return best_transform[0]

    def apply_transform(self, best_transform, sentences):
        res = []
        for sentence in sentences:
            applied_transform = best_transform.apply(sentence)
            if (applied_transform != False):
                res.append(applied_transform)
            else:
                res.append(sentence)
        return res
    def complete(self):
        for sentence in self.sentences:
            for word in sentence.word_tags:
                if (word.tag != word.correct_tag):
                    return False
        return True
    def initialize_with_most_likely_tag(self):
        self.sentences = [Sentence(item) for item in self.corpus]
    def learning(self):
        self.initialize_with_most_likely_tag()
        while not self.complete():
            best_transform = self.get_best_transform()
            if not best_transform: break
            self.rules.append(best_transform)
            self.sentences = self.apply_transform(best_transform, self.sentences)
            print(self.rules[-1])
    def fit(self, corpus):
        self.corpus = corpus
        self.learning()
    def predict(self, sentence):
        sentence = Sentence(sentence)
        stop = False
        while not stop:
            stop = True
            old = sentence
            for transfrom in self.rules:
                result = transfrom.apply(sentence)
                if not result: continue
                else: sentence = result
            if old.sentence != sentence.sentence:
                stop = False
        return sentence.sentence

