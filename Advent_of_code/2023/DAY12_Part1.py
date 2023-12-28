"""DAY12_Part1"""

from pathlib import Path


def is_valid(letters: str, groups: tuple[int]) -> bool:
    """Checks if the given arrangement satisfies the group constraints.

    Args:
        letters (list[str]): The arrangement of characters.
        groups (list[int]): The list of group sizes.

    Returns:
        bool: True if the arrangement satisfies the group constraints, False otherwise.
    """
    idx = 0
    for group in groups:
        idx = letters.find("#", idx)
        if idx == -1 or idx + group > len(letters) or letters[idx : idx + group] != "#" * group:
            return False
        idx += group
        if idx < len(letters) and letters[idx] != ".":
            return False
    return "#" not in letters[idx:]


def backtrack(letters: str, pos: int, groups: tuple[int]) -> int:
    """Explores all valid arrangements using backtracking.

    Args:
        letters (list[str]): The list of letters representing the arrangement.
        pos (int): The current position in the arrangement.
        groups (list[int]): The list of group sizes.

    Returns:
        int: The number of valid arrangements.
    """
    if pos == len(letters):
        return 1 if is_valid(letters, groups) else 0

    if letters[pos] != "?":
        return backtrack(letters, pos + 1, groups)

    count = 0
    for state in ["#", "."]:
        letters = letters[:pos] + state + letters[pos + 1 :]

        count += backtrack(letters, pos + 1, groups)
    letters = letters[:pos] + state + letters[pos + 1 :]
    return count


def main() -> None:
    """Main function to process input file and count arrangements."""
    input_file = Path("./Advent_of_code/2023/DAY12_Part1.txt")
    input_data = input_file.read_text().splitlines()

    result = 0
    for line in input_data:
        split_line = line.split(" ")
        letters = split_line[0]
        numbers = tuple([int(num) for num in split_line[1].split(",")])
        result += backtrack(letters=letters, pos=0, groups=numbers)

    print(result)


if __name__ == "__main__":
    main()
