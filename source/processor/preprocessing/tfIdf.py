
from math import log2, log10

class tfIdf:

    def getIdf(self, term):
        if term not in self.idf: return 0
        else: return self.idf[term]
    def fit(self, documents):
        self.docs = documents
        self.size = len(documents)
        self.docFreq = dict()
        self.idf = dict()
        for doc in self.docs:
            termFreqi = {}
            terms = doc.split()
            for term in terms:
                if term not in termFreqi:
                    termFreqi[term] = 1
                else: termFreqi[term] += 1
            for term in termFreqi:
                if term not in self.docFreq:
                    self.docFreq[term] = 1
                else: self.docFreq[term] += 1
        for term in self.docFreq:
            self.idf[term] = log2(self.size / self.docFreq[term])
    def fit_transform(self, documents):
        self.docs = documents
        self.size = len(documents)

        self.termFreq = []
        self.docFreq = dict()
        self.idf = dict()

        for doc in self.docs:
            termFreqi = {}
            terms = doc.split()
            for term in terms:
                if term not in termFreqi:
                    termFreqi[term] = 1
                else: termFreqi[term] += 1
            for term in termFreqi:
                if term not in self.docFreq:
                    self.docFreq[term] = 1
                else: self.docFreq[term] += 1
            self.termFreq.append(termFreqi)

        for term, val in self.docFreq.items():
            if val == self.size: continue
            self.idf[term] = log2(self.size / val)

        vectors = []
        for termFreqi in self.termFreq:
            vectori = []
            for term, val in termFreqi.items():
                idf = self.getIdf(term)
                if idf == 0: continue
                item = (term, val * idf)
                vectori.append(item)
            vectors.append(vectori)
        return vectors
    def transform(self, documents):
        vectors = []
        for doc in documents:
            vectori = []
            termFreqi = {}
            terms = doc.split()
            for term in terms:
                if term not in termFreqi:
                    termFreqi[term] = 1
                else: termFreqi[term] += 1
            for term, val in termFreqi.items():
                idf = self.getIdf(term)
                if idf == 0: continue
                item = (term, val * idf)
                vectori.append(item)
            vectors.append(vectori)
        return vectors
