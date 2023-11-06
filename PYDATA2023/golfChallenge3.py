# Partition Array

# You're given an array with 2n elements.
# You want to split the array into n pairs of elements.
# etc (a1, b1), (a2, b2), (a3, b3), ..., (an, bn)
# You want to take the minimum number from each pair and add them up, trying to make this sum as large as possible.
# Write a function that returns the maximum sum you can get when partitioning the given array into pairs and adding up the minimums.

# Sample Case

# Input: nums: [1, 4, 3, 2]
# Output: 4

# You can group this list into the pairs (1, 2), (4, 3), so when you add the minimums you get 1+3=4.


def solve_ungolfed(input_list: list[int]) -> int:
    """Given a list of integers, return the sum of the minimums of each pair.
solve=lambda n:sum(sorted(n)[::2])
    Args:
        input_list (list[int]): list of integers

    Returns:
        int: sum of the minimums of each pair
    """
    sorted_list = sorted(input_list)
    # grab every other element
    odds_list = sorted_list[::2]
    return sum(odds_list)


print(solve_ungolfed([1, 4, 3, 2, 5, 6, 7, 8, 9, 10]))

# fmt: off Golfed version

def solve(n):return sum(sorted(n)[::2])

solve=lambda n:sum(sorted(n)[::2])

print(solve([1, 4, 3, 2, 5, 6, 7, 8, 9, 10]))

