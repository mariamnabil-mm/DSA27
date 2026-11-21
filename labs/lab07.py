class SlowQueue:
    """List-backed queue. dequeue is O(n) on purpose (pop(0) shifts everything)."""

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def enqueue(self, value):
        self._items.append(value)         

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")   
        return self._items.pop(0)          

class CircularQueue:
    """Fixed-block ring buffer. enqueue/dequeue are O(1).

    _tail is the slot where the NEXT value will be written, so
    "full" is tested with _size == capacity (tail == head is ambiguous).
    With grow=True the block doubles when full (the challenge); otherwise
    enqueue on a full queue raises IndexError.
    """

    def __init__(self, capacity=4, grow=False):
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._block = [None] * capacity
        self._capacity = capacity
        self._head = 0
        self._tail = 0
        self._size = 0
        self._grow = grow

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self._capacity

    def _resize(self, new_capacity):
        new_block = [None] * new_capacity
        for i in range(self._size):         
            new_block[i] = self._block[(self._head + i) % self._capacity]
        self._block = new_block
        self._capacity = new_capacity
        self._head = 0                    
        self._tail = self._size            

    def enqueue(self, value):
        if self.is_full():
            if not self._grow:
                raise IndexError("enqueue on full queue")
            self._resize(2 * self._capacity)
        self._block[self._tail] = value
        self._tail = (self._tail + 1) % self._capacity   
        self._size += 1                                   

    def dequeue(self):
        if self._size == 0:
            raise IndexError("dequeue from empty queue")
        value = self._block[self._head]                  
        self._block[self._head] = None
        self._head = (self._head + 1) % self._capacity   
        self._size -= 1
        return value