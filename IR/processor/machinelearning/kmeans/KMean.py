
import os, math, json

class Point:
    def __init__(self, vector):
        self._vect = vector[:]
    def distance(self, point):
        common = self._vect + point._vect
        sorted_x = sorted(common, key=lambda kv: kv[0])
        sorted_x += [(-1, 0)]
        dist, n = 0, len(sorted_x)
        i = 0
        while i < n - 1:
            if sorted_x[i][0] == sorted_x[i + 1][0]:
                dist += (sorted_x[i][1] - sorted_x[i + 1][1]) ** 2
                i += 1
            else:
                dist += (sorted_x[i][1]) ** 2
            i += 1
        return math.sqrt(dist)
    def sumOfTwoPoint(self, point):
        common = self._vect + point._vect
        sorted_x = sorted(common, key=lambda kv: kv[0])
        sorted_x += [(-1, 0)]
        kq, n = [], len(sorted_x)
        i = 0
        while i < n - 1:
            if sorted_x[i][0] == sorted_x[i + 1][0]:
                kq += [[sorted_x[i][0], sorted_x[i][1] + sorted_x[i + 1][1]]]
                i += 1
            else:
                kq += [[sorted_x[i][0], sorted_x[i][1]]]
            i += 1
        return kq
    def __str__(self):
        return str(self._vect)

class Cluster:
    def __init__(self):
        self._lop = []
        self._center = None
    def get_center(self):
        p_center = Point([])
        for p in self._lop:
            p_center = Point(p_center.sumOfTwoPoint(p))
        for i in range(len(p_center._vect)):
            p_center._vect[i][1] /= len(self._lop)
        return p_center
    def set_list_of_points(self, lop):
        self._lop = lop[:]
        self._center = self.get_center()
    def add_a_point(self, point):
        self._lop.append(point)
    def update(self):
        self._center = self.get_center()
    def remove_all_points(self):
        self._lop = []
    def __str__(self):
        if (self == None): return "None";
        s = '('
        for p in self._lop: s += p.__str__() + "\n"
        s += ')'
        return s

class K_means:
    def __init__(self, k, lop):
        self._lop = lop[:]
        self._IDs = []
        self._k = k
        self._clusters = []
        for i in range(k):
            self._clusters.append(Cluster())
        for i in range(k):
            self._clusters[i].set_list_of_points([lop[i]])
            self._clusters[i]._center = lop[i]
            self._IDs.append(i)
        for i in range(k, len(lop)):
            cluster_index = self.find_closest_cluster(lop[i])
            self._IDs.append(cluster_index)
            self._clusters[cluster_index].add_a_point(lop[i])
        print(self._IDs)
        for cluster in self._clusters:
            print(len(cluster._lop), cluster._center)
    def find_closest_cluster(self, point):
        closest_distance = point.distance(self._clusters[0]._center)
        index = 0
        for i in range(1, self._k):
            d_i = point.distance(self._clusters[i]._center)
            if (d_i < closest_distance):
                closest_distance = d_i
                index = i
        return index
    def check_stop(self, old_IDs):
        return sum([(x - y) for (x, y) in zip(old_IDs, self._IDs)]) == 0
    def reset_all_clusters(self):
        for cluster in self._clusters:
            cluster.remove_all_points()
    def do_something(self):
        self.reset_all_clusters()
        new_IDs = []
        for p in self._lop:
            index = self.find_closest_cluster(p)
            new_IDs.append(index)
            self._clusters[index].add_a_point(p)
        for i in range(self._k):
            self._clusters[i].update()
        return new_IDs
    def clustering(self):
        old_IDs = [0] * self._k
        while (not self.check_stop(old_IDs)):
            old_IDs = self._IDs
            self._IDs = self.do_something()
    def show(self):
        for cluster in self._clusters:
            print(len(cluster._lop))
            #print(cluster)

def read_data():
    data = dict()
    DATA_DIR = 'data/documents/vectors'
    for fname in os.listdir(DATA_DIR):
        index = int(fname.replace('.vector', ''))
        vector = []
        for line in open(DATA_DIR + '/' + fname):
            if len(line) < 2: continue
            word, val = line.split(' : ')
            val = float(val)
            vector.append([word, val])
        data[index] = Point(vector)
    sorted_by_key = sorted(data.items(), key=lambda kv: kv[0])
    data = [item[1] for item in sorted_by_key]
    return data

def save_data(kmeans):
    DATA_PATH = 'data/documents/clusters/cluster.json'
    IDs = kmeans._IDs
    centers = [cluster._center._vect for cluster in kmeans._clusters]
    data = {"ids" : IDs, "centers" : centers}
    with open(DATA_PATH, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
