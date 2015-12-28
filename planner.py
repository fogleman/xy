from math import hypot
import anneal
import random

class OrderModel(object):
    def __init__(self, paths):
        self.paths = paths
    def energy(self):
        result = 0
        for i in xrange(len(self.paths) - 1):
            a = self.paths[i]
            b = self.paths[i + 1]
            x1, y1 = a[-1]
            x2, y2 = b[0]
            result += hypot(x2 - x1, y2 - y1)
        return result
    def do_move(self):
        n = len(self.paths) - 1
        i = random.randint(0, n)
        j = random.randint(0, n)
        self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
        return (i, j)
    def undo_move(self, undo):
        i, j = undo
        self.paths[i], self.paths[j] = self.paths[j], self.paths[i]
    def copy(self):
        return OrderModel(list(self.paths))

def order_paths(paths):
    state = OrderModel(paths)
    print state.energy()
    max_temp = anneal.get_max_temp(state, 10000)
    print max_temp
    state = anneal.anneal(state, max_temp, 1, 100000)
    print state.energy()
    return state.paths
