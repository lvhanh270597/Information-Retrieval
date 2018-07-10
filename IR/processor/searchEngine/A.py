# -*- coding: utf-8 -*-
import numpy as np
import csv
import copy

class Ontology:
    """docstring for Onto"""
    Class = ["Object", "Entity", "Other"]
    SubClass = ["Algorithm", "Book", "Field", "Location", "Method", "Person"]
    Relation = ["isLessRelateOf", "isRelateOf", "isSynonymOf", "isTheSameAs"]

    DataProperty = ["Name", "Info"]
    PersonData = ["Birthday", "DateOfDeath", "Education", "Field", "Nationality"]
    BookData = ["PublicationDate"]

    AllDataProperty = ["Name", "Info",
                       "Birthday", "DateOfDeath", "Education", "Field", "Nationality",
                       "PublicationDate"]

    AllDataName = ["Tên", "Thông tin",
                   "Ngày sinh", "Ngày mất", "Học vấn", "Lĩnh vực", "Quốc gia",
                   "Ngày xuất bản"]

    def __init__(self):

        self.onto = {}
        self.words = []

    def initword(self, word, wclass=''):
        if word not in self.onto:
            word = word.replace(' ', '')
            self.words.append(word)
            self.onto[word] = {'Data': {}, 'Relation': {}, 'Class': ''}
        if wclass != '':
            self.onto[word]['Class'] = wclass

    # Thêm Relation giữa word1 và word2
    def addRelation(self, word1, relation, word2):
        if word1 == '' or word2 == '' or word1 == word2:
            return
        word1 = word1.replace(' ', '')
        word2 = word2.replace(' ', '')
        self.initword(word1)
        self.initword(word2)
        if relation not in self.onto[word1]["Relation"]:
            self.onto[word1]["Relation"][relation] = [word2]
        else:
            if word2 not in self.onto[word1]["Relation"][relation]:
                self.onto[word1]["Relation"][relation].append(word2)
        if relation not in self.onto[word2]["Relation"]:
            self.onto[word2]["Relation"][relation] = [word1]
        else:
            if word1 not in self.onto[word2]["Relation"][relation]:
                self.onto[word2]["Relation"][relation].append(word1)
        pass

    # Thêm data property
    def addData(self, word, data, value):
        if word == '' or value == '':
            return
        self.initword(word)
        self.onto[word]["Data"][data] = value
        pass

    def reasoner(self):
        close = []
        close1 = []
        for i in range(len(self.words)):
            if "isTheSameAs" in self.onto[self.words[i]]['Relation'] and self.words[i] not in close:
                samewords = [self.words[i]]
                for w in samewords:
                    if "isTheSameAs" in self.onto[w]['Relation']:
                        # samewords = samewords +
                        # [x for x in self.onto[w]['Relation']["isTheSameAs"] if x not in samewords]
                        for x in self.onto[w]['Relation']["isTheSameAs"]:
                            if x not in samewords:
                                samewords.append(x)
                close = close + samewords
                for j in range(1,len(samewords)):
                    #for c in self.onto[samewords[j]]['Class']:
                        #if c not in self.onto[samewords[0]]['Class']:
                            #self.onto[samewords[0]]['Class'].append(c)
                    if not self.onto[samewords[0]]['Class'] and self.onto[samewords[j]]['Class']:
                        self.onto[samewords[0]]['Class'] = self.onto[samewords[j]]['Class']
                    for rela in self.onto[samewords[j]]['Relation'].keys():
                        for rela_word in self.onto[samewords[j]]['Relation'][rela]:
                            self.addRelation(samewords[0], rela, rela_word)
                    for data in self.onto[samewords[j]]['Data'].keys():
                        if self.onto[samewords[j]]['Data'][data] != "":
                            self.onto[samewords[0]]['Data'][data] = self.onto[samewords[j]]['Data'][data]
                for j in range(1, len(samewords)):
                    self.copyWord(samewords[0], samewords[j])
            if "isSynonymOf" in self.onto[self.words[i]]['Relation'] and self.words[i] not in close1:
                synonymwords = [self.words[i]]
                for w in synonymwords:
                    if "isSynonymOf" in self.onto[w]['Relation']:
                        for x in self.onto[w]['Relation']["isSynonymOf"]:
                            if x not in synonymwords:
                                synonymwords.append(x)
                close1 = close1 + synonymwords
                for w in synonymwords:
                    self.onto[w]['Relation']['isSynonymOf'] = copy.deepcopy(synonymwords)
                    self.onto[w]['Relation']['isSynonymOf'].remove(w)
            if "isRelateOf" in self.onto[self.words[i]]['Relation']:
                for rela_word in self.onto[self.words[i]]['Relation']['isRelateOf']:
                    if "isRelateOf" in self.onto[rela_word]['Relation']:
                        for w in self.onto[rela_word]['Relation']['isRelateOf']:
                            if not self.findRelation(self.words[i], w):
                                self.addRelation(self.words[i], 'isLessRelateOf', w)
        pass

    # Tìm Relation giữa word1 và word2
    def findRelation(self, word1, word2):
        if word1 not in self.onto or word2 not in self.onto:
            return []
        result = []
        for i in self.onto[word1]['Relation']:
            if word2 in self.onto[word1]['Relation'][i]:
                result.append(i)
        return result
        pass

    def deleteWord(self, word):
        if word not in self.onto:
            return
        for rela in self.onto[word]['Relation']:
            for w in self.onto[word]['Relation'][rela]:
                if w in self.onto and word in self.onto[w]['Relation'][rela]:
                    self.onto[w]['Relation'][rela].remove(word)
        del self.onto[word]
        self.words.remove(word)
        pass

    # copy word2 = word1
    def copyWord(self, word1, word2):
        if word1 not in self.onto:
            return
        self.initword(word2)
        self.onto[word2] = copy.deepcopy(self.onto[word1])
        for rela in self.onto[word2]['Relation'].keys():
            if word2 in self.onto[word2]['Relation'][rela]:
                self.onto[word2]['Relation'][rela].remove(word2)
                self.onto[word2]['Relation'][rela].append(word1)
            for rela_word in self.onto[word2]['Relation'][rela]:
                self.addRelation(rela_word, rela, word2)
                #self.onto[rela_word]['Relation'][rela].append(word2)

    def printWord(self, word):
        if word in self.onto:
            result = word + ': \n'
            result += '\tClass: ' + self.onto[word]['Class'] + '\n'
            result += '\tRelation Properties:\n'
            for rela in self.onto[word]['Relation']:
                result += '\t\t' + rela + ': ' + ', '.join(self.onto[word]['Relation'][rela]) + '\n'
            result += '\tData Properties:\n'
            for data in self.onto[word]['Data']:
                result += '\t\t' + data + ': ' + self.onto[word]['Data'][data] + '\n'
            result += '========================================================================'
            print(result)
        pass

    def printDataWord(self, word):
        if word in self.onto:
            result = word + ': \n'
            result += '\tData Properties:\n'
            for data in self.onto[word]['Data']:
                result += '\t\t' + data + ': ' + self.onto[word]['Data'][data] + '\n'
            result += '========================================================================'
            print(result)
            return result
        pass

    def printAllWord(self):
        for word in self.onto:
            self.printWord(word)
        pass

    def insert_from_file(self, file):
        with open(file, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            data = [r for r in reader]
        header = data[0]
        data.pop(0)
        for row in data:
            self.initword(row[0])
            for i in range(1, len(row)):
                if header[i] == 'Class':
                    self.onto[row[0]]['Class'] = row[i]
                elif header[i] in Ontology.Relation:
                    row[i] = row[i].replace(' ', '')
                    rela = row[i].split(',')
                    for r in rela:
                        self.addRelation(row[0], header[i], r)
                else:
                    self.addData(row[0], header[i], row[i])
        pass

    def save2csv(self, file):
        with open(file, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Word', 'Class'] + Ontology.Relation + Ontology.AllDataProperty)
            for word in self.onto.keys():
                row = [word, self.onto[word]['Class']]
                for rela in Ontology.Relation:
                    if rela in self.onto[word]['Relation']:
                        row.append(','.join(self.onto[word]['Relation'][rela]))
                    else:
                        row.append('')
                for data in Ontology.AllDataProperty:
                    if data in self.onto[word]['Data']:
                        row.append(self.onto[word]['Data'][data])
                    else:
                        row.append('')
                writer.writerow(row)
        pass

    # Load dữ liệu
    @staticmethod
    def load_from_csv(filename):
        x = Ontology()
        x.insert_from_file(filename)
        return x

    @staticmethod
    def load(filename):
        return np.load(filename).item()

    # lưu dữ liệu: Ontology.save()
    @staticmethod
    def save_to_csv(filename, onto):
        onto.save2csv(filename)

    @staticmethod
    def save(filename, onto):
        np.save(filename, onto)


#a = Ontology.load('onto.npy')
#a = Ontology.load_from_csv('a.csv')
#print (a.onto)
'''
a.addRelation("thuật_toán","isSynonymOf","thuật_giải")
a.addRelation("thuật_toán","isSynonymOf","giải_thuật")
a.addRelation("giải_thuật","isSynonymOf","algorithm")
a.onto['giải_thuật']['Class'] = [Ontology.Class[0]]
a.addData("thuật_toán","Field","IT")
a.addData("giải_thuật","Name","chiaasdfc")
a.addData("algorithm","Info","aaaaaaaaaaaa")

a.addRelation('a','isRelateOf','b')
a.addRelation('b','isRelateOf','e')
a.addRelation('b','isRelateOf','c')
a.reasoner()
a.save_to_csv('a.csv')
'''
