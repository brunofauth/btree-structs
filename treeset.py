#-------------------------------------------------------------------------------
# treeset.py
#
#
# Copyright (C) 2016, Ryosuke Fukatani
# License: Apache 2.0
#-------------------------------------------------------------------------------

from __future__ import annotations

import bisect
from typing import Iterable, Iterator, TypeVar, Callable


T = TypeVar("T")


class TreeSet(object):
    """
    Binary-tree set like java Treeset.
    Duplicate elements will not be added.
    When added new element, TreeSet will be sorted automatically.
    """
    def __init__(
        self,
        elements: Iterable[T],
        key: Callable[[T], int],
    ) -> None:
        self._treeset = list(set(elements))
        self._treeset.sort(key=key)
        self._key_func = key

    def addAll(self, elements: Iterable[T]) -> None:
        for element in elements:
            self.add(element)

    def add(self, element: T) -> None:
        if element not in self:
            bisect.insort(self._treeset, element, key=self._key_func)

    def ceiling(self, e):
        index = bisect.bisect_right(self._treeset, e)
        if self[index - 1] == e:
            return e
        return self._treeset[bisect.bisect_right(self._treeset, e)]

    def floor(self, e):
        index = bisect.bisect_left(self._treeset, e)
        if self[index] == e:
            return e
        else:
            return self._treeset[bisect.bisect_left(self._treeset, e) - 1]

    def __getitem__(self, num):
        return self._treeset[num]

    def __len__(self):
        return len(self._treeset)

    def clear(self):
        """Delete all elements in TreeSet."""
        self._treeset = []

    def clone(self):
        """
        Return shallow copy of self.
        """
        return TreeSet(self._treeset)

    def remove(self, element):
        """
        Remove element if element in TreeSet.
        """
        # This should use bisect to find the element's index and then __delitem__
        try:
            self._treeset.remove(element)
        except ValueError:
            return False
        return True

    def __iter__(self) -> Iterator[T]:
        """
        Do ascending iteration for TreeSet
        """
        yield from self._treeset

    def pop(self, index):
        return self._treeset.pop(index)

    def __repr__(self) -> str:
        return f"{{{', '.join(self._treeset)}}}"

    def __eq__(self, target: TreeSet) -> bool:
        if not isinstance(target, TreeSet):
            return NotImplemented
        return self._treeset == target._treeset

    def __contains__(self, e):
        """
        Fast attribution judgment by bisect
        """
        try:
            return e == self._treeset[bisect.bisect_left(self._treeset, e)]
        except:
            return False

if __name__ == '__main__':
    ts = TreeSet([3,7,7,1,3])
    print(ts.floor(4))
    print(ts.ceiling(4))
    print(ts.floor(3))
    print(ts.ceiling(3))
    print(ts)
