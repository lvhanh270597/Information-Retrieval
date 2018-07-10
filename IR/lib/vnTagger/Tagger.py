
from lib.environment.env import ENV
import pickle, operator

class Tagger:
    def __init__(self):
        with open(ENV['TAG_MODEL_PATH'], 'rb') as f:
            self.tagger = pickle.load(f)
    def tagging(self, sentence):
        return self.tagger.predict(sentence)
    def getTags(self, word):
        return ENV["tag_dict"].searchWord(word)
    def getEnglishTags(self, word):
        Map = {
            "A"  :  ["JJ", "JJR", "JJS"],
            "R"  :  ["RB", "RBR", "RBS"],
            "V"  :  ["VB", "MD"],
            "Nc" :  ["UNN"],
            "C"  :  ["CC"],
            "M"  :  ["CD"],
            "D"  :  ["DT"],
            "Np" :  ["NNP"],
            "N"  :  ["NN"],
            "E"  :  ["IN"]
        }

        vietnamTags = self.getTags(word)
        sorted_by_value = sorted(vietnamTags.items(), key=lambda kv: kv[1])
        cnt = 0
        s = sum([y for (x, y) in sorted_by_value])
        vietnamTags = []
        for (x, y) in sorted_by_value[::-1]:
            vietnamTags.append(x)
            cnt += y
            if cnt / s > 0.6: break
        englishTags = []
        for tag in vietnamTags:
            if tag in Map:
                englishTags += Map[tag]
        if len(englishTags) == 0: englishTags = ["NNP"]
        return englishTags

