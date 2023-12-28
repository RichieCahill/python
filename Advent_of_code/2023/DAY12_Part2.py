"""DAY12_Part1"""

from functools import cache
from pathlib import Path


@cache
def make_new_groups(groups: tuple[int]) -> tuple[int]:
    """Make new groups by subtracting 1 from the first element and keeping the rest unchanged.

    Args:
        groups (tuple[int]): A tuple representing the groups.

    Returns:
        tuple[int]: A new tuple with the first element decremented by 1 and the rest unchanged.
    """
    end = groups[1::]
    first = groups[0] - 1
    return (first, *end)


def hash_char_logic(group_item_0: int, next_str: str, new_groups: tuple[int]) -> int:
    """Logic for the hash character.

    Args:
        group_item_0 (int): The first element of the groups tuple.
        next_str (str): The next string of conditions.
        new_groups (tuple[int]): The new groups.

    Returns:
        int: The number of groups.
    """
    if group_item_0 == 0:
        return 0
    return get_num_groups_damaged(conditions=next_str, groups=new_groups)


@cache
def get_num_groups_undamaged(conditions: str, groups: tuple[int]) -> int:
    if not groups or groups == (0,):
        return int("#" not in conditions)

    if not conditions:
        return 0

    cond_char = conditions[0]
    next_str = conditions[1:]

    new_groups = make_new_groups(groups)

    group_item_0 = groups[0]

    next_spring = groups[1:]
    if cond_char == "#":
        return hash_char_logic(group_item_0=group_item_0, next_str=next_str, new_groups=new_groups)

    if cond_char == ".":
        if not groups:
            return 1
        if group_item_0 == 0:
            return get_num_groups_undamaged(conditions=next_str, groups=next_spring)
        return get_num_groups_undamaged(conditions=next_str, groups=groups)
    if cond_char == "?":
        num_pos = get_num_groups_undamaged(conditions=next_str, groups=groups)
        if group_item_0 != 0:
            num_pos += get_num_groups_damaged(conditions=next_str, groups=new_groups)
        return num_pos
    error = "Invalid input"
    raise ValueError(error)


def get_num_groups_damaged(conditions: str, groups: tuple[int]) -> int:
    if not groups or groups == (0,):
        return int("#" not in conditions)

    if not conditions:
        return 0

    cond_char = conditions[0]
    next_str = conditions[1:]

    group_item_0 = groups[0]
    new_groups = make_new_groups(groups)

    next_spring = groups[1:]
    if cond_char == "#":
        return hash_char_logic(group_item_0=group_item_0, next_str=next_str, new_groups=new_groups)

    if cond_char == ".":
        if not groups:
            return 1
        if group_item_0 == 0:
            return get_num_groups_undamaged(conditions=next_str, groups=next_spring)
        return 0

    if cond_char == "?":
        if group_item_0 != 0:
            return get_num_groups_damaged(conditions=next_str, groups=new_groups)
        return get_num_groups_undamaged(conditions=next_str, groups=next_spring)
    error = "Invalid input"
    raise ValueError(error)


def main() -> None:
    """Main function to process input file and count arrangements."""
    input_file = Path("./Advent_of_code/2023/DAY12_Part2.txt")
    input_data = input_file.read_text().splitlines()

    result = 0
    modifier_num = 5
    for line in input_data:
        split_line = line.split(" ")

        letters = []
        numbers = []
        for _ in range(modifier_num):
            letters.append(split_line[0])
            numbers.extend([int(num) for num in split_line[1].split(",")])

        letters = "?".join(letters)
        numbers = tuple(numbers)
        result += get_num_groups_undamaged(conditions=letters, groups=numbers)
        get_num_groups_undamaged.cache_clear()
    print(result)


if __name__ == "__main__":
    main()
