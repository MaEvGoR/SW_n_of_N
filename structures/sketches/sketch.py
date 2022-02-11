"""
Sketch that contains information about Summaries in batch
Actually, this is another GK implementation, but more or less
connected with other classes
"""

from structures.summaries.summary import Summary
from structures.summaries.summary_nn import SummaryNn
import bisect
from typing import List
import numpy as np

class Sketch():
    def __init__(
        self,
        epsilon: float
    ) -> None:
        """Class constructor

        :param epsilon: possible rank error
        """
        self.summaries: List[Summary] = []
        self.epsilon = epsilon

    def add(
        self,
        point,
        nb: int
    ) -> None:
        """Create summary out of point and put it in right order

        :param point: data point
        :param nb: number of seen points in bucket
        """
        delta = 2 * self.epsilon * nb
        new_summary = Summary(point, delta)

        # find place for new summary in ordered list 
        insert_index = bisect.bisect_right(
            self.summaries,
            new_summary
        )

        if insert_index == 0 or insert_index == self.len:
            new_summary.delta = 0

        self.summaries.insert(insert_index, new_summary)

    def len(self) -> int:
        """Number of summaries in sketch

        :return: length of summaries
        """
        return len(self.summaries)

    def compress(self, nb) -> None:
        """Merge summaries together

        :param nb: number of seen points in bucket
        """
        for i in range(self.len() - 2, 1, -1):
            while (i < self.len() - 1):
                status = self.delete_if_needed(i, nb)
                if not status:
                    break

    def delete_if_needed(self, index, nb) -> bool:
        """Merge two summaries together

        :param i: index of left summary
        :param nb: number of seeen points
        :return: if was merged or not
        """
        left = self.summaries[index]
        right = self.summaries[index + 1]
        if left.delta >= right.delta and left.gap + right.delta < 2 * self.epsilon * nb:
            self.summaries.pop(index)
            right.gap += left.gap
            return True

        return False

    def get_rmin_rmax(
        self
    ) -> List[SummaryNn]:
        """Reconstruct the summaries
        to get rank limit for data points

        :return: restructured summaries
        """
        assert len(self.summaries) != 0, 'No elements in sketch'

        summaries: List[SummaryNn] = []

        v0 = self.summaries[0].value
        rmin0 = 1
        rmax0 = self.summaries[0].gap + rmin0

        first = SummaryNn(
            point=v0,
            rmin=rmin0,
            rmax=rmax0
        )
        summaries.append(first)
        for i in range(1, len(self.summaries)):
            v = self.summaries[i].value
            rmin = summaries[i-1].rmin + self.summaries[i].gap
            rmax = self.summaries[i].delta + rmin

            new_summary = SummaryNn(
                point=v,
                rmin=rmin,
                rmax=rmax
            )

            summaries.append(new_summary)

        return summaries
    
    def lift(
        self,
        ksi: float,
        n: int
    ) -> List[SummaryNn]:
        """Apply LIFT to sketch 

        :param ksi: quantile value
        :param n: numbre of points to observe
        :return: LIFTed summaries in rmin - rmax format
        """
        assert 0 < ksi <= 1, f'Quantile value should be between (0, 1]. Got {ksi}'

        rmin_rmax = self.get_rmin_rmax()
        for summary in rmin_rmax:
            summary.rmax += np.floor(ksi * n / 2)

        return rmin_rmax

    def __repr__(self) -> str:
        """Readable format for sketch

        :return: string representation
        """
        out = ""
        for s in self.summaries:
            out += str(s) + ", "

        return out