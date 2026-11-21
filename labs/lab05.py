from __future__ import annotations


class Node:

    __slots__ = ("value", "next")

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

    def __repr__(self):
        return f"Node({self.value!r})"


class LinkedList:

    def __init__(self, values=()):
        self.head: Node | None = None
        self._size = 0
        for value in values:
            self.append(value)

    def push_front(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, value):
        node = Node(value)
        if self._head is None:
            self._head = node
        else:
            current = self._head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def find(self, value):
        current = self._head
        index = 0
        while current is not None:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def __getitem__(self, index):
        if not 0 <= index < self._size:
            raise IndexError("index out of range")
        current = self._head
        for _ in range(index):
            current = current.next
        return current.value

    def insert_at(self, index, value):
        if not 0 <= index <= self._size:
            raise IndexError("index out of range")
        if index == 0:
            self.push_front(value)
            return
        previous = self._head
        for _ in range(index - 1):
            previous = previous.next
        node = Node(value)
        node.next = previous.next
        previous.next = node
        self._size += 1

    def pop_front(self):
        if self._head is None:
            raise IndexError("pop from empty list")
        value = self._head.value
        self._head = self._head.next
        self._size -= 1
        return value

    def remove(self, value):
        previous = None
        current = self._head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self._head = current.next
                else:
                    previous.next = current.next
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def reverse(self):
        previous = None
        current = self._head
        while current is not None:
            next_node = current.next
            current.next = previous
            previous = current
            current = next_node
        self._head = previous