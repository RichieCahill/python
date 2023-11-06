# Word Search

# Given an m x n grid of characters board and a string word,
# return true if word exists in the grid.
# You can construct the word by moving between adjacent cells in the grid
# (up, down, left, or right),
# but you may not use the same cell more than once.

# Sample Case

# board:
# [
# [A, B, C, E],
# [A, F, C, S],
# [A, D, E, E]
# ]

# word: "ABCCED"

# Output: true


def solve(matrex, input_string):
    matrex0_len = len(matrex[0])
    matrex_len = len(matrex)

    def funk_thing(i, j, char_index):
        if char_index == len(input_string):
            return 1
        if (
            i >= matrex_len
            or j >= matrex0_len
            or matrex[i][j] != input_string[char_index]
        ):
            return 0
        return any(
            funk_thing(i + x_pos, j + y_pos, char_index + 1)
            for x_pos, y_pos in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        )

    return any(
        funk_thing(i, j, 0) for i in range(matrex_len) for j in range(matrex0_len)
    )


# 305


def solve(matrex, input_string):
    matrex0_len = len(matrex[0])
    matrex_len = len(matrex)

    def funk_thing(i, j, char_index):
        if char_index == len(input_string):
            return 1
        if (
            i >= matrex_len
            or j >= matrex0_len
            or matrex[i][j] != input_string[char_index]
        ):
            return 0
        return any(
            funk_thing(i + x_pos, j + y_pos, char_index + 1)
            for x_pos, y_pos in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        )

    return any(
        funk_thing(i, j, 0) for i in range(matrex_len) for j in range(matrex0_len)
    )


def solve(matrex, input_string):
    matrex0_len = len(matrex[0])
    matrex_len = len(matrex)

    def funk_thing(i, j, char_index):
        if char_index == len(input_string):
            return 1
        if (
            i >= matrex_len
            or j >= matrex0_len
            or matrex[i][j] != input_string[char_index]
        ):
            return 0
        return any(
            funk_thing(i + x_pos, j + y_pos, char_index + 1)
            for x_pos, y_pos in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        )

    return any(
        funk_thing(i, j, 0) for i in range(matrex_len) for j in range(matrex0_len)
    )


def solve(b, w, d=[(1, 0), (-1, 0), (0, 1), (0, -1)]):
    def f(i, j, k):
        if k == len(w):
            return 1
        if not (0 <= i < len(b)) or not (0 <= j < len(b[0])) or b[i][j] != w[k]:
            return 0
        return any(f(i + x, j + y, k + 1) for x, y in d)

    return any(f(i, j, 0) for i in range(len(b)) for j in range(len(b[0])))


# 263


def solve(b, w):
    a, z = len(b), len(b[0])

    def f(i, j, c):
        if c == len(w):
            return 1
        if i >= a or j >= z or b[i][j] != w[c]:
            return 0
        return any(
            f(i + x, j + y, c + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        )

    return any(f(i, j, 0) for i in range(a) for j in range(z))


# 243


def solve(b, w):
    a, z = len(b), len(b[0])

    def f(i, j, c):
        if c == len(w):
            return 1
        if i >= a or j >= z or b[i][j] != w[c]:
            return 0
        return any(
            f(i + x, j + y, c + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        )

    return any(f(i, j, 0) for i in range(a) for j in range(z))


# 243


def solve(m, s):
    x, z = len(m), len(m[0])
    f = (
        lambda i, j, k: 1
        if k == len(s)
        else 0
        if i >= x or j >= z or m[i][j] != s[k]
        else any(f(i + x, j + y, k + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    )
    return any(f(i, j, 0) for i in range(x) for j in range(z))


# 228


def solve(m, s):
    x, z = len(m), len(m[0])
    f = (
        lambda i, j, k: 1
        if k == len(s)
        else 0
        if i >= x or j >= z or m[i][j] != s[k]
        else any(f(i + x, j + y, k + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    )
    return any(f(i, j, 0) for i in range(x) for j in range(z))


def solve2(m, s):
    f = lambda i, j, k: k == len(s) or (
        i >= 0 < j < len(m[0])
        and m[i][j] == s[k]
        and any(f(i + x, j + y, k + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    )
    return any(f(i, j, 0) for i in range(len(m)) for j in range(len(m[0])))


def solve(m, s):
    x, z = len(m), len(m[0])
    f = (
        lambda i, j, k: 1
        if k == len(s)
        else 0
        if i >= x or j >= z or m[i][j] != s[k]
        else any(f(i + x, j + y, k + 1) for x, y in [(1, 0), (-1, 0), (0, 1), (0, -1)])
    )
    return any(f(i, j, 0) for i in range(x) for j in range(z))


def solve(matrex, input_string):
    matrex0_len = len(matrex[0])
    matrex_len = len(matrex)

    def funk_thing(i, j, char_index):
        if char_index == len(input_string):
            return 1
        if (
            i >= matrex_len
            or j >= matrex0_len
            or matrex[i][j] != input_string[char_index]
        ):
            return 0
        test_listr = [0, 0, 1, -1]
        test_listl = [
            1,
            -1,
            0,
            0,
        ]
        return any(
            funk_thing(
                i + test_listr[test_index], j + test_listl[test_index], char_index + 1
            )
            for test_index in range(4)
        )

    return any(
        funk_thing(i, j, 0) for i in range(matrex_len) for j in range(matrex0_len)
    )


# lsit with negtive ingexing
def solve(m, s, r=range):
    x, z, y = len(m), len(m[0]), [0, 0, 1, -1]
    f = (
        lambda i, j, k: 1
        if k == len(s)
        else 0
        if i >= x or j >= z or m[i][j] != s[k]
        else any(f(i + y[p], j + y[p - 2], k + 1) for p in r(4))
    )
    return any(f(i, j, 0) for i in r(x) for j in r(z))


def solve(m, s, r=range):
    x, z, y = len(m), len(m[0]), [0, 0, 1, -1]
    f = (
        lambda i, j, k: 1
        if k == len(s)
        else 0
        if i >= x or j >= z or m[i][j] != s[k]
        else any(f(i + y[p], j + y[p - 2], k + 1) for p in r(4))
    )
    return any(f(i, j, 0) for i in r(x) for j in r(z))


221
