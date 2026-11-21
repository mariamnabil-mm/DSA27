"""Dynamic programming.

The teaching arc for each problem is the same three steps, and it is worth
making students walk all three every time:

  1. **naive recursion** — obviously correct, exponentially slow
  2. **memoised** (top-down) — same code, a cache, suddenly polynomial
  3. **tabulated** (bottom-up) — the recursion turned inside out, O(1) space
     where the recurrence allows it

`fib_naive` versus `fib_memo` through `viz.complexity.measure` is the most
convincing thirty seconds in the whole course — just keep n small for the
naive one.
"""

from __future__ import annotations

__all__ = [
    "fib_naive", "fib_memo", "fib_table",
    "grid_paths", "coin_change", "longest_common_subsequence",
    "edit_distance", "knapsack_01", "longest_increasing_subsequence",
]


# -- the three forms, on one problem --------------------------------------


def fib_naive(n):
    """Fibonacci by direct recursion. O(phi^n) — exponential.

    Count the calls. F(30) is roughly 2.7 million, and almost all of them
    recompute something already known.
    """
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)


def fib_memo(n, cache=None):
    """Same recursion, results cached. O(n) time, O(n) space."""
    if cache is None:
        cache = {}
    if n < 2:
        return n
    if n in cache:
        return cache[n]
    cache[n] = fib_memo(n - 1, cache) + fib_memo(n - 2, cache)
    return cache[n]


def fib_table(n):
    """Bottom-up. O(n) time, O(1) space — only the last two values matter."""
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(2, n + 1):
        previous, current = current, previous + current
    return current


# -- classic problems ------------------------------------------------------


def grid_paths(rows, cols, blocked=()):
    """Count paths from top-left to bottom-right moving only right or down.

    O(rows * cols). The DP table is literally the grid, so
    `viz.draw.draw_array` on each row shows it filling in.
    """
    if rows <= 0 or cols <= 0:
        return 0
    blocked = {tuple(cell) for cell in blocked}
    table = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if (r, c) in blocked:
                table[r][c] = 0
            elif r == 0 and c == 0:
                table[r][c] = 1
            else:
                from_above = table[r - 1][c] if r > 0 else 0
                from_left = table[r][c - 1] if c > 0 else 0
                table[r][c] = from_above + from_left
    return table[rows - 1][cols - 1]


def coin_change(coins, amount):
    """Fewest coins summing to `amount`, or -1 if impossible. O(amount * len(coins)).

    Challenge: return the actual coins, not just the count. That means storing
    a choice alongside each cell and walking it back — the same reconstruction
    idea every DP problem needs.
    """
    INF = float("inf")
    table = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a and table[a - coin] + 1 < table[a]:
                table[a] = table[a - coin] + 1
    return table[amount] if table[amount] != INF else -1


def longest_common_subsequence(a, b):
    """Length of the LCS of two sequences. O(len(a) * len(b)).

    Challenge: return the subsequence itself by backtracking through the table.
    """
    n, m = len(a), len(b)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table[n][m]


def edit_distance(a, b):
    """Minimum insert/delete/replace operations turning `a` into `b`.

    O(len(a) * len(b)). This is what spell checkers and `diff` are built on.
    """
    n, m = len(a), len(b)
    table = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        table[i][0] = i
    for j in range(m + 1):
        table[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                table[i][j] = table[i - 1][j - 1]
            else:
                table[i][j] = 1 + min(
                    table[i - 1][j],
                    table[i][j - 1],
                    table[i - 1][j - 1],
                )
    return table[n][m]


def knapsack_01(weights, values, capacity):
    """Maximum value within `capacity`, each item taken at most once.

    O(len(items) * capacity) — "pseudo-polynomial", because it is linear in
    the *value* of capacity, not in the number of bits used to write it. A
    genuinely useful distinction to raise here.
    """
    table = [0] * (capacity + 1)
    for weight, value in zip(weights, values):
        for c in range(capacity, weight - 1, -1):
            table[c] = max(table[c], table[c - weight] + value)
    return table[capacity]


def longest_increasing_subsequence(values):
    """Length of the longest strictly increasing subsequence.

    O(n^2) with the obvious DP. Challenge: O(n log n) using `lower_bound` from
    `dsa.searching` — a satisfying payoff for having written it earlier.
    """
    if not values:
        return 0
    best = [1] * len(values)
    for i in range(len(values)):
        for j in range(i):
            if values[j] < values[i]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)
