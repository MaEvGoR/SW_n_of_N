import numpy as np
from typing import List

class NumpyQuantile():

    def __init__(self, n: int):
        self.points: List = []
        self.n = n
        print('Init Numpy Quantile System.')

    def add(self, point, *args, **kwargs):
        self.points.append(point)

    def query(self, q: float, last_n: False):
        if last_n:
            return np.quantile(self.points[-self.n:], q)
        else:
            return np.quantile(self.points, q)
