"""Stack — last in, first out.

Deliberately a thin structure: the interesting part is what you *do* with it
(balanced brackets, infix to postfix, undo history, DFS without recursion).

Built on your own `DynamicArray` (Week 4): the top of the stack is the END of
the array, where append and pop are O(1). Put the top at index 0 instead and
every push shifts the whole stack — try it, and measure it.
"""

from __future__ import annotations

from dsa.dynamic_array import DynamicArray


class Stack:
    """LIFO. Every operation should be O(1)."""

    def __init__(self, values=()):
        self._items = DynamicArray()
        for value in values:
            self.push(value)

    def push(self, value):
        """Add to the top. Target: O(1) amortised."""
        self._items.append(value)

    def pop(self):
        """Remove and return the top. Target: O(1). Raises IndexError when empty."""
        if self.is_empty():
            raise IndexError("pop from empty Stack")
        # pop() with no argument removes the last element: nothing shifts
        return self._items.pop()

    def peek(self):
        """Return the top without removing it. Raises IndexError when empty."""
        if self.is_empty():
            raise IndexError("peek from empty Stack")
        # read the last used slot, but do NOT remove it
        return self._items[len(self._items) - 1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        if not len(self._items):
            return "Stack([])"
        return f"Stack({list(self._items)!r})  # top = {self._items[len(self._items) - 1]!r}"


# -- challenges -----------------------------------------------------------


def is_balanced(text):
    """True when every bracket in `text` is closed in the right order.

    "(a[b]{c})" -> True ;  "(a[b)]" -> False ;  "(" -> False

    The canonical first use of a stack. Target: O(n).
    """
    partner = {")": "(", "]": "[", "}": "{"}
    opens = Stack()
    for ch in text:
        if ch in "([{":
            opens.push(ch)
        elif ch in ")]}":
            # check 1: a closer with nothing open to match
            if opens.is_empty():
                return False
            # check 2: the closer must match the most recent opener
            if opens.pop() != partner[ch]:
                return False
    # check 3: nothing may be left open at the end
    return opens.is_empty()



def infix_to_postfix(tokens):
    """Shunting-yard: ["3","+","4","*","2"] -> ["3","4","2","*","+"].

    Target: O(n). Handles + - * / and parentheses.
    """
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []                      # the result: a plain list is fine here
    operators = Stack()              # the waiting siding: our own Stack

    for token in tokens:
        if token in precedence:
            # pop every operator of HIGHER OR EQUAL precedence, stopping at "("
            while (not operators.is_empty()
                   and operators.peek() != "("
                   and precedence[operators.peek()] >= precedence[token]):
                output.append(operators.pop())
            operators.push(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            # pop to the output until we reach the matching "("
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("unmatched ')'")
            operators.pop()          # throw the "(" away
        else:
            output.append(token)     # a number goes straight through

    # end of input: everything still waiting leaves
    while not operators.is_empty():
        top = operators.pop()
        if top == "(":
            raise ValueError("unmatched '('")
        output.append(top)
    return output