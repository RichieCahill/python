"""DAY7_Part1"""
from pathlib import Path
from pprint import pprint


class Galaxy:
    """Galaxy"""

    def __init__(self, row: int, column: int) -> None:
        """__init__"""
        self.row = row
        self.column = column

    def __repr__(self) -> str:
        """__repr__"""
        return f"({self.row}, {self.column})"

    def get_distance(self, other: "Galaxy") -> int:
        """get_distance"""
        return abs(self.row - other.row) + abs(self.column - other.column)


def add_lines(input_data: list[str]) -> list[str]:
    """add_lines"""
    indexes = [
        index
        for index, line in enumerate(input_data)
        if len(set(line)) == 1 and set(line) == {"."}
    ]
    line_len = len(input_data[0])
    indexes.sort(reverse=True)
    for index in indexes:
        input_data.insert(index, "." * line_len)
    return input_data


def add_rows_and_columns(input_data: list[str]) -> list[str]:
    """add_rows_and_columns"""
    for _ in range(2):
        input_data = add_lines(input_data)
        input_data = list(zip(*input_data, strict=True))
    return input_data


def find_galaxies(processed_data: list[str]) -> list[list[tuple[int, int]]]:
    """find_galaxies"""
    galaxies = []
    for row_index, row in enumerate(processed_data):
        for column_index, column in enumerate(row):
            if column == "#":
                galaxies.append(Galaxy(row=row_index, column=column_index))
    return galaxies


def calculate_distance_between_galaxies(galaxies: list[Galaxy]) -> dict:
    """calculate_distance_between_galaxies"""
    distances = []
    for index, galaxy in enumerate(galaxies):
        distances.extend(
            [
                galaxy.get_distance(other_galaxy)
                for other_galaxy in galaxies[index + 1 :]
            ]
        )
    return distances


def main():
    input_file = Path("./Advent_of_code/2023/DAY10_Part1.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    processed_data = add_rows_and_columns(input_data=input_data)

    galaxies = find_galaxies(processed_data=processed_data)

    distances = calculate_distance_between_galaxies(galaxies=galaxies)

    pprint(sum(distances))


main()
