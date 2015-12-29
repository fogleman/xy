from math import hypot
import anneal
import random

def order_paths(paths, iterations=100000, verbose=False):
    '''
    This function re-orders a set of 2D paths (polylines) to minimize the
    distance required to visit each path. This is useful for 2D plotting to
    reduce wasted movements where the instrument is not drawing.

    The code uses simulated annealing as its optimization algorithm. The number
    of iterations can be increased to improve the chances of finding a perfect
    solution. However, a perfect solution isn't necessarily required - we just
    want to find something good enough.

    With randomly generated paths, the algorithm can quickly find a solution
    that reduces the extra distance to 25 percent of its original value.
    '''
    state = Model(paths)
    before = state.energy()
    max_temp = anneal.get_max_temp(state, 10000)
    min_temp = max_temp / 1000.0
    state = anneal.anneal(state, max_temp, min_temp, iterations)
    after = state.energy()
    pct = 100.0 * after / before
    if verbose:
        print 'original distance : %g' % before
        print 'improved distance : %g (%.1f%% of original)' % (after, pct)
    return state.paths

# the algorithm cannot work with floating point distances due to optimizations
# this factor is used to scale up floats to workable integers
FACTOR = 1000000

class Model(object):
    def __init__(self, paths, distances=None, total_distance=None):
        self.paths = paths
        self.total_distance = total_distance or 0
        if distances:
            self.distances = distances
        else:
            self.distances = [0] * (len(paths) - 1)
            self.add_distances(range(len(self.distances)))
    def subtract_distances(self, indexes):
        n = len(self.distances)
        for i in indexes:
            if i >= 0 and i < n:
                self.total_distance -= self.distances[i]
    def add_distances(self, indexes):
        n = len(self.distances)
        for i in indexes:
            if i >= 0 and i < n:
                x1, y1 = self.paths[i][-1]
                x2, y2 = self.paths[i + 1][0]
                self.distances[i] = int(hypot(x2 - x1, y2 - y1) * FACTOR)
                self.total_distance += self.distances[i]
    def energy(self):
        # return the total extra distance for this ordering
        return float(self.total_distance) / FACTOR
    def do_move(self):
        # mutate the state by swapping two random paths
        n = len(self.paths) - 1
        i = random.randint(0, n)
        j = random.randint(0, n)
        indexes = set([i - 1, i, j - 1, j])
        self.subtract_distances(indexes)
        self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
        self.add_distances(indexes)
        return (i, j)
    def undo_move(self, undo):
        # undo the previous mutation
        i, j = undo
        indexes = set([i - 1, i, j - 1, j])
        self.subtract_distances(indexes)
        self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
        self.add_distances(indexes)
    def copy(self):
        # make a copy of the model
        return Model(
            list(self.paths), list(self.distances), self.total_distance)

if __name__ == '__main__':
    # test the module
    random.seed(123)
    paths = []
    for _ in range(100):
        x1 = random.random()
        y1 = random.random()
        x2 = random.random()
        y2 = random.random()
        path = [(x1, y1), (x2, y2)]
        paths.append(path)
    order_paths(paths, verbose=True)
