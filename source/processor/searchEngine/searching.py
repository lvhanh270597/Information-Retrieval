
from setup import initEnvironment, loadData
from lib.vnTokenize.Tokenizer import Tokenizer
from lib.vnTagger.Tagger import Tagger
from lib.parsing.EarleyParsing import EarleyParsing
from processor.preprocessing.Preprocessing import Preprocessing
from processor.expansion.Expansion import ExpansionQuery
from processor.matching.MinimumEditDistance import MinimumEditDistance
from processor.matching.GreedyStringTiling import GreedyStringTiling
from processor.matching.nGramMatching import nGramMatching
from processor.checkspellingandgrammar.CorrectQuery import CorrectQuery
from processor.machinelearning.kmeans.KMean import Point
from math import log2
from processor.ontology.Ontology import Ontology
class Searcher:
    tokenizer = Tokenizer()
    preprocessor = Preprocessing(stopword=False)
    expander = ExpansionQuery()
    tagger = Tagger()
    parser = EarleyParsing()
    corrector = CorrectQuery()
    def likelihood(self, x):
        return -log2(x + 0.0000001)
    def __init__(self):
        initEnvironment()
        self.docs, self.vectors, self.tries,\
        self.tfidf, self.parsedData, self.clusters = loadData()
    def heuristic(self, query, content):
        MED = MinimumEditDistance()
        nGram = nGramMatching()
        GST = GreedyStringTiling()
        rMED = MED.matching(query, content)
        rnGram = nGram.matching(query, content)
        rGST = GST.matching(query, content)
        #return likelihood(rMED) / (likelihood(rGST) + likelihood(rnGram) + 0.000001)
        return rGST + rnGram
    def preprocessing(self):
        BASE_DIR = 'data/ontologies/'
        get = Ontology.load_from_csv(BASE_DIR + 'onto1.csv')
        get.reasoner()
        Special_Words = get.words
        raw_query = self.query.lower()
        for w in Special_Words:
             tmp = w.replace("_"," ")
             raw_query = raw_query.replace(tmp,w)

        self.query = self.tokenizer.tokenize(raw_query)
        print('query = ', self.query)
        self.preprocessor.fit([self.query])
        self.query = self.preprocessor.getResult()[0]
    def buildVector(self):
        self.vector = self.tfidf.transform([self.query])[0]
    def expandVectorQuery(self):
        self.vector = self.expander.expandVector(self.vector)
    def scoring(self):
        self.score = {}
        for (index, tree) in self.tries.items():
            sim = tree.cosine(self.vector)
            self.score[index] = sim
    def correctQuery(self):
        self.query = self.corrector.Correct(self.query.lower())

    def calculateCluster(self):
        point = Point(self.vector)
        self.distanceToCenters = []
        centers = self.clusters['centers']
        for i in range(len(centers)):
            center = Point(centers[i])
            self.distanceToCenters.append(point.distance(center))
        max_elems = max(self.distanceToCenters)
        for i in range(len(centers)):
            self.distanceToCenters[i] /= max_elems

    def ranking(self):
        self.rank = sorted(self.score.items(), key=lambda kv: kv[1])[::-1][:10]
        self.score = dict()
        query_tagged = self.tagger.tagging(self.query)
        query_parsed = self.parser.getChunk(self.query)
        for item in self.rank:
            index = item[0]
            doc_of_index = self.docs[index]
            tagged_of_this = doc_of_index['tagged']
            title_of_this = doc_of_index['title']

            h_content = self.heuristic(query_tagged, tagged_of_this)
            h_title = self.heuristic(self.query, title_of_this)

            lines_of_doc = self.parsedData[index]
            heuristic_parse, cnt = 0, len(lines_of_doc)
            for chunk_of_line in lines_of_doc:
                heuristic_parse += self.parser.getSimilarity(query_parsed, chunk_of_line)

            heuristic_parse = heuristic_parse / (cnt + 0.00001)
            print('heuristic parse: %f' %heuristic_parse)
            self.score[index] = h_content + h_title + heuristic_parse

            cluster_of_index = self.clusters['ids'][index - 1]
            distance_to_cluster = self.distanceToCenters[cluster_of_index]
            print(distance_to_cluster)
            self.score[index] /= distance_to_cluster

        self.rank = sorted(self.score.items(), key=lambda kv: kv[1])[::-1]

    def getResults(self):
        results = []
        for index, score in self.rank:
            this_doc = self.docs[index]
            content = this_doc['content'].replace('_', ' ')[:200]
            data = [this_doc['title'], this_doc['link'], content]
            results.append(data)
        return results
    def searching(self, query):
        self.query = query
        print(self.query)
        old_query = self.query
        #self.correctQuery()
        print('Tìm kiếm: %s thay cho %s' %(self.query, old_query))
        self.preprocessing()
        print(self.query)
        self.buildVector()
        print(self.vector)

        self.calculateCluster()

        self.expandVectorQuery()
        self.scoring()
        self.ranking()
