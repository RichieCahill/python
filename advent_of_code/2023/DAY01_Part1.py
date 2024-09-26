"""DAY1_Part1"""

from pathlib import Path


def find_left_number(line: str) -> str:
    """Find the leftmost number in a string.

    Args:
        line (str): The input string.

    Returns:
        int: The leftmost number found in the string.
    """
    for char in line:
        if char.isdigit():
            return char
    error_msg = "No number found in string."
    raise ValueError(error_msg)


def find_right_number(line: str) -> str:
    """Find the rightmost number in a string.

    Args:
        line (str): The input string.

    Returns:
        int: The rightmost number found in the string.
    """
    for char in line[::-1]:
        if char.isdigit():
            return char
    error_msg = "No number found in string."
    raise ValueError(error_msg)


def find_number(line: str) -> int:
    """Find the number in a string by combining the leftmost and rightmost numbers.

    Args:
        line (str): The input string.

    Returns:
        int: The number found in the string.
    """
    return int(find_left_number(line) + find_right_number(line))


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./Advent_of_code/2023/DAY1_Part1.txt")
    input_data = input_file.read_text().splitlines()

    numbers = [find_number(line) for line in input_data]
    print(sum(numbers))


if __name__ == "__main__":
    main()

mv ./DAY1_Part1.py ./DAY01_Part1.py
mv ./DAY2_Part1.py ./DAY02_Part1.py
mv ./DAY3_Part1.py ./DAY03_Part1.py
mv ./DAY4_Part1.py ./DAY04_Part1.py
mv ./DAY6_Part1.py ./DAY06_Part1.py
mv ./DAY7_Part2.py ./DAY07_Part2.py
mv ./DAY8_Part2.py ./DAY08_Part2.py
mv ./DAY9_Part2.py ./DAY09_Part2.py
mv ./DAY1_Part2.py ./DAY01_Part2.py
mv ./DAY2_Part2.py ./DAY02_Part2.py
mv ./DAY3_Part2.py ./DAY03_Part2.py
mv ./DAY4_Part2.py ./DAY04_Part2.py
mv ./DAY7_Part1.py ./DAY07_Part1.py
mv ./DAY8_Part1.py ./DAY08_Part1.py
mv ./DAY9_Part1.py ./DAY09_Part1.py