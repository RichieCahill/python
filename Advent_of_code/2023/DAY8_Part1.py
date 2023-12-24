"""DAY7_Part1"""
from pathlib import Path
from pprint import pprint
from time import sleep


def create_map(input_data):
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


def main():
    input_file = Path("./Advent_of_code/2023/DAY8_Part1.txt")
    input_data = input_file.read_text().splitlines()

    instruction = input_data.pop(0)
    input_data.pop(0)

    pprint(instruction)
    search_map = create_map(input_data)

    instruction_len = len(instruction)

    count = 0
    position = "AAA"
    while position != "ZZZ":
        current_instruction = instruction[count % instruction_len]
        position = search_map.get(position).get(current_instruction)

        count += 1

    print(count)


main()
