

from environment.env import ENV
from lib.vnTokenize.Tokenizer import Tokenizer
from lib.parsing.EarleyParsing import EarleyParsing
from lib.vnTagger.Tagger import Tagger
from processor.preprocessing.tfIdf import tfIdf
from processor.preprocessing.Tree import Trie
from processor.preprocessing.Preprocessing import Preprocessing
from os import listdir
import json, pickle, time

def tokenizeAndTagDocuments():
    preprocessor = Preprocessing(specialChar=True, stopword=False, separateSentence=True)
    tokenizer = Tokenizer()
    tagger = Tagger()
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/json/'
    for fname in listdir(LOCAL_DIR):
        with open(LOCAL_DIR + fname, encoding='utf-8') as f:
            data = json.load(f)
        content = data['content']
        preprocessor.fit([content])
        title = data['title']
        link = data['link']

        lines = preprocessor.getResult()[0]
        content = ''
        contentTag = ''
        for line in lines:
            line = tokenizer.tokenize(line)
            content += line + '\n'
            contentTag += tagger.tagging(line) + '\n'

        doc = {'title' : title, 'link' : link, 'content' : content, 'tagged' : contentTag}
        with open(LOCAL_DIR + fname , 'w') as outfile:
            json.dump(doc, outfile, ensure_ascii=False)


def saveTfIdf(model):
    LOCAL_PATH = ENV['BASE_DATA_PATH'] + '/tfidf/tfidf.pkl'
    with open(LOCAL_PATH, 'wb') as f:
        pickle.dump(model, f)

def buildVectorsAndTries():
    tfidf = tfIdf()
    docs, ids = [], []
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/wseg/'
    for fname in listdir(LOCAL_DIR):
        content = open(LOCAL_DIR + fname).read()
        index = int(fname.replace('.txt', ''))
        ids.append(index)
        docs.append(content.lower())
    vectors = tfidf.fit_transform(docs)
    for i in range(len(vectors)):
        vectori = vectors[i]
        index = ids[i]
        f = open(DIR_ROOT + '/documents/vectors/' + str(index) + '.vector', 'w')
        for (word, val) in vectori:
            f.write(word + ' : ' + str(val) + '\n')
        f.close()

        trie = Trie()
        trie.buildTreeDepend(vectori)
        with open(DIR_ROOT + '/documents/tries/' + str(index) + '.pkl', 'wb') as f:
            pickle.dump(trie, f)

    saveTfIdf(tfidf)


def parse(s):
    lower = s.lower()
    BOOL = {"false" : False, "true" : True}
    if lower in BOOL: return BOOL[lower]
    return s

def initEnvironment(pathEnv = 'environment/env.txt'):
    for line in open(pathEnv):
        key_val = line.split()
        if len(key_val) == 2:
            key, val = key_val
            ENV[key] = parse(val)
    print('Initialize environment successfully!')

def saveEnvironment(pathEnv = 'environment/env.txt'):
    f = open(pathEnv, "w")
    for (key, value) in ENV.items():
        if key == key.upper():
            f.write(key + '\t' + str(value) + '\n')
    f.close()
    print("Saved environment successfully!")


def loadVectors():
    vectors = {}
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/vectors/'
    for fname in listdir(LOCAL_DIR):
        vector = []
        for line in open(LOCAL_DIR + fname, encoding='utf-8'):
            word, val = line.split(' : ')
            val = float(val)
            vector.append(tuple([word, val]))
        index = int(fname.replace('.vector', ''))
        vectors[index] = vector
    return vectors
def buildTries(vectors):
    tries = {}
    for (index, vector) in vectors.items():
        trie = Trie()
        trie.buildTreeDepend(vector)
        tries[index] = trie
    return tries
def loadJsonData():
    docs = {}
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/json/'
    for fname in listdir(LOCAL_DIR):
        with open(LOCAL_DIR + fname, encoding='utf-8') as f:
            data = json.load(f)
        index = int(fname.replace('.json', ''))
        docs[index] = data
    return docs
def loadTries():
    tries = {}
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/tries/'
    for fname in listdir(LOCAL_DIR):
        with open(LOCAL_DIR + fname, 'rb') as f:
            trie = pickle.load(f)
        index = int(fname.replace('.pkl', ''))
        tries[index] = trie
    return tries

def loadTfidf():
    DIR_ROOT = ENV['BASE_DATA_PATH']
    FNAME = DIR_ROOT + '/tfidf/tfidf.pkl'
    with open(FNAME, 'rb') as f:
         tfidf = pickle.load(f)
    return tfidf
def loadParsedData():
    DIR_ROOT = ENV['BASE_DATA_PATH']
    LOCAL_DIR = DIR_ROOT + '/documents/parsed/'
    parsedData = dict()
    for fname in listdir(LOCAL_DIR):
        index = int(fname.replace('.txt', ''))
        data = []
        for line in open(LOCAL_DIR + fname, encoding='utf-8'):
            line = line.split()
            if len(line) > 0: data.append(line)
        parsedData[index] = data
    return parsedData

def loadClusters():
    DIR_ROOT = ENV['BASE_DATA_PATH']
    FNAME = DIR_ROOT + '/documents/clusters/cluster.json'
    with open(FNAME, encoding='utf-8') as f:
        data = json.load(f)
    return data

def loadData():
    print('Start loading data...')
    start = time.time()
    docs = loadJsonData()
    vectors = loadVectors()
    tries = buildTries(vectors)
    #loadTries()
    tfidf = loadTfidf()
    parsedData = loadParsedData()
    clusters = loadClusters()
    print('Time for loading data: %f' %(time.time() - start))
    return docs, vectors, tries, tfidf, parsedData, clusters

def generateParse():
    DIR_ROOT = ENV['BASE_DATA_PATH']
    SAVE_DIR = DIR_ROOT + '/documents/parsed/'
    parser = EarleyParsing()
    for fname in listdir(DIR_ROOT + '/documents/wseg/'):
        content = open(DIR_ROOT + '/documents/wseg/' + fname).read()
        index = int(fname.replace('.txt', ''))
        content = content.lower()

        f = open(SAVE_DIR + str(index) + '.txt', 'w')
        for line in content.split('\n'):
            chunk_line = parser.getChunk(line)
            for chunk in chunk_line: f.write(chunk + '  ')
            f.write('\n')
        f.close()

#tokenizeAndTagDocuments()
#buildVectorsAndTries()
#generateParse()
