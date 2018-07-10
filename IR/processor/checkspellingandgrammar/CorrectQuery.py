from collections import defaultdict
import glob
import codecs
import operator
import math
import os


class CorrectQuery():
    BASE_DIR = 'data/spelling/'

    def __init__(self):
        self.Load_TelexVni("Telex_Vni.txt")
        self.LoadNGram()

    def writefile(self, filename, st):
        file = codecs.open(self.BASE_DIR + filename, "w", "utf-8")
        file.write(str(st))
        file.close()

    # Lấy cách đổi từ thành telex vni
    def Load_TelexVni(self, filename):
        global _TelexVni
        _TelexVni = []
        file = codecs.open(self.BASE_DIR + filename, "r", "utf-8")
        for line in file.readlines():
            if (line.split() and '#' not in line):
                _TelexVni.append(line.split())
        file.close()

    # Ví dụ ẩ -> aar
    def toTelex(self, word):
        kq = word
        for i in word:
            for each in _TelexVni:
                if (i == each[0]):
                    kq = kq.replace(i, str(each[1]))
        return kq

    # Ví dụ ẩ -> a63
    def toVni(self, word):
        kq = word
        for i in word:
            for each in _TelexVni:
                if (i == each[0]):
                    kq = kq.replace(i, str(each[2]))
        return kq

    # Tính khoảng cách ngắn nhất để từ s1 đổi thành s2
    def MinimumDist(self, s1, s2):
        len1 = len(s1)
        len2 = len(s2)

        matrix = [[0] * (len2 + 1) for _ in range(len1 + 1)]

        for i in range(0, len1 + 1):
            matrix[i][0] = i
        for j in range(0, len2 + 1):
            matrix[0][j] = j
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                if (s1[i - 1] == s2[j - 1]):
                    matrix[i][j] = matrix[i - 1][j - 1]
                else:
                    # Xóa tốn 1 đơn vị, thay thế tốn 2 đơn vị
                    matrix[i][j] = min(matrix[i - 1][j - 1] + 2, matrix[i - 1][j] + 1, matrix[i][j - 1] + 1)
        return matrix[len1][len2]

    # Tính các từ có khả năng thay thế cho query cao nhất
    def ChangeWord(self, query):
        words = query.split()
        can_change = []  # Các từ có khả năng đổi cao nhất
        for w in words:
            if w not in _SingleWords:
                RefTerm1 = defaultdict(list)  # Tính theo telex
                RefTerm2 = defaultdict(list)  # Tính theo vni
                RefTerm3 = defaultdict(list)  # Tính theo không dấu
                for word in _SpecialSingle:
                    RefTerm1[word].append(self.MinimumDist(self.toTelex(w), self.toTelex(word)))
                    RefTerm2[word].append(self.MinimumDist(self.toVni(w), self.toVni(word)))
                    tmp = self.toVni(word)
                    tmp1 = tmp
                    for x in tmp1:
                        if (x >= '0' and x <= '9'):
                            tmp = tmp.replace(x, "")

                    RefTerm3[word].append(self.MinimumDist(w, tmp))

                RefTerm1 = sorted(RefTerm1.items(), key=operator.itemgetter(1))
                RefTerm2 = sorted(RefTerm2.items(), key=operator.itemgetter(1))
                RefTerm3 = sorted(RefTerm3.items(), key=operator.itemgetter(1))

                Select = ""
                tmp_max = -1.0

                if RefTerm3[0][1][0] == 0:
                    RefTerm3 = [item for item in RefTerm3 if item[1][-1] < 1]
                    for i in range(len(RefTerm3)):
                        can_change.append(RefTerm3[i][0])
                        if tmp_max < unigram[RefTerm3[i][0]]:
                            Select = RefTerm3[i][0]
                            tmp_max = unigram[RefTerm3[i][0]]
                # print(RefTerm3)
                else:
                    min_dist = min(RefTerm1[0][1][0], RefTerm2[0][1][0]) + 1
                    RefTerm1 = [item for item in RefTerm1 if item[1][-1] < min_dist]
                    RefTerm2 = [item for item in RefTerm2 if item[1][-1] < min_dist]
                    for i in range(len(RefTerm1)):
                        if RefTerm1[i][0] not in can_change:
                            can_change.append(RefTerm1[i][0])
                        if tmp_max < unigram[RefTerm1[i][0]]:
                            Select = RefTerm1[i][0]
                            tmp_max = unigram[RefTerm1[i][0]]
                    #			print("_TelexVni",tmp_max, " : ", Select)
                    for i in range(len(RefTerm2)):
                        if RefTerm2[i][0] not in can_change:
                            can_change.append(RefTerm2[i][0])
                        if tmp_max < unigram[RefTerm2[i][0]]:
                            Select = RefTerm2[i][0]
                            tmp_max = unigram[RefTerm2[i][0]]
        #			print("_Vni",tmp_max, " : ", Select)

        #		print(Select)
        return can_change

    # Tiền xử lý xóa các từ xàm trong toàn bộ tài liệu
    def ReProcessing(self, name):
        st = ""
        path = "data/spelling/Docs/"
        for filename in glob.glob(os.path.join(path, "*.txt")):
            docs = []
            file = open(self.BASE_DIR + filename, encoding="utf8")
            for line in file:
                line = line.replace("\ufeff", "")
                line = line.lower().split('.')
                for sentence in line:
                    sentence = "<s> " + sentence
                    sentence += " </s>"
                    words = sentence.split()
                    for w in words:
                        st += w
                        st += " "
        Delete = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '!', '@', '#', '$', '%', '^', '&', '*',
                  '(', ')', '_', '+', '[', ']', '{', '}', ':', ';', '"', ',', '.', '?', '\'', '\\', '|', '*', '+']
        for x in Delete:
            st = st.replace(x, "")
        self.writefile(name, st)

    # Tạo NGram
    def CreateNGram(self, filename):
        unigram = {}
        bigram = {}

        file = open(self.BASE_DIR + filename, encoding="utf8")
        words = file.read()
        file.close()
        words = words.split(" ")
        for i in range(len(words) - 1):
            if words[i] != '':  # Nếu từ hiện tại khác rỗng
                key = "false"
                x = i + 1
                while x + 1 < len(words) and words[x] == '':  # Tìm từ phía sau khác rỗng
                    x = x + 1
                if words[x] != '':
                    key = words[i] + ' ' + words[x]

                if key != "false":
                    if key in bigram.keys():
                        bigram[key] += 1
                    else:
                        bigram[key] = 1

                if words[i] in unigram.keys():
                    unigram[words[i]] += 1
                else:
                    unigram[words[i]] = 1

        self.writefile("Bigram.txt", str(bigram))
        self.writefile("Unigram.txt", str(unigram))

    #	print(unigram)
    #	print(bigram)

    def LoadNGram(self):
        global _Nterm, unigram, bigram, _SingleWords, _SpecialSingle
        _SingleWords = []  # Các từ
        _Nterm = 0
        unigram = {}
        bigram = {}

        file = open(self.BASE_DIR + "Special_Single.txt", encoding="utf8")
        words = file.read()
        file.close()
        _SpecialSingle = words.split()

        # load unigram
        file = open(self.BASE_DIR + "Unigram.txt", encoding="utf8")
        words = file.read()
        file.close()
        words = words.replace("{", "")
        words = words.replace("}", "")
        words = words.replace("'", "")
        words = words.replace(":", "")
        words = words.replace(", ", ",")
        words = words.split(",")
        for tup in words:
            tmp = tup.split()
            unigram[tmp[0]] = float(tmp[1])
            _Nterm += float(tmp[1])
            _SingleWords.append(tmp[0])

        # load bigram
        file = open(self.BASE_DIR + "Bigram.txt", encoding="utf8")
        words = file.read()
        file.close()
        words = words.replace("{", "")
        words = words.replace("}", "")
        words = words.replace("'", "")
        words = words.replace(":", "")
        words = words.replace(", ", ",")
        words = words.split(",")
        for tup in words:
            tmp = tup.split()
            key = tmp[0] + " " + tmp[1]
            bigram[key] = float(tmp[2])
        self.writefile("SingleWord.txt", _SingleWords)

    def CalculateEntropy(self, sentence):
        _Confidence_uni = 0.95
        _Confidence_bi = 0.95

        X1 = (1 - _Confidence_uni) / _Nterm

        words = sentence.split()
        for i in range(len(words) - 1):
            P1 = X1
            P2 = (1 - _Confidence_bi) * P1

            key = words[i] + ' ' + words[i + 1]

            if (words[i] in unigram.keys()):
                P1 = _Confidence_uni * (unigram[words[i]] / _Nterm) + X1

            if (key in bigram.keys()):
                P2 = _Confidence_bi * (bigram[key] / unigram[words[i]]) + (1 - _Confidence_bi) * P1

        return P2

    def Correct(self, st):
        change_to = ""
        st1 = st.lower()
        sentence = '<s> ' + st1
        sentence = sentence + ' </s>'

        arr_sentence = sentence.split()

        for i in range(1, len(arr_sentence) - 1):

            if arr_sentence[i] not in _SingleWords:  # Nếu là từ chưa xuất hiện trong toàn tài liệu

                can_change = []  # Các từ có khả năng cao để thay thế
                can_change = self.ChangeWord(arr_sentence[i])

                change_to += arr_sentence[i] + " --> "
                change_to += str(can_change)
                change_to += "\n"
                xs_term = {}

                for word in can_change:
                    lhs = arr_sentence[i - 1] + ' ' + word
                    rhs = word + ' ' + arr_sentence[i + 1]
                    xs_term[word] = -math.log(2,
                                              self.CalculateEntropy(lhs) * self.CalculateEntropy(rhs))  # Tính entropy

                tmp_max = 0
                for j in xs_term:
                    if xs_term[j] > tmp_max:
                        tmp_max = xs_term[j]
                for j in xs_term:
                    if xs_term[j] == tmp_max:
                        sentence = sentence.replace(arr_sentence[i], j)
                        break
        sentence = sentence.replace("<s> ", "")
        sentence = sentence.replace(" </s>", "")
        #	print(change_to,"\n",sentence)
        st = st.split()
        sentence = sentence.split()
        kq = ""
        for i in range(len(st)):
            tmp = sentence[i]
            if str(st[i][0]) > 'A' and str(st[i][0]) < 'Z':
                tmp = tmp.capitalize()
            kq += tmp
            kq += " "
        return kq

# a.Correct("thuật1 toán1 quicksort1 thuat gidi me gie quy hoach đookng")
