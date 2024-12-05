"""DAY1_Part1"""

from pathlib import Path


def get_start_indexes(string: str, target_letter: str) -> list[int]:
    """Get the indexes of the target_letter's in the string."""
    return [i for i, letter in enumerate(string) if letter == target_letter]


def _check_word(  # noqa: PLR0913
    matrix: list[str],
    direction: tuple[int, int],
    word: str,
    word_index: int,
    start: tuple[int, int],
    word_len: int,
    matrix_len: int,
    line_len: int,
) -> bool:
    """Check if the word is valid."""
    x, y = start
    if word_index == word_len:
        return True
    if x < 0 or x >= matrix_len or y < 0 or y >= line_len or (matrix[x][y] != word[word_index]):
        return False
    return _check_word(
        matrix=matrix,
        direction=direction,
        word=word,
        word_index=word_index + 1,
        start=(x + direction[0], y + direction[1]),
        word_len=word_len,
        matrix_len=matrix_len,
        line_len=line_len,
    )


def check_word(matrix: list[str], start: tuple[int, int]) -> bool:
    """Check if the word is valid."""
    word = "XMAS"
    directions = {
        "up": (0, -1),
        "right_up": (1, -1),
        "right": (1, 0),
        "right_down": (1, 1),
        "down": (0, 1),
        "left_down": (-1, 1),
        "left": (-1, 0),
        "left_up": (-1, -1),
    }
    word_len = len(word)
    matrix_len = len(matrix)
    line_len = len(matrix[0])

    return sum(
        _check_word(
            matrix=matrix,
            direction=direction,
            word=word,
            word_index=0,
            start=start,
            word_len=word_len,
            matrix_len=matrix_len,
            line_len=line_len,
        )
        for direction in directions.values()
    )


def main() -> None:
    """Main function to read input file and calculate the sum of numbers in each line."""
    input_file = Path("./advent_of_code/2024/day04.txt")
    input_data = input_file.read_text().splitlines()

    output = 0
    for index, line in enumerate(input_data):
        start_indexes = get_start_indexes(line, target_letter="X")
        output += sum(check_word(input_data, (index, start)) for start in start_indexes)

    print(output)


if __name__ == "__main__":
    main()
