

from processor.ontology.Relation import Relation

class ExpansionQuery:
    def __init__(self, weight=None):
        self.relation = Relation()
        if weight is None:
            self.weight = {
                'isTheSameAs' : 1,
                'isSynonymOf' : 0.85,
                'isRelateOf' : 0.7,
                'isLessRelateOf' : 0.5
            }
        else: self.weight = weight
    def getDictOf(self, word, val, rel):
        result = dict()
        words = self.relation.getWordsOf(word, rel)
        for new_word in words:
            if new_word not in result:
                result[new_word] = val * self.weight[rel]
        return result
    def expandVector(self, vector):
        vector_result = []
        addition = dict()
        for word, val in vector: addition[word] = val
        relationNames = self.weight.keys()
        for word, val in vector:
            for rel in relationNames:
                for key, value in self.getDictOf(word, val, rel).items():
                    if key not in addition:
                        addition[key] = value
                    else:
                        addition[key] = max(addition[key], value)
        for word, val in addition.items():
            vector_result.append(tuple([word, val]))
        return vector_result
