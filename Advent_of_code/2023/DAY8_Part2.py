"""DAY7_Part1"""
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


def get_new_position(
    positions: list[dict[str, str]],
    instruction: str,
    search_map: dict[dict[str, str]],
) -> list[dict[str, str]]:
    """get_new_position"""
    return [search_map.get(position).get(instruction) for position in positions]


def test_for_z(positions: str) -> bool:
    """test_for_z"""
    for position in positions:  # noqa: SIM110 this apreas to be slower
        if position[-1] != "Z":
            return False
    return True


def test_for_z_slow(positions: str) -> bool:
    """test_for_z"""
    return all(position[-1] == "Z" for position in positions)


def main():
    """main"""
    input_file = Path("./Advent_of_code/2023/DAY8_Part2.txt")
    with input_file.open("r") as file:
        input_data = [line.strip() for line in file]

    instruction = input_data.pop(0)
    input_data.pop(0)

    pprint(instruction)
    search_map = create_map(input_data)

    instruction_len = len(instruction)

    positions = [position for position in search_map if position[-1] == "A"]

    max_iter = 10000000
    count = 0
    while True:
        current_instruction = instruction[count % instruction_len]

        positions = get_new_position(
            positions=positions,
            instruction=current_instruction,
            search_map=search_map,
        )

        count += 1

        if test_for_z(positions=positions):
            break

        if count > max_iter:
            break

    print(count)


main()
