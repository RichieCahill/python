"""DAY7_Part1"""
from itertools import product
from math import lcm
from pathlib import Path
from pprint import pprint


def create_map(input_data: str) -> dict[dict[str, str]]:
    """create_map"""
    search_map = {}
    for line in input_data:
        id, path = line.split(" = ")

        left, right = path.strip("()").split(", ")

        search_map[id] = {
            "L": left,
            "R": right,
        }
    return search_map


def get_pattern(
    instructions: str,
    search_map: dict[dict[str, str]],
    position: str,
    max_iter: int,
) -> str:
    """get_pattern"""
    output = []
    instruction_len = len(instructions)
    for index in range(max_iter):
        current_instruction = instructions[index % instruction_len]
        output.append(position)
        position = search_map.get(position).get(current_instruction)
    return output


def get_z_positions(pattern: list[str]) -> list[int]:
    """get_z_position"""
    return [index for index, position in enumerate(pattern) if position[-1] == "Z"]


def main():
    """main"""
    input_file = Path("./Advent_of_code/2023/DAY8_Part2.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    instructions = input_data.pop(0)
    input_data.pop(0)

    max_iter = len(instructions) * len(input_data)
    print(max_iter)

    search_map = create_map(input_data)

    positions = [position for position in search_map if position[-1] == "A"]
    patterns = [
        get_pattern(
            instructions=instructions,
            search_map=search_map,
            position=position,
            max_iter=max_iter,
        )
        for position in positions
    ]

    all_items_ending_with_z = [get_z_positions(pattern=pattern) for pattern in patterns]

    combinations = list(product(*all_items_ending_with_z))

    lcm_for_map = min([lcm(*combination) for combination in combinations])

    pprint(lcm_for_map)


main()
