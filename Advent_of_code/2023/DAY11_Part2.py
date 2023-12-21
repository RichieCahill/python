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
        return f"(row {self.row}, column {self.column})"


class Universe:
    """Universe"""

    expansion_factor = 1000000

    def __init__(self, input_data: list[str]) -> None:
        """__init__"""
        self.input_data = input_data
        self.galaxies = self.find_galaxies()
        self.empty_rows = self.find_empty_rows()
        self.empty_columns = self.find_empty_columns()

    def find_galaxies(self) -> list[list[tuple[int, int]]]:
        """find_galaxies"""
        galaxies = []
        for row_index, row in enumerate(self.input_data):
            for column_index, column in enumerate(row):
                if column == "#":
                    galaxies.append(Galaxy(row=row_index, column=column_index))
        return galaxies

    def find_empty_rows(self) -> list[int]:
        """find_empty_lines"""
        return {
            index
            for index, line in enumerate(self.input_data)
            if len(set(line)) == 1 and set(line) == {"."}
        }

    def find_empty_columns(self) -> set[int]:
        """find_empty_columns"""
        return {
            index
            for index, column in enumerate(zip(*self.input_data, strict=True))
            if len(set(column)) == 1 and set(column) == {"."}
        }

    def get_distance_set(self, pos1: int, pos2: int) -> set[int]:
        """get_distance_set"""
        if pos1 > pos2:
            return set(range(pos2, pos1))
        return set(range(pos1, pos2))

    def get_distance(self, galaxy1: Galaxy, galaxy2: Galaxy) -> int:
        """get_distance"""
        add_test = 0
        row_range = self.get_distance_set(galaxy1.row, galaxy2.row)
        row_intersection = self.empty_rows.intersection(row_range)
        if test := len(row_intersection):
            add_test += test * self.expansion_factor - test
        column_range = self.get_distance_set(galaxy2.column, galaxy1.column)
        column_intersection = self.empty_columns.intersection(column_range)
        if test := len(column_intersection):
            add_test += (test * self.expansion_factor) - test
        return (
            abs(galaxy1.row - galaxy2.row)
            + abs(galaxy1.column - galaxy2.column)
            + add_test
        )


def calculate_distance_between_galaxies(universe: Universe) -> dict:
    """calculate_distance_between_galaxies"""
    distances = []
    for index, galaxy in enumerate(universe.galaxies):
        distances.extend(
            [
                universe.get_distance(galaxy, other_galaxy)
                for other_galaxy in universe.galaxies[index + 1 :]
            ]
        )
    return distances


def main():
    input_file = Path("./Advent_of_code/2023/DAY11_Part2.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    universe = Universe(input_data=input_data)

    distances = calculate_distance_between_galaxies(universe=universe)
    pprint(sum(distances))


main()
