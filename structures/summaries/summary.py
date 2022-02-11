"""
Class representation of tuple (value_i, gap_i, delta_i), where
    gap_i = r_min(value_i) - r_min(value_i-1)
    delta_i = r_max(value_i) - r_min(value_i)
"""
from __future__ import annotations

class Summary():
    def __init__(self, point, delta):
        """Class constructor

        :param point: value
        :param delta: starting delta
        """
        self.value = point
        self.gap = 1
        self.delta = delta

    def __repr__(self) -> str:
        """Summary in readable format

        :return: string representation
        """
        return f"({self.value}, {self.gap}, {self.delta})"

    def __lt__(self, other: Summary) -> bool:
        """Less-than method for comparison

        :param other: instance to compare
        """
        return self.value < other.value