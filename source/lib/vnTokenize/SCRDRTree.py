
class Node:
    def __init__(self, _typeCmp, _valCmp, _indexCmp, _val):
        self._typeCmp = _typeCmp
        self._valCmp = _valCmp
        self._indexCmp = _indexCmp
        self._val = _val
        self._child = {'if-not' : -1, 'except' : -1}
    def checkRule(self, window_words, window_tags):
        if (self._typeCmp == 'true'): return True
        if (self._typeCmp == 'tag'):
            return window_tags[self._indexCmp] == self._valCmp
        if (self._typeCmp == 'word'):
            return window_words[self._indexCmp] == self._valCmp
    def leaf(self):
        return (self._child['if-not'] == None) \
               and (self._child['except'] == None)
    def add(self, nodeChild, edge):
        self._child[edge] = nodeChild
    def __str__(self):
        if self._typeCmp == 'true':
            return "if true then tag = " + self._val
        return 'if ' + self._typeCmp + "-" + str(self._indexCmp) + " == " + self._valCmp + " then tag = " + str(self._val)
class SCRDRTree:
    def __init__(self):
        self.listNodes = []
        root = Node("true", None, None, "B")
        self.listNodes.append(root)
    def getTag(self, window_words, window_tags):
        return self.reasoning(0, window_words, window_tags)
    def reasoning(self, indexNode, window_words, window_tags):
        node = self.listNodes[indexNode]
        if node.checkRule(window_words, window_tags):
            #if node.leaf(): return node._val
            res = node._val
            exceptNode = node._child['except']
            if exceptNode != -1:
                res = self.reasoning(exceptNode, window_words, window_tags)
            if res == None:
                res = node._val
            return res
        else:
            if_notNode = node._child['if-not']
            if if_notNode == -1:
                return None
            else:
                return self.reasoning(if_notNode, window_words, window_tags)

    def getFartherNode(self, indexNode, words, tags):
        node = self.listNodes[indexNode]
        if node.checkRule(words, tags):
            exceptNode = node._child['except']
            if exceptNode != -1:
                return self.getFartherNode(exceptNode, words, tags)
            else:
                return (indexNode, "except")
        else:
            if_notNode = node._child['if-not']
            if if_notNode != -1:
                return self.getFartherNode(if_notNode, words, tags)
            else:
                return (indexNode, "if-not")

    def addNode(self, indexParent, nextEdge, node):
        #print(indexParent)
        parent = self.listNodes[indexParent]
        self.listNodes.append(node)
        parent._child[nextEdge] = len(self.listNodes) - 1

    def deleteNode(self, indexParent, nextEdge):
        parent = self.listNodes[indexParent]
        parent._child[nextEdge] = -1
        del self.listNodes[-1]

    def getScoreInNode(self, indexNode):
        '''
        only come over here
        '''
        #percent, n = 0, len(self.correctLabel)
        correct, allItems = 0, 0
        position = [indexNode, len(self.listNodes) - 1]
        for i in range(len(self.correctLabel)):
            words, tags = self.windows[i]
            correctTag = self.correctLabel[i]
            farther, edge = self.getFartherNode(0, words, tags)
            if farther in position:
                allItems += 1
                tag = self.getTag(words, tags)
                correct += (tag == correctTag)
            '''percent2 = int((i / n) * 100)
            if percent2 > percent:
                percent = percent2
                print('#', end='')'''
        #print()
        #print(correct, allItems)
        return correct / (allItems + 0.00001)

    def createNode(self, indexWrong):
        words, tags = self.windows[indexWrong]
        correctTag = self.correctLabel[indexWrong]
        (indexNode, nextEdge) = self.getFartherNode(0, words, tags)
        window_size = len(words)
        maxScore = -1
        choseNode = None
        for i in range(window_size):
            node = Node("tag", tags[i], i, correctTag)
            #print("Test node:", node)
            # add a node into the indexNode throw nextEdge
            self.addNode(indexNode, nextEdge, node)
            # calculate score of this node
            score = self.getScoreInNode(indexNode)
            if (score > maxScore):
                maxScore = score
                choseNode = node
            self.deleteNode(indexNode, nextEdge)

            node = Node("word", words[i], i, correctTag)
            #print("Test node:", node)
            self.addNode(indexNode, nextEdge, node)
            score = self.getScoreInNode(indexNode)
            if (score > maxScore):
                maxScore = score
                choseNode = node
            self.deleteNode(indexNode, nextEdge)

        if (maxScore > self.threshold):
            self.addNode(indexNode, nextEdge, choseNode)
            #print(maxScore, choseNode)
        # add to indexNode

    def learning(self):
        stop = False
        cnt = 0
        while not stop:
            stop = True
            for i in range(len(self.correctLabel)):
                words, tags = self.windows[i]
                correctTag = self.correctLabel[i]
                tag = self.getTag(words, tags)
                if tag != correctTag:
                    indexWrong = i
                    self.createNode(indexWrong)
                    print("current", indexWrong)
                    stop = False
            cnt += 1
            if cnt > 3:
                print("Number of learning > 10")
                break
            print("Number of learning = ", cnt)
        print("OK")

    def fit(self, windows, correctLabel, threshold = 0.1):
        self.windows = windows
        self.correctLabel = correctLabel
        self.threshold = threshold
        self.learning()

    def predict(self, windows):
        y = []
        for window in windows:
            words, tags = window
            y.append(self.getTag(words, tags))
        return y

    def travel(self, indexNode):
        node = self.listNodes[indexNode]
        print(node)
        if node._child["except"] > -1:
            print(indexNode, "has child except")
            self.travel(node._child["except"])
        if node._child["if-not"] > -1:
            print(indexNode, "has child if-not")
            self.travel(node._child["if-not"])
