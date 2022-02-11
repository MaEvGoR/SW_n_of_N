"""
Bucket implementation
"""
from structures.sketches.sketch import Sketch
from structures.summaries.summary_nn import SummaryNn
from typing import List
import numpy as np


class Bucket():
    def __init__(
        self,
        ts: float,
        epsilon: float
    ) -> None:
        """Class constructor

        :param ts: record timestamp
        :param epsilon: possible approximation error
        """
        self.Nb = 0
        self.timestamp = ts
        self.epsilon = epsilon
        # preserve epsilon/2 approximate
        self.sketch = Sketch(self.epsilon/2)
        self.compressing_interval = np.floor(1/(self.epsilon))

    def add(self, point) -> None:
        """Add new point to bucket

        :param point: data value
        """
        self.sketch.add(point, self.Nb)
        self.Nb += 1

        if self.Nb % self.compressing_interval == 0:
            self.sketch.compress(self.Nb)

    def lift(self) -> List[SummaryNn]:
        """Apply LIFT algorithm to sketch

        :return: LIFTed sketch
        """
        return self.sketch.lift(self.epsilon, self.Nb)

    def __repr__(self) -> str:
        """Readable format for Bucket

        :return: string representation
        """
        return f"T: {self.timestamp}, Nb: {self.Nb}, sketch: {self.sketch}"
