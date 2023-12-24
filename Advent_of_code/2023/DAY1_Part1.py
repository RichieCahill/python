from pathlib import Path


def find_left_number(line: str) -> int:
    """
    Find the leftmost number in a string.

    Args:
        line (str): The input string.

    Returns:
        int: The leftmost number found in the string.
    """
    for char in line:
        if char.isdigit():
            return char


def find_right_number(line: str) -> int:
    """
    Find the rightmost number in a string.

    Args:
        line (str): The input string.

    Returns:
        int: The rightmost number found in the string.
    """
    for char in line[::-1]:
        if char.isdigit():
            return char


def find_number(line: str) -> int:
    """
    Find the number in a string by combining the leftmost and rightmost numbers.

    Args:
        line (str): The input string.

    Returns:
        int: The number found in the string.
    """
    return int(find_left_number(line) + find_right_number(line))


def main():
    """
    Main function to read input file and calculate the sum of numbers in each line.
    """
    input_file = Path("./Advent_of_code/2023/DAY1_Part1.txt")
    input_data = input_file.read_text().splitlines()

    print(sum([find_number(line) for line in input_data]))


if __name__ == "__main__":
    main()
