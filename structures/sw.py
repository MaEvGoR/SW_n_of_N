"""
Implementation of SW n-of-N alorithm from 
'Continuously Maintaining Quantile Summaries of the Most Recent N Elements over a Data Stream'
https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.72.6192&rep=rep1&type=pdf
"""

import time
from collections import defaultdict
from structures.buckets.bucket import Bucket
from typing import List, Dict
import numpy as np
from structures.summaries.summary_nn import SummaryNn


class SW_n_of_N():

    def __init__(
        self,
        n: int,
        epsilon: float
    ):
        """Class constructor

        :param n: number of most recent points that will be considered for quantile query
        :param epsilon: approximate coefficient
        """
        self._n = n
        self._epsilon = epsilon
        self._lambda = self._epsilon / (self._epsilon + 2)
        self._buckets: Dict[List[Bucket]] = defaultdict(list)

        print('Init SW n-of-N system.')
        print(f'\tepsilon: {self._epsilon} (rank error coefficient)')
        print(f'\tlambda: {self._lambda} (bucket limit at i-th level)')
        print(f'\tn: {self._n} (number of last desired points)')

    def add(self, point, ts: float = time.time()):
        """Add new data point

        :param point: data point, should be Comparable
        :param ts: point recieve timestamp
        """
        # Step 1: create a new sketch
        self._create_new_sketch(ts)

        # Step 2: drop sketches
        self._drop_sketches()

        # Step 3: maintain sketches
        self._maintain_sketches(point)

    def _create_new_sketch(self, ts: float):
        """Record a new 1-bucket, its timestamp ts, and number of data = 0.
        Initialize a sketch S

        :param ts: point timestamp
        """
        new_bucket = Bucket(ts, self._epsilon)
        self._buckets[1].append(new_bucket)

    def _drop_sketches(self):
        """Remove expired and filled buckets
        """
        # If the number of 1-buckets is full (i.e., ⌈ 1/λ ⌉ + 2)
        if len(self._buckets[1]) < (np.ceil(1 / self._lambda) + 2):
            return None

        # iteratively from i = 1 till j
        for i in range(len(self._buckets)):
            level = 2 ** i
            # where the current number (before this new element arrives) of j-buckets is not greater than ⌈ 1/λ ⌉
            if len(self._buckets[level]) != np.ceil(1/self._lambda) + 2:
                # no enough buckets to merge
                continue

            # get the two oldest buckets b1 and b2 among the i-buckets
            # drop b1 and b2 from the i-th bucket list
            b1 = self._buckets[level].pop(0)
            b2 = self._buckets[level].pop(0)

            # add b1 together with its time stamp into (i+1) - buckets list
            self._buckets[2 ** (i + 1)].append(b1)

        # Scan the sketch list from oldest to delete the expired buckets b - (Sb, Nb, tb); that is Nb ≥ N.
        for i in range(len(self._buckets), 0, -1):
            level = 2 ** (i - 1)
            new_buckets = []
            for bucket in self._buckets[level]:
                # choose only not expired buckets
                if bucket.Nb < self._n:
                    new_buckets.append(bucket)
            # delete expired buckets
            self._buckets[level] = new_buckets

    def _maintain_sketches(self, point):
        """Add point to every sketch

        :param point: data point
        """
        # for each remaining sketch Sb
        for i in range(len(self._buckets)):
            level = 2 ** i
            for bucket in self._buckets[level]:
                # add e into Sb by GK-algorithm for epsilon/2 - approximation and Nb := Nb + 1
                bucket.add(point)

    def query(self, q: float, *args, **kwargs):
        """Retrieve φ-quantile

        :param q: φ-quantile
        :raises Exception: If 'q' not in (0, 1]
        :return: calculated value
        """
        if q <= 0 or q > 1:
            raise Exception(
                f'Quantile fraction should be in (0, 1]. Got {q}.'
            )

        # For a given n (n ≤ N), scan the sketch list 
        # from oldest and find the first sketch such that Nb ≤ n
        queried_bucket: Bucket = None
        for i in range(len(self._buckets), 0, -1):
            level = 2 ** (i - 1)
            for bucket in self._buckets[level]:
                if bucket.Nb <= self._n:
                    queried_bucket = bucket
                    break
            if queried_bucket is not None:
                break
        
        # Apply the algorithm Lift to Sb to generate S_lift where ζ = ǫ
        lifted: List[SummaryNn] = queried_bucket.lift()

        # For a given rank 'r', find the first tuple (v, r+, r−) 
        # in S_lift such that r − ǫn ≤ r− ≤ r+ ≤ r + ǫn
        rank = q * self._n
        err = self._epsilon * self._n
        for summary in lifted:
            if rank - err <= summary.rmin <= summary.rmax <= rank + err:
                return summary.value
        
        raise Exception('smth is not good')

    def __str__(self) -> str:
        """Return SW buckets in readable format

        :return: string representation
        """
        repr = ""
        for i in range(len(self._buckets)):
            level = 2 ** i
            repr += f"level {level}: {self._buckets[level]}"
            repr += '\n'

        return repr