
class MinimumEditDistance:
    def matching(self, sentence1, sentence2):
        listWords1 = sentence1.split()
        listWords2 = sentence2.split()
        m = len(listWords1) + 1
        n = len(listWords2) + 1

        tbl = {}
        for i in range(m): tbl[i, 0] = i
        for j in range(n): tbl[0, j] = j
        for i in range(1, m):
            for j in range(1, n):
                cost = 0 if listWords1[i-1] == listWords2[j-1] else 1
                tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)

        return tbl[i,j] / max(n, m)
