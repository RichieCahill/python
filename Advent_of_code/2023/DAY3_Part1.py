"""DAY3_Part1"""

from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


@dataclass
class Cell:
    """Class to store cell content and position"""

    cell_content: str
    line_number: int
    cell_number: int

    def __init__(self, cell_content: str, line_number: int, cell_number: int) -> None:
        """Initiate class"""
        self.cell_content = cell_content
        self.line_number = line_number
        self.cell_number = cell_number


def check_cell(
    matrix: list[list[str]],
    line_number: int,
    cell_number: int,
) -> str | None:
    """Check if cell is in matrix and return cell content"""
    if line_number > len(matrix) or cell_number > len(matrix[line_number]):
        return None
    cell_content = matrix[line_number][cell_number]
    if cell_content == ".":
        return None
    return cell_content


def search_positions(
    matrix: list[list[str]],
    position_offsets: dict[str, list[int]],
    line_number: int,
    cell_number: int,
) -> dict[str, Cell]:
    """Search for cell in given positions"""
    search_result: dict[str, Cell] = {}
    for position, offset in position_offsets.items():
        offset_line_number = line_number + offset.get("line_offset")
        offset_cell_number = cell_number + offset.get("cell_offset")
        if cell_content := check_cell(
            matrix=matrix,
            line_number=offset_line_number,
            cell_number=offset_cell_number,
        ):
            search_result[position] = Cell(
                cell_content=cell_content,
                line_number=offset_line_number,
                cell_number=offset_cell_number,
            )

    return search_result


def search_cell_surroundings(
    matrix: list[str],
    line_number: int,
    cell_number: int,
) -> dict[str, Cell]:
    """Search for cell in all directions"""
    search_result: dict[str, Cell] = {}
    position_offsets_dicts = {
        "base": {
            "up": {"cell_offset": 0, "line_offset": -1},
            "down": {"cell_offset": 0, "line_offset": 1},
            "left": {"cell_offset": -1, "line_offset": 0},
            "right": {"cell_offset": 1, "line_offset": 0},
        },
        "up": {
            "up_left": {"cell_offset": -1, "line_offset": -1},
            "up_right": {"cell_offset": 1, "line_offset": -1},
        },
        "down": {
            "down_left": {"cell_offset": -1, "line_offset": 1},
            "down_right": {"cell_offset": 1, "line_offset": 1},
        },
    }
    for name, position_offsets in position_offsets_dicts.items():
        if name in search_result:
            continue

        search_result.update(
            search_positions(
                matrix=matrix,
                line_number=line_number,
                cell_number=cell_number,
                position_offsets=position_offsets,
            ),
        )

    return search_result


def search_right(matrix: list[list[str]], cell: Cell) -> str:
    """Search for numbers to the right"""
    number = ""
    for item in matrix[cell.line_number][cell.cell_number + 1 :]:
        if item.isdigit():
            number += item
            continue
        break
    return number


def search_left(matrix: list[list[str]], cell: Cell) -> str:
    """Search for numbers to the left"""
    number = ""
    for item in matrix[cell.line_number][cell.cell_number - 1 :: -1]:
        if item.isdigit():
            number += item
            continue
        break
    return number[::-1]


def compleat_right_number(matrix: list[list[str]], cell: Cell) -> int:
    """Compleat number from right side"""
    return int(cell.cell_content + search_right(matrix=matrix, cell=cell))


def compleat_left_number(matrix: list[list[str]], cell: Cell) -> int:
    """Compleat number from left side"""
    return int(search_left(matrix=matrix, cell=cell) + cell.cell_content)


def compleat_bidirectional_number(matrix: list[list[str]], cell: Cell) -> int:
    """Compleat number from both sides"""
    cell_content = cell.cell_content
    number = cell_content

    left_number_half = search_left(matrix=matrix, cell=cell)
    right_number_half = search_right(matrix=matrix, cell=cell)

    return int(left_number_half + number + right_number_half)


def find_all_number_bases(matrix: list[list[str]]) -> list[dict[Cell]]:
    """Find all number bases"""
    char_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
    search_results = []
    for line_number, line in enumerate(matrix):
        for cell_number, cell in enumerate(line):
            if cell not in char_list:
                search_results.append(
                    search_cell_surroundings(
                        matrix=matrix,
                        line_number=line_number,
                        cell_number=cell_number,
                    ),
                )
    return search_results


def total_numbers(matrix: list[list[str]], search_results: list) -> int:
    """Calculate total numbers"""
    total_number = 0
    for search_result in search_results:
        for name, cell in search_result.items():
            if name in ["up", "down"]:
                total_number += compleat_bidirectional_number(matrix=matrix, cell=cell)
            if "left" in name:
                total_number += compleat_left_number(matrix=matrix, cell=cell)
            if "right" in name:
                total_number += compleat_right_number(matrix=matrix, cell=cell)
    return total_number


def main():
    """Main"""
    input_file = Path("./Advent_of_code/2023/DAY3_Part1.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    matrix = [list(line) for line in input_data]

    search_results = find_all_number_bases(matrix=matrix)

    print(total_numbers(matrix=matrix, search_results=search_results))


main()
