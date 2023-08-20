#-------------------------------------------------------------------------------
# treeset.py
#
#
# Copyright (C) 2016, Ryosuke Fukatani
# License: Apache 2.0
#-------------------------------------------------------------------------------

from __future__ import annotations

import bisect
from typing import Iterable, Iterator, TypeVar, Callable, Generic


T = TypeVar("T")


class TreeSet(Generic[T]):
    """
    Binary-tree set, like java's Treeset.
    Duplicate elements will not be added.
    Ordering is kept after adding/removing elements.
    """

    @classmethod
    def from_iter(
        cls,
        iterable: Iterable[T],
        *,
        key: Callable[[T], int] | None = None,
    ) -> TreeSet[T]:
        return TreeSet(*iterable, key=key)

    def __init__(
        self,
        *elements: Iterable[T],
        key: Callable[[T], int] | None = None,
    ) -> None:
        self._treeset = list(set(elements))
        self._treeset.sort(key=key)
        self._key_func = key

    def extend(self, other: Iterable[T]) -> None:
        self._treeset.extend(other)
        self._treeset.sort(key=self._key_func)

    def add_from_iter(self, elements: Iterable[T]) -> None:
        for element in elements:
            self.add(element)

    def add(self, element: T) -> None:
        if element not in self:
            bisect.insort(self._treeset, element, key=self._key_func)

    def clear(self) -> None:
        """Delete all elements in TreeSet."""
        self._treeset = []

    def clone(self) -> TreeSet[T]:
        """Return shallow copy of self."""
        return TreeSet(self._treeset)

    def remove(self, element: T) -> None:
        """Remove element if element in TreeSet."""
        index = bisect.bisect_right(self._treeset, element, key=self._key_func)
        if len(self) > 0 and self._treeset[index] == element:
            del self._treeset[index]

    def __getitem__(self, num: int) -> T:
        return self._treeset[num]
    
    def __delitem__(self, index: int) -> None:
        del self._treeset[index]

    def __len__(self) -> int:
        return len(self._treeset)

    def __iter__(self) -> Iterator[T]:
        """Do ascending iteration for TreeSet"""
        yield from self._treeset

    def pop(self, index: int) -> T:
        return self._treeset.pop(index)

    def __repr__(self) -> str:
        return f"{{{', '.join(self._treeset)}}}"

    def __eq__(self, target: TreeSet) -> bool:
        if not isinstance(target, TreeSet):
            return NotImplemented
        return self._treeset == target._treeset

    def __contains__(self, e: T) -> bool:
        """Fast attribution judgment by bisect"""
        try:
            return e == self._treeset[bisect.bisect_left(self._treeset, e, key=self._key_func)]
        except:
            return False


if __name__ == '__main__':
    ts = TreeSet([3,7,7,1,3])
    print(ts.floor(4))
    print(ts.ceiling(4))
    print(ts.floor(3))
    print(ts.ceiling(3))
    print(ts)

