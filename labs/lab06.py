class Stack:
    """LIFO stack. The top is the END of self._items (O(1) push/pop)."""

    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

    def is_empty(self):
        return len(self._items) == 0

    def push(self, value):
        self._items.append(value)           

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()          

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[len(self._items) - 1] 


_PAIRS = {")": "(", "]": "[", "}": "{"}
_OPENERS = set(_PAIRS.values())


def is_balanced(text):
    stack = Stack()
    for ch in text:
        if ch in _OPENERS:
            stack.push(ch)
        elif ch in _PAIRS:
            if stack.is_empty():            
                return False
            if stack.pop() != _PAIRS[ch]:  
                return False
    return stack.is_empty()             


def _to_number(token):
    if isinstance(token, (int, float)):
        return token
    try:
        return int(token)
    except (ValueError, TypeError):
        try:
            return float(token)
        except (ValueError, TypeError):
            raise ValueError(f"invalid operand: {token!r}")


_OPS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,             
}


def evaluate_postfix(tokens):
    stack = Stack()
    for tok in tokens:
        if isinstance(tok, str) and tok in _OPS:
            if len(stack) < 2:
                raise ValueError("malformed postfix expression")
            right = stack.pop()            
            left = stack.pop()
            stack.push(_OPS[tok](left, right))
        else:
            stack.push(_to_number(tok))
    if len(stack) != 1:                    
        raise ValueError("malformed postfix expression")
    return stack.pop()


_PREC = {"+": 1, "-": 1, "*": 2, "/": 2}


def infix_to_postfix(tokens):
    out = []
    ops = Stack()
    for tok in tokens:
        if tok == "(":
            ops.push(tok)
        elif tok == ")":
            while not ops.is_empty() and ops.peek() != "(":
                out.append(ops.pop())
            if ops.is_empty():
                raise ValueError("mismatched parentheses")
            ops.pop()                      
        elif tok in _PREC:
            
            while (not ops.is_empty() and ops.peek() != "("
                   and _PREC[ops.peek()] >= _PREC[tok]):
                out.append(ops.pop())
            ops.push(tok)
        else:
            out.append(tok)
    while not ops.is_empty():              
        top = ops.pop()
        if top == "(":
            raise ValueError("mismatched parentheses")
        out.append(top)
    return out