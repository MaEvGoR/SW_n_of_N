"""
Greenwald-Khanna quantile estimator
Implementation is taken from the link below for test purposes
https://aakinshin.net/posts/greenwald-khanna-quantile-estimator/#post-title
"""
import numpy as np
from typing import List
from structures.summaries.summary import Summary
import bisect

class GK():
    def __init__(self, epsilon):
        self.epsilon = epsilon
        self.compressing_interval = np.floor(1 / (2 * epsilon))
        self.summaries: List[Summary] = []
        self.n = 0
        print('Init GK system.')
        print(f'\tepsilon: {self.epsilon} (rank error coefficient)')
        print(f'\tcompressing_interval: {self.compressing_interval} (limit for storing)')

    def add(self, point, *args, **kwargs):

        delta = 2 * self.epsilon * self.n
        new_summary = Summary(point, delta)
        
        insert_index = bisect.bisect_right(
            self.summaries,
            new_summary
        )

        if insert_index == 0 or insert_index == len(self.summaries):
            new_summary.delta = 0
        
        self.summaries.insert(insert_index, new_summary)
        self.n += 1

        if self.n % self.compressing_interval == 0:
            self.compress()
    
    def _compress(self):
        for i in range(len(self.summaries) - 2, 1, -1):
            while (i < len(self.summaries) - 1 and self.delete_if_needed(i)):
                pass
    
    def _delete_if_needed(self, i):
        s1 = self.summaries[i]
        s2 = self.summaries[i + 1]
        if s1.delta >= s2.delta and s1.gap + s2.delta < 2 * self.epsilon * self.n:
            self.summaries.pop(i)
            s2.gap += s1.gap
            return True
        return False

    def query(self, q: float, *args, **kargs):
        assert len(self.summaries) != 0, 'No elements'

        rank = q * (self.n - 1) + 1
        margin = np.ceil(self.epsilon * self.n)

        best_index = -1
        best_dist = float('inf')
        rmin = 0
        for i in range(len(self.summaries)):
            summary = self.summaries[i]
            rmin += summary.gap
            rmax = rmin + summary.delta
            if rank - margin <= rmin and rmax <= rank + margin:
                current_dist = abs(rank - (rmin + rmax) / 2)
                if current_dist < best_dist:
                    best_dist = current_dist
                    best_index = i
        
        assert best_index != -1

        return self.summaries[best_index].value

