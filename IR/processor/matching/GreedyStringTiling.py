
class GreedyStringTiling:
    def __init__(self, minimumMatchLength = 2):
        self.minimumMatchLength = minimumMatchLength
    def matching(self, sentence1, sentence2):
        listWords1 = sentence1.split()
        listWords2 = sentence2.split()
        n_1, n_2 = len(listWords1), len(listWords2)
        unmark1 = [True] * n_1
        unmark2 = [True] * n_2
        lengthOfTokensTiled = 0
        while True:
            matches = []
            maxMatch = self.minimumMatchLength
            for p in range(n_1):
                if unmark1[p]:
                    t = 0
                    while t < n_2:
                        if unmark2[t]:
                            j = 0
                            while True:
                                t_j, p_j = t + j, p + j
                                if t_j < n_2 and p_j < n_1 and\
                                    unmark2[t_j] and unmark1[p_j]\
                                    and listWords1[p + j] == listWords2[t + j]:
                                    j += 1
                                else: break
                            if j == maxMatch: matches.append(tuple([p, t, j]))
                            else:
                                if j > maxMatch:
                                    matches = [tuple([p, t, j])]
                                    maxMatch = j
                            t += max(j, 1)
                        else: t += 1
            for p, t, maxMatch in matches:
                for j in range(maxMatch):
                    unmark1[p + j] = False
                    unmark2[t + j] = False
                lengthOfTokensTiled += maxMatch
            if len(matches) == 0: break
        return lengthOfTokensTiled / max(min(n_1, n_2), 0.000001)



