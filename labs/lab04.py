from __future__ import annotations

from dsa.array import Array

def make_block(capacity):
    return Array(capacity)

class DynamicArray:

    def __init__(self, values=(), growth=2):
        self._size = 0
        self._capacity = 1
        self._block = make_block(self._capacity)
        self.growth = growth
        #: number of reallocations so far — plot this against n
        self.resize_count = 0
        for value in values:
            self.append(value)

    def _resize(self, capacity):
        new_block = make_block(capacity)
        for i in range(self._size):
            new_block[i] = self._block[i]
        self._block = new_block
        self._capacity = capacity
        self.resize_count += 1

    def append(self, value):
        if self._size == self._capacity:
            self._resize(self._capacity * self.growth)
        self._block[self._size] = value
        self._size += 1

    def __getitem__(self, index):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        return self._block[index]

    def __setitem__(self, index, value):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        self._block[index] = value

    def insert_at(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError(index)
        if self._size == self._capacity:
            self._resize(self._capacity * self.growth)
        for i in range(self._size, index, -1):
            self._block[i] = self._block[i - 1]
        self._block[index] = value
        self._size += 1

    def pop(self, index=-1):
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("pop index out of range")
        value = self._block[index]
        for i in range(index, self._size - 1):
            self._block[i] = self._block[i + 1]
        self._block[self._size - 1] = None
        self._size -= 1
        return value

