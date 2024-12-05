"""DAY1_Part1"""

from pathlib import Path


def get_start_indexes(string: str, target_letter: str) -> list[int]:
    """Get the indexes of the target_letter's in the string."""
    return [i for i, letter in enumerate(string) if letter == target_letter]


def check_word(matrix: list[str], position_x: int, position_y: int) -> bool:
    """Check if the word is valid."""
    pattern = (
        f"{matrix[position_x + 1][position_y - 1]}"
        f"{matrix[position_x + 1][position_y + 1]}"
        f"{matrix[position_x - 1][position_y - 1]}"
        f"{matrix[position_x - 1][position_y + 1]}"
    )

    return pattern in ("MMSS", "SSMM", "SMSM", "MSMS")


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day04.txt")
    input_data = input_file.read_text().splitlines()

    output = 0
    line_len = len(input_data[0])
    for index, line in enumerate(input_data[1:-1], 1):
        start_indexes = [start for start in get_start_indexes(line, target_letter="A") if start < line_len - 1]
        output += sum(check_word(input_data, index, start) for start in start_indexes)

    print(output)


if __name__ == "__main__":
    main()
