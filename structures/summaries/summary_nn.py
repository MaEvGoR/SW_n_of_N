"""
Class representation of tuple (value_i, r_min, r_max)
"""
from __future__ import annotations

class SummaryNn():
    def __init__(self, point, rmin, rmax):
        """Class constructor

        :param point: data value
        :param rmin: minimal rank
        :param rmax: maximum rank
        """
        self.value = point
        self.rmin = rmin
        self.rmax = rmax

    def __repr__(self) -> str:
        """SummaryNn in readable format

        :return: string representation
        """
        return f"({self.value}, {self.rmin}, {self.rmax})"

    def __lt__(self, other):
        """Less-than method for comparison

        :param other: instance to compare
        """
        return self.value < other.value