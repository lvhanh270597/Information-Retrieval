
from processor.ontology.Ontology import Ontology


class Relation:
    def __init__(self):
        BASE_DIR = 'data/ontologies'
        self.ontology = Ontology.load_from_csv(BASE_DIR + '/onto1.csv')
        self.ontology.reasoner()
    def getRelationBetweenTwoWords(self, word1, word2):
        return self.ontology.findRelation(word1, word2)
    def getWordsOf(self, word, rel='isSynonymOf'):
        if word not in self.ontology.onto: return []
        data = self.ontology.onto[word]['Relation']
        if rel in data: return data[rel]
        else: return []
